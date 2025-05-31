from fpdf import FPDF
from datetime import datetime
import pandas as pd
from .utils import format_currency
from .config import FORMAS_PAGAMENTO_VALIDAS


def create_pdf(data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)

    left_margin = 10
    right_margin = 10
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    page_width = pdf.w - left_margin - right_margin

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(page_width, 10, txt="FINANCIAL ANALYSIS REPORT", ln=1, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.cell(page_width, 10, txt=f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=1, align='R')
    pdf.ln(10)

    completed_services = data[data['Realizado']]
    not_completed = data[(data['Realizado'] == False) & (data['Cliente'].notna())]

    metrics = [
        ("Completed Appointments", len(completed_services)),
        ("Not Completed", len(not_completed)),
        ("Total Services", format_currency(completed_services['Services'].sum())),
        ("Total Tips", format_currency(completed_services['Gorjeta'].sum())),
        ("Company Profit", format_currency(completed_services['Lucro Empresa'].sum()))
    ]

    for metric, value in metrics:
        pdf.cell(page_width / 2, 10, txt=f"{metric}:", ln=0)
        pdf.cell(page_width / 2, 10, txt=str(value), ln=1)

    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(page_width, 10, txt="Summary per Employee", ln=1)

    summary = completed_services.groupby(['Nome', 'Categoria']).agg({
        'Services': 'sum',
        'Gorjeta': 'sum',
        'Pagamento Employee': 'sum',
        'Lucro Empresa': 'sum',
        'Cliente': 'count'
    }).reset_index()

    summary.columns = ['Employee', 'Category', 'Total Services', 'Total Tips',
                        'Total Payment', 'Company Profit', 'Appointments']

    pdf.set_font("Arial", size=8)
    col_widths = [30, 25, 25, 25, 25, 25]

    headers = ["Employee", "Category", "Services", "Tips", "Payment", "Profit"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, txt=header, border=1, align='C')
    pdf.ln()

    for _, row in summary.iterrows():
        pdf.cell(col_widths[0], 10, txt=str(row['Employee'])[:15], border=1)
        pdf.cell(col_widths[1], 10, txt=str(row['Category'])[:10], border=1)
        pdf.cell(col_widths[2], 10, txt=format_currency(row['Total Services']), border=1, align='R')
        pdf.cell(col_widths[3], 10, txt=format_currency(row['Total Tips']), border=1, align='R')
        pdf.cell(col_widths[4], 10, txt=format_currency(row['Total Payment']), border=1, align='R')
        pdf.cell(col_widths[5], 10, txt=format_currency(row['Company Profit']), border=1, align='R')
        pdf.ln()

    pdf.ln(10)

    return pdf


def create_employee_payment_receipt(emp_data, emp_name, week):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    left_margin = 15
    right_margin = 15
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    page_width = pdf.w - left_margin - right_margin

    min_date = emp_data['Data'].min().strftime('%m/%d/%y')
    max_date = emp_data['Data'].max().strftime('%m/%d/%y')
    date_range = f"{min_date} to {max_date}"

    pdf.set_font("Arial", 'B', 18)
    pdf.cell(page_width, 10, txt="EMPLOYEE PAYMENT RECEIPT", ln=1, align='C')
    pdf.ln(9)

    pdf.set_font("Arial", size=10)
    pdf.cell(page_width, 8, txt=f"Employee: {emp_name}", ln=1)
    pdf.cell(page_width, 8, txt=f"Reference: {date_range}", ln=1)
    pdf.cell(page_width, 8, txt=f"Issue Date: {datetime.now().strftime('%m/%d/%Y')}", ln=1)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(page_width, 10, txt="SUMMARY OF SERVICES", ln=1)
    pdf.set_font("Arial", size=10)

    total_services = emp_data['Services'].sum()
    total_tips = emp_data['Gorjeta'].sum()
    total_payment = emp_data['Pagamento Employee'].sum()

    col_widths = [page_width / 2, page_width / 2]

    pdf.cell(col_widths[0], 10, txt="Total Appointments:", border='B', ln=0)
    pdf.cell(col_widths[1], 10, txt=str(len(emp_data)), border='B', ln=1, align='R')

    pdf.cell(col_widths[0], 10, txt="Total in Services:", border='B', ln=0)
    pdf.cell(col_widths[1], 10, txt=format_currency(total_services), border='B', ln=1, align='R')

    pdf.cell(col_widths[0], 10, txt="Total in Tips:", border='B', ln=0)
    pdf.cell(col_widths[1], 10, txt=format_currency(total_tips), border='B', ln=1, align='R')

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(col_widths[0], 10, txt="Total Payment:", border='B', ln=0)
    pdf.cell(col_widths[1], 10, txt=format_currency(total_payment), border='B', ln=1, align='R')

    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(page_width, 5, txt="This receipt was generated automatically.", ln=1, align='C')

    return pdf


def create_employee_of_the_week_receipt(emp_data, emp_name, week):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    left_margin = 15
    right_margin = 15
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    page_width = pdf.w - left_margin - right_margin

    min_date = emp_data['Data'].min().strftime('%m/%d/%y')
    max_date = emp_data['Data'].max().strftime('%m/%d/%y')
    date_range = f"{min_date} to {max_date}"

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(page_width, 10, txt="You have performed excellent services and have been recognized as:", ln=1, align='C')

    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(page_width, 15, txt="EMPLOYEE OF THE WEEK", ln=1, align='C')

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(page_width, 10, txt="Congratulations on your outstanding performance!", ln=1, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", '', 11)
    pdf.cell(page_width, 8, txt=f"Employee: {emp_name}", ln=1)
    pdf.cell(page_width, 8, txt=f"Reference: {date_range}", ln=1)
    pdf.cell(page_width, 8, txt=f"Issue Date: {datetime.now().strftime('%m/%d/%Y')}", ln=1)

    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(page_width, 5, txt="This certificate was generated automatically.", ln=1, align='C')

    return pdf
