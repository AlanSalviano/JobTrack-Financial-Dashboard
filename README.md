
# Sheet2Dash — Service Payment & Profit Dashboard

Este é um sistema desenvolvido em **Python + Streamlit**, que realiza análises financeiras de serviços. Ele permite processar planilhas, calcular pagamentos de funcionários, visualizar dashboards interativos e gerar relatórios profissionais em PDF.

---

## 🔥 Funcionalidades

- ✅ Processamento automático de planilhas Excel (.xlsx)
- ✅ Filtros por semanas, funcionário e categorias
- ✅ Cálculo de:
  - Pagamento dos funcionários
  - Lucro da empresa
- ✅ Dashboard interativo com:
  - Gráficos de evolução semanal
  - Pagamento por funcionário
  - Utilização dos métodos de pagamento
  - Distribuição de atendimentos por dia da semana
- ✅ Cards de produtividade:
  - 🏆 **Employeer of the Week**
  - 📉 Menor produtividade da semana
- ✅ Relatórios em PDF:
  - 📑 Relatório geral
  - 💳 Recibo individual do funcionário
  - 🏅 Certificado do funcionário of the Week
- ✅ Exportação de dados em CSV

---

## 🏗️ Estrutura do Projeto

```
📦 bns-finance-app
 ┣ 📜 app.py                 → Interface principal no Streamlit
 ┣ 📜 run_app.py             → Arquivo para rodar o app
 ┣ 📜 calculations.py        → Cálculos de pagamento e lucro
 ┣ 📜 config.py              → Configurações globais
 ┣ 📜 data_processor.py      → Processamento das planilhas Excel
 ┣ 📜 pdf_generator.py       → Geração dos PDFs e recibos
 ┣ 📜 utils.py               → Funções auxiliares (ex.: formatação de moeda)
 ┣ 📜 visualization.py       → Criação dos gráficos Plotly
 ┣ 📜 README.md              → Este arquivo (documentação)
 ┣ 📜 requirements.txt       → Dependências do projeto
 ┗ 📁 styles/                → Arquivos de estilos (CSS opcional)
```

---

## 🚀 Instalação e Execução

### 🔧 Pré-requisitos:
- Python 3.9 ou superior

### 🔥 Instalação:

1. Clone este repositório:
```bash
git clone https://github.com/AlanSalviano/JobTrack-Financial-Dashboard.git
cd seu-repositorio
```

2. Crie e ative um ambiente virtual:
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
python run_app.py
```

✅ Acesse no navegador: `http://localhost:8501`

---

## 📑 Como Usar

1. Carregue uma ou mais planilhas Excel (**.xlsx**) ou cole a URL de uma planilha online.
2. Utilize os filtros na barra lateral para:
   - Selecionar semanas específicas
   - Selecionar funcionários
   - Filtrar por categoria
3. Explore os dashboards:
   - Métricas rápidas
   - Gráficos interativos
   - Cards de produtividade (Melhor e pior desempenho da semana)
   - Lista de atendimentos não realizados
4. Exporte os dados:
   - 📁 CSV dos dados brutos
   - 📑 Relatório PDF geral
   - 💳 Recibo PDF do funcionário
   - 🏆 Certificado PDF do Employeer of the Week

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — Frontend e interface web
- [Plotly](https://plotly.com/python/) — Gráficos interativos
- [FPDF](https://pyfpdf.github.io/fpdf2/) — Geração de PDFs
- [Pandas](https://pandas.pydata.org/) — Manipulação de dados
- [NumPy](https://numpy.org/) — Cálculos numéricos

---

## 🧠 Sobre o Funcionamento

O sistema lê planilhas Excel no formato semanal, extrai os dados dos funcionários, seus serviços, gorjetas, pagamentos e calcula automaticamente:

- **Pagamento do funcionário** baseado na categoria:
  - Funcionário, Coordinator, Training, Started ou Registering
- **Lucro da empresa**
- **Produtividade dos funcionários**

E gera dashboards com métricas e gráficos, além de relatórios e recibos em PDF.

---

## 📜 Licença

Este projeto está sob a Licença MIT — sinta-se livre para usar, copiar, modificar e distribuir.

---

## 🙋‍♂️ Autor

Desenvolvido por **AlanSalviano**.

---

## ⭐ Se este projeto foi útil...

Considere deixar uma ⭐ no repositório! Isso me ajuda muito! 🚀😉
