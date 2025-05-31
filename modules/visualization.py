import plotly.express as px
import pandas as pd
from .utils import format_currency


# 📈 Gráfico de evolução semanal por employee
def plot_weekly_evolution(data):
    fig = px.line(
        data,
        x='Semana',
        y='Services',
        color='Nome',
        markers=True,
        title='Weekly Service Evolution by Employee',
        labels={'Services': 'Service Value ($)', 'Semana': 'Week'}
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Value: $%{y:,.2f}")
    return fig


# 💰 Gráfico de pagamento semanal por employee
def plot_weekly_payments(data):
    fig = px.bar(
        data.sort_values('Pagamento Employee'),
        x='Pagamento Employee',
        y='Nome',
        color='Semana',
        barmode='group',
        title='Weekly Payment per Employee',
        labels={'Pagamento Employee': 'Payment ($)', 'Nome': 'Employee'}
    )
    fig.update_traces(
        texttemplate='$%{x:,.2f}',
        textposition='outside'
    )
    fig.update_layout(hovermode="x unified")
    return fig


# 👥 Gráfico de atendimentos por employee
def plot_services_by_employee(data):
    fig = px.bar(
        data.sort_values('Atendimentos'),
        x='Atendimentos',
        y='Nome',
        title='Appointments by Employee',
        color='Categoria',
        labels={'Atendimentos': 'Count', 'Nome': 'Employee'}
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Appointments: %{x}<br>Category: %{marker.color}"
    )
    return fig


# 💵 Gráfico de gorjetas por employee
def plot_tips_by_employee(data):
    fig = px.bar(
        data.sort_values('Gorjeta'),
        x='Gorjeta',
        y='Nome',
        title='Tips by Employee',
        color='Categoria',
        labels={'Gorjeta': 'Tips Value ($)', 'Nome': 'Employee'}
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total Tips: $%{x:,.2f}<br>Category: %{marker.color}"
    )
    return fig


# 📆 Gráfico de atendimentos por dia da semana
def plot_services_by_day(data):
    fig = px.bar(
        data,
        x='Dia',
        y='Atendimentos',
        title='Appointments by Day of the Week',
        labels={'Atendimentos': 'Count', 'Dia': 'Day'}
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Appointments: %{y}"
    )
    return fig


# 💳 Gráfico de valor total por método de pagamento
def plot_payment_methods_total(data):
    fig = px.bar(
        data.sort_values('Total'),
        x='Total',
        y='Pagamento',
        title='Total Value by Payment Method (Services + Tips)',
        color='Services',
        color_continuous_scale='Peach',
        labels={'Total': 'Total Value ($)', 'Services': 'Service Value ($)'}
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total: $%{x:,.2f}<br>Services: $%{marker.color:,.2f}"
    )
    return fig


# 📊 Gráfico de quantidade de usos por método de pagamento
def plot_payment_methods_usage(data):
    if 'Percentual Uso' not in data.columns:
        data['Percentual Uso'] = (data['Qtd Usos'] / data['Qtd Usos'].sum() * 100).round(2)

    fig = px.bar(
        data.sort_values('Qtd Usos'),
        x='Qtd Usos',
        y='Pagamento',
        title='Usage Count by Payment Method',
        color='Qtd Usos',
        color_continuous_scale='Peach',
        labels={'Qtd Usos': 'Usage Count'},
        text='Percentual Uso'
    )
    fig.update_traces(
        texttemplate='%{text}%',
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Usage: %{x}<br>% of Total: %{text}%"
    )
    return fig

