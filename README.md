# Análise de Comportamento do Cliente / Customer Behavior Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🇧🇷 Português

### Descrição
Este projeto visa analisar o comportamento do cliente usando dados de compras para identificar padrões, segmentar clientes e prever a rotatividade (churn). Ele utiliza técnicas de análise RFM (Recência, Frequência, Valor Monetário) e aprendizado de máquina para fornecer insights acionáveis.

### Funcionalidades
- **Geração de Dados Sintéticos**: Se nenhum arquivo de dados for fornecido, o projeto pode gerar dados sintéticos para demonstração.
- **Cálculo de Métricas do Cliente**: Calcula métricas importantes como Recência, Frequência, Valor Monetário (RFM) e Valor de Vida do Cliente (CLV).
- **Segmentação de Clientes**: Utiliza o algoritmo K-Means para segmentar clientes com base em suas métricas RFM.
- **Análise de Características do Segmento**: Fornece um resumo das características de cada segmento de cliente.
- **Visualizações Interativas**: Gera um dashboard interativo em HTML com gráficos 3D de segmentação, distribuição de churn, receita por segmento e CLV médio por segmento.
- **Previsão de Churn**: Constrói e avalia um modelo de Random Forest para prever a rotatividade de clientes.
- **Relatório de Insights**: Gera um relatório consolidado com os principais insights da análise.

### Instalação
Para configurar o ambiente de desenvolvimento, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Customer-Behavior-Analytics.git
   cd Customer-Behavior-Analytics
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r config/requirements.txt
   ```

### Uso
Para executar a análise completa, execute o script principal:

```bash
python3 src/customer_analytics.py
```

- Se você tiver seus próprios dados de cliente em formato CSV, coloque-os em `src/data/customer_data.csv`. O script usará esses dados. Caso contrário, dados sintéticos serão gerados automaticamente.
- Um dashboard interativo (`docs/customer_behavior_dashboard.html`) será gerado na pasta `docs/` do projeto.

### Estrutura do Projeto
```
Customer-Behavior-Analytics/
├── config/
│   └── requirements.txt
├── docs/
│   ├── notebooks/
│   └── customer_behavior_dashboard.html (dashboard gerado)
├── src/
│   ├── data/
│   │   └── customer_data.csv (opcional, para seus dados)
│   └── customer_analytics.py
├── tests/
│   └── test_customer_analytics.py
├── .gitignore
└── README.md
```

### GitHub Pages
Este projeto está configurado para ser publicado no GitHub Pages. O dashboard interativo (`customer_behavior_dashboard.html`) gerado pode ser visualizado diretamente através do GitHub Pages. Para ativar, vá para as configurações do seu repositório no GitHub, selecione 'Pages' e configure a fonte para a branch `gh-pages` (ou `main`/`master` com a pasta `/docs`).

### Tecnologias Utilizadas
- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- Plotly

### Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

### Contribuição
Contribuições são bem-vindas! Por favor, siga estas diretrizes:
1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature/sua-feature`).
3. Faça suas alterações e commit-as (`git commit -m 'Adiciona nova feature'`).
4. Envie para a branch (`git push origin feature/sua-feature`).
5. Abra um Pull Request.

---

## 🇬🇧 English

### Description
This project aims to analyze customer behavior using purchase data to identify patterns, segment customers, and predict churn. It utilizes RFM (Recency, Frequency, Monetary) analysis and machine learning techniques to provide actionable insights.

### Features
- **Synthetic Data Generation**: If no data file is provided, the project can generate synthetic data for demonstration purposes.
- **Customer Metrics Calculation**: Calculates important metrics such as Recency, Frequency, Monetary (RFM), and Customer Lifetime Value (CLV).
- **Customer Segmentation**: Uses the K-Means algorithm to segment customers based on their RFM metrics.
- **Segment Characteristics Analysis**: Provides a summary of the characteristics of each customer segment.
- **Interactive Visualizations**: Generates an interactive HTML dashboard with 3D segmentation plots, churn distribution, revenue by segment, and average CLV by segment.
- **Churn Prediction**: Builds and evaluates a Random Forest model to predict customer churn.
- **Insights Report**: Generates a consolidated report with key insights from the analysis.

### Installation
To set up the development environment, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Customer-Behavior-Analytics.git
   cd Customer-Behavior-Analytics
   ```

2. Create and activate a virtual environment (optional, but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r config/requirements.txt
   ```

### Usage
To run the complete analysis, execute the main script:

```bash
python3 src/customer_analytics.py
```

- If you have your own customer data in CSV format, place it in `src/data/customer_data.csv`. The script will use this data. Otherwise, synthetic data will be automatically generated.
- An interactive dashboard (`docs/customer_behavior_dashboard.html`) will be generated in the `docs/` folder of the project.

### Project Structure
```
Customer-Behavior-Analytics/
├── config/
│   └── requirements.txt
├── docs/
│   ├── notebooks/
│   └── customer_behavior_dashboard.html (generated dashboard)
├── src/
│   ├── data/
│   │   └── customer_data.csv (optional, for your data)
│   └── customer_analytics.py
├── tests/
│   └── test_customer_analytics.py
├── .gitignore
└── README.md
```

### GitHub Pages
This project is configured to be published on GitHub Pages. The generated interactive dashboard (`customer_behavior_dashboard.html`) can be viewed directly via GitHub Pages. To activate, go to your repository settings on GitHub, select 'Pages' and configure the source to the `gh-pages` branch (or `main`/`master` with the `/docs` folder).

### Technologies Used
- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- Plotly

### License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

### Contribution
Contributions are welcome! Please follow these guidelines:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.
