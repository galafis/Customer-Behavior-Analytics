# Customer Behavior Analytics
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema avançado de análise de comportamento do cliente com funcionalidades abrangentes e stack tecnológico moderno. Oferece múltiplas linguagens de programação, interfaces web interativas, API RESTful completa e capacidades de análise avançadas para soluções de nível profissional.

## 🎯 Visão Geral

Este projeto demonstra a implementação de um sistema completo de análise de comportamento do cliente, integrando análise estatística em R, processamento de dados em Python, API RESTful com Flask e interface web moderna com JavaScript.

## ✨ Características

- **Processamento Avançado**: Algoritmos de alta performance para análise de dados
- **Análise em Tempo Real**: Visualização e processamento de dados ao vivo
- **API RESTful**: Endpoints completos para integração empresarial
- **Interface Interativa**: Web interface moderna e responsiva
- **Análise Estatística**: Modelagem estatística abrangente em R
- **Arquitetura Escalável**: Construída para performance empresarial
- **Configuração Profissional**: Setup pronto para produção

## 🛠️ Stack Tecnológico

### Backend
- **Python**: Processamento principal e APIs
- **Flask**: Endpoints RESTful completos
- **pandas/numpy**: Manipulação e análise de dados
- **SQLite**: Persistência de dados local

### Frontend
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Grid, Flexbox, animações responsivas
- **JavaScript (ES6+)**: Funcionalidades interativas

### Análise de Dados
- **R**: Modelagem estatística e visualização
- **ggplot2**: Gráficos avançados
- **dplyr**: Manipulação de dados
- **pandas/numpy**: Processamento de dados Python
- **scikit-learn**: Machine Learning

## 📁 Estrutura do Projeto

```
Customer-Behavior-Analytics/
├── 📁 data/                    # Dataset e arquivos de dados
│   └── customer_data.csv       # Dados de exemplo dos clientes
├── 📁 notebooks/               # Análise exploratória
│   ├── analise_exploratoria.ipynb
│   ├── dashboard_interativo.ipynb
│   └── modelo_comportamento.ipynb
├── 📄 server.py                # Servidor Flask com API RESTful
├── 📄 customer_analytics.py    # Scripts de análise Python
├── 📄 customer_analysis.R      # Análise estatística em R
├── 📄 analytics.R              # Funções auxiliares R
├── 📄 index.html              # Interface web principal
├── 📄 app.js                  # Lógica JavaScript
├── 📄 styles.css              # Estilos responsivos
├── 📄 requirements.txt        # Dependências Python
├── 📄 .env.example           # Configurações de ambiente
├── 📄 .gitignore             # Arquivos ignorados
├── 📄 LICENSE                # Licença MIT
└── 📄 README.md              # Documentação
```

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8+
- R 4.0+
- Navegador moderno

### 1. Clone o repositório
```bash
git clone https://github.com/galafis/Customer-Behavior-Analytics.git
cd Customer-Behavior-Analytics
```

### 2. Configuração de ambiente
```bash
# Copie o arquivo de configuração
cp .env.example .env

# Edite as configurações conforme necessário
nano .env  # ou seu editor preferido
```

### 3. Instale dependências Python
```bash
pip install -r requirements.txt
```

### 4. Execute o servidor Flask
```bash
# Desenvolvimento
python server.py

# Ou com variáveis de ambiente específicas
FLASK_ENV=development FLASK_DEBUG=true python server.py
```

### 5. Acesse a aplicação
- **Interface Web**: `http://localhost:5000`
- **API Endpoints**: `http://localhost:5000/api/`
- **Documentação da API**: `http://localhost:5000/`

## 📊 API Endpoints

### Informações Gerais
- `GET /` - Informações da API e lista de endpoints
- `GET /health` - Status de saúde da aplicação

### Clientes
- `GET /api/customers` - Lista todos os clientes
- `GET /api/customers/<id>` - Detalhes de um cliente específico
- **Parâmetros de filtro**: `?country=USA&category=Electronics`

### Analytics
- `GET /api/analytics/summary` - Resumo geral das análises
- `GET /api/analytics/demographics` - Análise demográfica
- `GET /api/analytics/purchases` - Comportamento de compras

### Exemplos de uso da API

```bash
# Obter todos os clientes
curl http://localhost:5000/api/customers

# Filtrar clientes por país
curl "http://localhost:5000/api/customers?country=USA"

# Obter resumo analytics
curl http://localhost:5000/api/analytics/summary

# Verificar saúde da aplicação
curl http://localhost:5000/health
```

## 🔬 Análises Disponíveis

### Python Analytics (`customer_analytics.py`)
- Segmentação de clientes
- Análise de comportamento de compra
- Detecção de padrões
- Métricas de engajamento

### R Analytics (`customer_analysis.R`)
- Modelagem estatística
- Análise de correlação
- Testes de hipóteses
- Visualizações avançadas

### Jupyter Notebooks
- Análise exploratória interativa
- Dashboard em tempo real
- Modelagem de comportamento

## ⚙️ Configuração Avançada

### Variáveis de Ambiente (.env)

O arquivo `.env.example` contém todas as configurações disponíveis:

```bash
# Configurações básicas
FLASK_ENV=development
FLASK_DEBUG=true
PORT=5000

# Banco de dados (se necessário)
# DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Recursos avançados
ENABLE_REAL_TIME_ANALYTICS=true
API_RATE_LIMIT=1000
CACHE_DEFAULT_TIMEOUT=300
```

### Configuração para Produção

```bash
# Configurações de produção no .env
FLASK_ENV=production
FLASK_DEBUG=false
SECURE_HEADERS_ENABLED=true
HTTPS_REDIRECT=true
WORKERS=4
```

## 📱 Interface Responsiva

A interface web é totalmente responsiva com:
- **Mobile-First Design**: Otimizada para dispositivos móveis
- **Grid Layout**: Layout flexível e adaptável
- **Interatividade**: Elementos interativos modernos
- **Performance**: Carregamento rápido e eficiente

## 🔧 Extensões Possíveis

- [ ] Integração com APIs de CRM
- [ ] Análise de sentimento em tempo real
- [ ] Machine Learning avançado
- [ ] Dashboards personalizáveis
- [ ] Alertas automáticos
- [ ] Integração com bancos de dados externos
- [ ] Autenticação e autorização
- [ ] Cache distribuído com Redis
- [ ] Processamento assíncrono

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaAnalise`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova análise'`)
4. Push para a branch (`git push origin feature/NovaAnalise`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- Email: gabrieldemetrios@gmail.com
- LinkedIn: [Gabriel Demetrios Lafis](https://www.linkedin.com/in/gabriel-demetrios-lafis-62197711b)

---
⭐ Se este projeto foi útil, considere deixar uma estrela!
