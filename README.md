# Análise de Comportamento do Cliente

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![R](https://img.shields.io/badge/R-4.1%2B-blue?style=for-the-badge&logo=r)
![scikit-learn](https://img.shields.io/badge/scikit--learn-v1.3-orange?style=for-the-badge&logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-v2.0-red?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-v5.15-purple?style=for-the-badge&logo=plotly)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Ativo-brightgreen?style=for-the-badge&logo=github)

## Visão Geral

Este repositório apresenta um projeto de **Análise de Comportamento do Cliente** desenvolvido por Gabriel Demetrios Lafis. O objetivo é demonstrar a aplicação de técnicas de ciência de dados para entender padrões de compra, segmentar clientes e prever o churn, utilizando Python e R para análise e visualização.

O projeto inclui:

*   **Análise Exploratória de Dados (EDA)**: Compreensão profunda dos dados do cliente.
*   **Segmentação de Clientes**: Utilizando algoritmos de clustering (K-Means) para identificar grupos de clientes com comportamentos semelhantes.
*   **Análise RFM (Recência, Frequência, Valor Monetário)**: Uma técnica poderosa para segmentar clientes com base em seu histórico de transações.
*   **Previsão de Churn**: Construção de modelos de Machine Learning para prever quais clientes têm maior probabilidade de deixar o serviço.
*   **Visualizações Interativas**: Dashboards criados com Plotly para explorar os insights de forma dinâmica.
*   **Documentação Bilíngue**: READMEs completos em Português e Inglês.

## Estrutura do Projeto

A estrutura do repositório é organizada para facilitar a navegação e compreensão:

```
Customer-Behavior-Analytics/
├── docs/                       # Documentação adicional e notebooks
│   └── notebooks/
│       └── Exploratory_Customer_Analysis.ipynb
├── public/                     # Arquivos estáticos para GitHub Pages
│   ├── index.html
│   └── styles.css
├── src/                        # Código fonte do projeto
│   ├── data/                   # Dados (sintéticos ou reais)
│   │   └── customer_data.csv
│   ├── customer_analytics.py   # Script principal de análise em Python
│   ├── analytics.R             # Script de análise em R
│   ├── customer_analysis.R     # Script de análise em R (detalhado)
│   ├── app.js                  # Lógica JavaScript para frontend
│   └── server.py               # Servidor Flask para API (se aplicável)
├── tests/                      # Testes unitários
│   └── test_customer_analytics.py
├── .gitignore                  # Arquivos e pastas a serem ignorados pelo Git
├── LICENSE                     # Licença do projeto
├── README.md                   # Este arquivo (Português)
├── README_en.md                # README em Inglês
└── requirements.txt            # Dependências Python
```

## Arquitetura do Sistema

O diagrama abaixo ilustra a arquitetura geral do projeto:

```mermaid
graph TD
    A[Dados Brutos] --> B(Pré-processamento de Dados)
    B --> C{Análise de Comportamento do Cliente}
    C --> D[Segmentação RFM]
    C --> E[Segmentação K-Means]
    C --> F[Previsão de Churn]
    D --> G[Insights de Segmentos]
    E --> G
    F --> G
    G --> H[Visualizações Interativas]
    H --> I[Dashboard Web (GitHub Pages)]
    subgraph Ferramentas
        B -- Python/Pandas --> B
        C -- Python/scikit-learn, R/dplyr --> C
        H -- Plotly/R/ggplot2 --> H
    end
```

## Como Usar

### Pré-requisitos

Certifique-se de ter Python 3.9+ e R 4.1+ instalados em seu sistema. As dependências Python são listadas em `requirements.txt`.

### Instalação

1.  **Clonar o repositório:**

    ```bash
    git clone https://github.com/galafis/Customer-Behavior-Analytics.git
    cd Customer-Behavior-Analytics
    ```

2.  **Instalar dependências Python:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Instalar dependências R (se for usar os scripts R):**

    Abra o console R e execute:

    ```R
    install.packages(c("dplyr", "ggplot2", "cluster", "factoextra", "corrplot", "randomForest", "caret", "plotly", "DT", "shiny", "shinydashboard"), repos="http://cran.us.r-project.org")
    ```

### Execução

#### Análise Python

Para executar a análise de comportamento do cliente em Python e gerar o dashboard HTML:

```bash
python src/customer_analytics.py
```

O dashboard interativo será salvo como `customer_behavior_dashboard.html` na raiz do projeto.

#### Análise R

Para executar a análise de comportamento do cliente em R:

```bash
Rscript src/customer_analysis.R
```

Ou interativamente no console R:

```R
source("src/customer_analysis.R")
results <- run_customer_analysis()
```

## Testes

Para executar os testes unitários do projeto Python:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m unittest tests/test_customer_analytics.py
```

## GitHub Pages

Uma demonstração interativa do dashboard gerado pelo script Python está disponível via GitHub Pages [aqui](https://galafis.github.io/Customer-Behavior-Analytics/).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

**Gabriel Demetrios Lafis**

*   [GitHub](https://github.com/galafis)
*   [LinkedIn](https://www.linkedin.com/in/gabriel-demetrios-lafis/)

---
