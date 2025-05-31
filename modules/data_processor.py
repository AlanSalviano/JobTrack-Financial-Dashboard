import pandas as pd
import numpy as np
from io import BytesIO
import requests
from .config import INVALID_CLIENTS, FORMAS_PAGAMENTO_VALIDAS


def process_spreadsheet(file):
    all_weeks_data = {}

    if isinstance(file, str) and file.startswith('http'):
        response = requests.get(file)
        file = BytesIO(response.content)
    elif isinstance(file, BytesIO):
        file.seek(0)

    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if sheet_name.startswith('WEEK'):
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            employee_blocks = []
            current_block = []
            collecting = False

            for idx, row in df.iterrows():
                if any('NAME:' in str(cell) for cell in row.values):
                    if current_block:
                        employee_blocks.append(current_block)
                        current_block = []
                    collecting = True
                if collecting:
                    current_block.append(row)
            if current_block:
                employee_blocks.append(current_block)

            week_data = []
            for block in employee_blocks:
                name_row = next((row for row in block if any('NAME:' in str(cell) for cell in row.values)), None)

                if name_row is None:
                    continue

                name_col = next(
                    (i for i, cell in enumerate(name_row.values) if isinstance(cell, str) and 'NAME:' in cell), None
                )

                employee_info = {
                    'Semana': sheet_name,
                    'Nome': name_row[name_col + 1] if name_col is not None else None,
                    'Categoria': name_row[name_col + 3] if name_col is not None else None,
                    'Origem': name_row[name_col + 5] if name_col is not None and 'From:' in str(name_row[name_col + 4]) else None
                }

                header_row = next((i for i, row in enumerate(block) if all(
                    keyword in str(row.values) for keyword in ['Schedule', 'DATE', 'SERVICE']
                )), None)

                if header_row is None:
                    continue

                days_data = []
                for i in range(header_row + 1, len(block)):
                    day_row = block[i]
                    for day_idx, day_col in enumerate(
                        [(1, 9), (10, 18), (19, 27), (28, 36), (37, 45), (46, 54), (55, 63)]
                    ):
                        start_col, end_col = day_col
                        day_data = day_row[start_col:end_col + 1].values
                        client_name = str(day_data[0]).strip() if pd.notna(day_data[0]) else ''

                        if not client_name or client_name.upper() in [c.upper() for c in INVALID_CLIENTS]:
                            continue

                        if pd.notna(day_data[2]) and str(day_data[2]).strip() and str(day_data[2]).strip() != 'nan':
                            try:
                                service_value = float(day_data[2])
                            except:
                                service_value = np.nan
                            if not np.isnan(service_value):
                                pagamento = day_data[5] if pd.notna(day_data[5]) and str(day_data[5]).strip() in FORMAS_PAGAMENTO_VALIDAS else None
                                tip_value = float(day_data[3]) if pd.notna(day_data[3]) else 0
                                day_info = {
                                    'Dia': ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'][day_idx],
                                    'Data': day_data[1],
                                    'Cliente': client_name,
                                    'Services': service_value,
                                    'Gorjeta': tip_value,
                                    'Products': day_data[4] if pd.notna(day_data[4]) else 0,
                                    'Pagamento': pagamento,
                                    'ID Pagamento': day_data[6] if pd.notna(day_data[6]) else None,
                                    'Verificado': day_data[7] if pd.notna(day_data[7]) else False,
                                    'Realizado': True
                                }
                                days_data.append({**employee_info, **day_info})
                        elif pd.notna(day_data[0]):
                            if client_name.upper() in [c.upper() for c in INVALID_CLIENTS]:
                                continue
                            day_info = {
                                'Dia': ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'][day_idx],
                                'Data': day_data[1],
                                'Cliente': client_name,
                                'Services': 0,
                                'Gorjeta': 0,
                                'Products': 0,
                                'Pagamento': None,
                                'ID Pagamento': None,
                                'Verificado': False,
                                'Realizado': False
                            }
                            days_data.append({**employee_info, **day_info})

                week_data.extend(days_data)

            if week_data:
                all_weeks_data[sheet_name] = pd.DataFrame(week_data)

    if all_weeks_data:
        combined_data = pd.concat(all_weeks_data.values(), ignore_index=True)
        combined_data['Data'] = pd.to_datetime(combined_data['Data'], errors='coerce')
        combined_data['Services'] = pd.to_numeric(combined_data['Services'], errors='coerce')
        combined_data['Gorjeta'] = pd.to_numeric(combined_data['Gorjeta'], errors='coerce').fillna(0)
        combined_data['Products'] = pd.to_numeric(combined_data['Products'], errors='coerce').fillna(0)
        combined_data = combined_data.dropna(subset=['Data'])
        combined_data = combined_data[
            ~combined_data['Cliente'].astype(str).str.strip().str.upper().isin([c.upper() for c in INVALID_CLIENTS])
        ]
        return combined_data

    return pd.DataFrame()
