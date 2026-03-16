# Customer Behavior Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Tidyverse](https://img.shields.io/badge/Tidyverse-276DC3?style=for-the-badge&logo=r&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![License-MIT](https://img.shields.io/badge/License--MIT-yellow?style=for-the-badge)


[English](#english) | [Portugues](#portugues)

---

## Portugues

### Visao Geral

Projeto de analise de comportamento de clientes usando Python e R. Realiza segmentacao de clientes via KMeans (analise RFM — Recency, Frequency, Monetary), previsao de churn com Random Forest, e gera dashboards interativos com Plotly. Inclui uma API REST minima em Flask para consultar dados de clientes.

### Arquitetura

```mermaid
graph TB
    subgraph Python["Python - Analise Principal"]
        CA[customer_analytics.py<br/>Segmentacao RFM + Churn]
        SRV[server.py<br/>API REST Flask]
    end

    subgraph R["R - Analise Estatistica"]
        CR[customer_analysis.R<br/>Segmentacao + Modelagem]
    end

    subgraph Dados["Dados"]
        CSV[customer_data.csv<br/>ou dados sinteticos]
    end

    subgraph Saida["Saida"]
        DASH[Dashboard HTML<br/>Plotly interativo]
        API[API JSON<br/>Endpoints REST]
    end

    CSV --> CA
    CSV --> SRV
    CSV --> CR
    CA --> DASH
    SRV --> API
    CR --> DASH

    style Python fill:#e1f5fe
    style R fill:#f3e5f5
    style Dados fill:#fff3e0
    style Saida fill:#e8f5e9
```

### Funcionalidades

- **Segmentacao RFM**: Agrupa clientes por recencia, frequencia e valor monetario usando KMeans
- **Previsao de Churn**: Modelo Random Forest para identificar clientes em risco de abandono
- **Dashboard Interativo**: Graficos 3D, barras, pizza e boxplots via Plotly (salvo como HTML)
- **API REST**: Endpoints Flask para consulta de clientes, demografias e resumo de compras
- **Analise em R**: Script alternativo com segmentacao hierarquica, RFM scoring e visualizacoes ggplot2
- **Dados Sinteticos**: Gera dados automaticamente quando nao ha CSV real disponivel

### Estrutura do Projeto

```
Customer-Behavior-Analytics/
├── src/
│   ├── __init__.py
│   ├── customer_analytics.py   # Classe principal: RFM, KMeans, churn, dashboard
│   ├── customer_analysis.R     # Analise estatistica em R
│   └── server.py               # API REST Flask
├── tests/
│   └── test_customer_analytics.py
├── config/
│   └── requirements.txt
├── data/                       # Diretorio para dados CSV (gitignored)
├── LICENSE
└── README.md
```

### Como Executar

```bash
# Clonar o repositorio
git clone https://github.com/galafis/Customer-Behavior-Analytics.git
cd Customer-Behavior-Analytics

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r config/requirements.txt

# Executar analise completa (gera dashboard HTML)
python -m src.customer_analytics

# Executar API REST
python -m src.server
```

### Testes

```bash
python -m pytest tests/ -v
```

### Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python | Linguagem principal |
| pandas / NumPy | Processamento de dados |
| scikit-learn | KMeans, Random Forest, metricas |
| Plotly | Dashboards interativos |
| Flask | API REST |
| R | Analise estatistica alternativa |

---

## English

### Overview

Customer behavior analytics project using Python and R. Performs customer segmentation via KMeans (RFM analysis — Recency, Frequency, Monetary), churn prediction with Random Forest, and generates interactive dashboards with Plotly. Includes a minimal Flask REST API for querying customer data.

### Architecture

```mermaid
graph TB
    subgraph Python["Python - Main Analysis"]
        CA[customer_analytics.py<br/>RFM Segmentation + Churn]
        SRV[server.py<br/>Flask REST API]
    end

    subgraph R["R - Statistical Analysis"]
        CR[customer_analysis.R<br/>Segmentation + Modeling]
    end

    subgraph Data["Data"]
        CSV[customer_data.csv<br/>or synthetic data]
    end

    subgraph Output["Output"]
        DASH[HTML Dashboard<br/>Interactive Plotly]
        API[JSON API<br/>REST Endpoints]
    end

    CSV --> CA
    CSV --> SRV
    CSV --> CR
    CA --> DASH
    SRV --> API
    CR --> DASH

    style Python fill:#e1f5fe
    style R fill:#f3e5f5
    style Data fill:#fff3e0
    style Output fill:#e8f5e9
```

### Features

- **RFM Segmentation**: Groups customers by recency, frequency and monetary value using KMeans
- **Churn Prediction**: Random Forest model to identify customers at risk of leaving
- **Interactive Dashboard**: 3D scatter, bar, pie and box plots via Plotly (saved as HTML)
- **REST API**: Flask endpoints for querying customers, demographics and purchase summaries
- **R Analysis**: Alternative script with hierarchical clustering, RFM scoring and ggplot2 visualizations
- **Synthetic Data**: Automatically generates data when no real CSV is available

### Project Structure

```
Customer-Behavior-Analytics/
├── src/
│   ├── __init__.py
│   ├── customer_analytics.py   # Main class: RFM, KMeans, churn, dashboard
│   ├── customer_analysis.R     # Statistical analysis in R
│   └── server.py               # Flask REST API
├── tests/
│   └── test_customer_analytics.py
├── config/
│   └── requirements.txt
├── data/                       # Directory for CSV data (gitignored)
├── LICENSE
└── README.md
```

### How to Run

```bash
# Clone the repository
git clone https://github.com/galafis/Customer-Behavior-Analytics.git
cd Customer-Behavior-Analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r config/requirements.txt

# Run full analysis (generates HTML dashboard)
python -m src.customer_analytics

# Run REST API
python -m src.server
```

### Tests

```bash
python -m pytest tests/ -v
```

### Technologies

| Technology | Usage |
|------------|-------|
| Python | Primary language |
| pandas / NumPy | Data processing |
| scikit-learn | KMeans, Random Forest, metrics |
| Plotly | Interactive dashboards |
| Flask | REST API |
| R | Alternative statistical analysis |

---

### Autor / Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

### Licenca / License

MIT License - veja [LICENSE](LICENSE) para detalhes / see [LICENSE](LICENSE) for details.
