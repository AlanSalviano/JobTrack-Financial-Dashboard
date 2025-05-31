import pandas as pd


def calcular_pagamento_individual(row, weekly_data):
    emp_week_data = weekly_data[
        (weekly_data['Nome'] == row['Nome']) &
        (weekly_data['Semana'] == row['Semana'])
    ]

    if len(emp_week_data) == 0:
        return pd.Series([0, row['Services'] + row['Gorjeta']])

    total_pagamento = emp_week_data['Pagamento Employee'].iloc[
        0] if 'Pagamento Employee' in emp_week_data.columns else 0
    total_servico = emp_week_data['Services'].sum()

    if total_servico == 0:
        return pd.Series([0, row['Services'] + row['Gorjeta']])

    try:
        pagamento = (row['Services'] / total_servico) * total_pagamento
        lucro = row['Services'] + row['Gorjeta'] - pagamento
    except:
        pagamento = 0
        lucro = row['Services'] + row['Gorjeta']

    return pd.Series([pagamento, lucro])


def calcular_pagamento_semanal(row):
    categoria = row['Categoria']
    servico = row['Services']
    gorjeta = row['Gorjeta']
    dias_trabalhados = row['Dias Trabalhados']

    if categoria == 'Registering':
        pagamento = 0.00
        lucro = servico + gorjeta
    elif categoria == 'Employee':
        pagamento = servico * 0.20 + gorjeta
        lucro = servico * 0.80
    elif categoria == 'Training':
        pagamento = 80 * dias_trabalhados
        lucro = servico + gorjeta - pagamento
    elif categoria == 'Coordinator':
        pagamento = servico * 0.25 + gorjeta
        lucro = servico * 0.75
    elif categoria == 'Started':
        valor_comissao = servico * 0.20 + gorjeta
        valor_minimo = 150 * dias_trabalhados
        pagamento = max(valor_minimo, valor_comissao)
        lucro = servico + gorjeta - pagamento
    else:
        pagamento = 0
        lucro = servico + gorjeta

    return pd.Series([pagamento, lucro])
