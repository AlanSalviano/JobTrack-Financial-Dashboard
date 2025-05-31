import streamlit as st
import pandas as pd

from modules.data_processor import process_spreadsheet
from modules.calculations import calcular_pagamento_semanal, calcular_pagamento_individual
from modules.config import FORMAS_PAGAMENTO_VALIDAS, INVALID_CLIENTS
from modules.pdf_generator import (
    create_pdf,
    create_employee_payment_receipt,
    create_employee_of_the_week_receipt
)
from modules.visualization import (
    plot_weekly_evolution,
    plot_weekly_payments,
    plot_payment_methods_total,
    plot_payment_methods_usage
)
from modules.utils import format_currency

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Employee Financial Dashboard", layout="wide")
    local_css("styles.css")

    st.sidebar.title("Filters")

    uploaded_files = st.sidebar.file_uploader(
        "Upload one or more Excel spreadsheets",
        type=['xlsx'],
        accept_multiple_files=True
    )

    url_input = st.sidebar.text_input("Or paste the URL of an online spreadsheet")

    st.title("Employee Financial Dashboard")

    all_dataframes = []

    if uploaded_files or url_input:
        files_to_process = uploaded_files if uploaded_files else [url_input]
        for file in files_to_process:
            df = process_spreadsheet(file)
            if not df.empty:
                all_dataframes.append(df)

    if all_dataframes:
        data = pd.concat(all_dataframes, ignore_index=True)

        data = data[data['Nome'].notna() & (data['Nome'].astype(str).str.strip() != '')]
        data = data[~data['Cliente'].astype(str).str.strip().str.upper().isin([c.upper() for c in INVALID_CLIENTS])]

        weeks = data['Semana'].unique()
        employees = data['Nome'].unique()
        categories = data['Categoria'].unique()

        st.sidebar.header("Filter by:")

        selected_weeks = st.sidebar.multiselect("Select weeks for analysis", options=weeks)
        selected_employees = st.sidebar.multiselect("Select employees:", options=employees, default=list(employees))
        selected_categories = st.sidebar.multiselect("Select categories:", options=categories, default=list(categories))

        if selected_weeks:
            data = data[data['Semana'].isin(selected_weeks)]
        if selected_employees:
            data = data[data['Nome'].isin(selected_employees)]
        if selected_categories:
            data = data[data['Categoria'].isin(selected_categories)]

        if data.empty:
            st.warning("No data found with the selected filters.")
            st.stop()

        st.success("Spreadsheets processed successfully!")

        if st.checkbox("Show raw data"):
            st.dataframe(data)

        completed_services = data[data['Realizado']]
        not_completed = data[(data['Realizado'] == False) & (data['Cliente'].notna())]

        dias_trabalhados = completed_services.groupby(['Nome', 'Semana', 'Data']).size().reset_index()
        dias_trabalhados = dias_trabalhados.groupby(['Nome', 'Semana']).size().reset_index(name='Dias Trabalhados')

        weekly_totals = completed_services.groupby(['Nome', 'Semana', 'Categoria']).agg({
            'Services': 'sum',
            'Gorjeta': 'sum',
            'Dia': 'count'
        }).reset_index()

        weekly_totals = pd.merge(weekly_totals, dias_trabalhados, on=['Nome', 'Semana'], how='left')

        weekly_totals[['Pagamento Employee', 'Lucro Empresa']] = weekly_totals.apply(
            calcular_pagamento_semanal, axis=1, result_type='expand'
        )

        completed_services[['Pagamento Employee', 'Lucro Empresa']] = completed_services.apply(
            lambda x: calcular_pagamento_individual(x, weekly_totals), axis=1, result_type='expand'
        )

        total_lucro = completed_services['Lucro Empresa'].sum()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Completed", len(completed_services))
        col2.metric("Not Completed", len(not_completed))
        col3.metric("Total Services", format_currency(completed_services['Services'].sum()))
        col4.metric("Total Tips", format_currency(completed_services['Gorjeta'].sum()))
        col5.metric("Company Profit", format_currency(total_lucro))

        st.subheader("Weekly Service Evolution")
        st.plotly_chart(plot_weekly_evolution(weekly_totals), use_container_width=True)

        st.subheader("Weekly Payment per Employee")
        st.plotly_chart(plot_weekly_payments(weekly_totals), use_container_width=True)

        st.subheader("Summary per Employee")

        emp_summary = weekly_totals.groupby(['Nome', 'Categoria']).agg({
            'Services': 'sum',
            'Gorjeta': 'sum',
            'Pagamento Employee': 'sum',
            'Lucro Empresa': 'sum',
            'Dia': 'sum',
            'Dias Trabalhados': 'sum'
        }).reset_index()

        emp_summary.columns = ['Employee', 'Category', 'Total Services', 'Total Tips', 'Total Payment', 'Company Profit', 'Appointments', 'Worked Days']

        emp_summary['Average Service'] = emp_summary['Total Services'] / emp_summary['Appointments']
        emp_summary['Average Tip'] = emp_summary['Total Tips'] / emp_summary['Appointments']

        for col in ['Total Services', 'Total Tips', 'Total Payment', 'Company Profit', 'Average Service', 'Average Tip']:
            emp_summary[col] = emp_summary[col].apply(format_currency)

        st.dataframe(emp_summary.sort_values('Appointments', ascending=False))

        if len(selected_weeks) == 1:
            week = selected_weeks[0]
            week_data = completed_services[completed_services['Semana'] == week]

            if not week_data.empty:
                summary = week_data.groupby('Nome').agg({'Cliente': 'count'}).reset_index().rename(columns={'Cliente': 'Appointments'})

                avg_appointments = summary['Appointments'].mean()

                top_emp = summary.sort_values('Appointments', ascending=False).iloc[0]
                low_emp = summary.sort_values('Appointments', ascending=True).iloc[0]

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Employee of the Week")
                    st.success(f"**{top_emp['Nome']}** had the best metrics in week **{week}**!")
                    st.markdown(f"""
                        - **Appointments:** {top_emp['Appointments']}  
                        - **Employee Average:** {avg_appointments:.2f}  
                        - **Productivity:** {((top_emp['Appointments'] / avg_appointments) - 1) * 100:+.1f}%
                    """)

                with col2:
                    st.subheader("Lowest Productivity of the Week")
                    st.error(f"**{low_emp['Nome']}** had the lowest number of appointments in week **{week}**.")
                    st.markdown(f"""
                        - **Appointments:** {low_emp['Appointments']}  
                        - **Employee Average:** {avg_appointments:.2f}  
                        - **Productivity:** {((low_emp['Appointments'] / avg_appointments) - 1) * 100:+.1f}%
                    """)

        else:
            st.info("Select exactly **one week** to view the employee productivity cards.")

        st.subheader("Appointments Not Completed")
        if not not_completed.empty:
            st.warning(f"{len(not_completed)} appointments not completed.")
            st.dataframe(not_completed[['Nome', 'Dia', 'Data', 'Cliente']])
        else:
            st.success("All scheduled appointments were completed!")

        st.subheader("Payment Method Summary")

        valid_payments = completed_services[completed_services['Pagamento'].isin(FORMAS_PAGAMENTO_VALIDAS)]

        if not valid_payments.empty:
            payment_summary = valid_payments.groupby('Pagamento').agg({
                'Services': 'sum',
                'Gorjeta': 'sum',
                'Cliente': 'count'
            }).reset_index().rename(columns={'Cliente': 'Usage Count'})

            payment_summary['Total'] = payment_summary['Services'] + payment_summary['Gorjeta']
            payment_summary['Usage Percentage'] = (payment_summary['Usage Count'] / payment_summary['Usage Count'].sum() * 100).round(2)

            st.dataframe(payment_summary)

            st.plotly_chart(plot_payment_methods_total(payment_summary), use_container_width=True)
            st.plotly_chart(plot_payment_methods_usage(payment_summary), use_container_width=True)

        st.subheader("Export Data")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="employee_services.csv", mime="text/csv")

        with col2:
            pdf = create_pdf(completed_services)
            pdf_output = pdf.output(dest='S').encode('latin-1')

            st.download_button("Download PDF Report", data=pdf_output, file_name="general_report.pdf", mime="application/pdf")

        with col3:
            if len(selected_employees) == 1 and len(selected_weeks) == 1:
                emp_name = selected_employees[0]
                week = selected_weeks[0]
                emp_data = completed_services[(completed_services['Nome'] == emp_name) & (completed_services['Semana'] == week)]

                pdf = create_employee_payment_receipt(emp_data, emp_name, week)
                pdf_output = pdf.output(dest='S').encode('latin-1')

                st.download_button(f"Receipt {emp_name}", data=pdf_output, file_name=f"receipt_{emp_name}_{week}.pdf", mime="application/pdf")
            else:
                st.info("Select exactly 1 employee and 1 week to generate the receipt.")

        with col4:
            if len(selected_employees) == 1 and len(selected_weeks) == 1:
                emp_name = selected_employees[0]
                week = selected_weeks[0]
                emp_data = completed_services[(completed_services['Nome'] == emp_name) & (completed_services['Semana'] == week)]

                pdf = create_employee_of_the_week_receipt(emp_data, emp_name, week)
                pdf_output = pdf.output(dest='S').encode('latin-1')

                st.download_button(f"Employee of the Week {emp_name}", data=pdf_output, file_name=f"employee_of_the_week_{emp_name}_{week}.pdf", mime="application/pdf")
            else:
                st.info("Select exactly 1 employee and 1 week to generate the certificate.")

    else:
        st.warning("No spreadsheet loaded. Please upload a spreadsheet to start.")

if __name__ == "__main__":
    main()
