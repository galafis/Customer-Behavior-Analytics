# Customer Behavior Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema profissional para análise de comportamento do cliente com pipeline integrado em Python e R, API/visualização e estrutura pronta para expansão (API, notebooks, dashboards).

- Repositório: Customer-Behavior-Analytics
- Dataset prioritário: data/customer_data.csv (real)
- Fallback: dataset sintético gerado on-the-fly quando o real não estiver disponível

## Sumário
- Visão Geral
- Estrutura do Repositório
- Pré-requisitos
- Dataset e Prioridade de Fonte
- Como Executar (Python e R)
- Fluxo de Fallback Sintético
- Geração de Insights e Visualizações
- Exemplos de Entrada/Saída
- Boas Práticas e Padrões do Pipeline
- Roadmap (API, notebooks, etc.)
- Contribuição
- Licença

## Visão Geral
Este projeto implementa um pipeline de analytics de clientes com:
- Ingestão e limpeza do CSV real (data/customer_data.csv) como fonte padrão
- Análises exploratórias e estatísticas (Python e R)
- Geração de métricas e insights acionáveis
- Visualizações salvas em ./outputs/ (PNG/HTML)
- Fallback para dados sintéticos quando o CSV real não está presente

## Estrutura do Repositório
```
.
├── data/
│   └── customer_data.csv          # dataset real (prioritário)
├── scripts/
│   └── customer_analysis.R        # análise em R (usa CSV real por padrão)
├── customer_analytics.py          # análise em Python (usa CSV real por padrão)
├── outputs/                       # gráficos, relatórios, artefatos
├── README.md
└── requirements.txt (se aplicável)
```

OBS: Ajuste caminhos conforme sua organização local. Os scripts assumem raiz do projeto ao serem executados.

## Pré-requisitos
- Python 3.9+ (recomendado 3.10/3.11)
- R 4.1+
- Bibliotecas Python: ver requirements.txt (ex.: pandas, numpy, matplotlib/seaborn, scikit-learn, flask opcional)
- Pacotes R: tidyverse, readr, dplyr, ggplot2 (ajuste conforme o script)

Instalação (Python):
- pip install -r requirements.txt

## Dataset e Prioridade de Fonte
- Fonte padrão: data/customer_data.csv
- Variáveis de ambiente/CLI permitem apontar para outro CSV, mas por padrão os scripts tentam carregar o real primeiro
- Se o arquivo real não existir ou falhar, ativa-se automaticamente o fluxo de fallback com dados sintéticos para fins de demonstração/validação

## Como Executar

### Python: customer_analytics.py
Uso básico (usa o CSV real por padrão):
```
python customer_analytics.py
```
Com argumentos explícitos:
```
python customer_analytics.py --input data/customer_data.csv --output_dir outputs --no-show
```
Parâmetros comuns:
- --input: caminho para o CSV (padrão: data/customer_data.csv)
- --output_dir: pasta de saída para gráficos/relatórios (padrão: outputs)
- --no-show: não abrir janelas de plot (headless)
- --seed: semente para reprodutibilidade
- --fallback: forçar uso de dados sintéticos (sobrepõe CSV real)

Comportamento:
1) Tenta carregar data/customer_data.csv
2) Se indisponível, gera dataset sintético consistente (esquema compatível)
3) Executa limpeza, EDA, estatísticas e salva resultados em outputs/
4) Retorna sumário/insights no console e salva artefatos

### R: scripts/customer_analysis.R
Uso básico (usa o CSV real por padrão):
```
Rscript scripts/customer_analysis.R
```
Com argumentos explícitos:
```
Rscript scripts/customer_analysis.R --input data/customer_data.csv --output_dir outputs --no-view
```
Parâmetros comuns:
- --input: caminho para o CSV (padrão: data/customer_data.csv)
- --output_dir: pasta de saída (padrão: outputs)
- --no-view: não abrir dispositivos gráficos
- --seed: semente para reprodutibilidade
- --fallback: forçar dados sintéticos

## Fluxo de Fallback Sintético
- Gera um dataset com colunas equivalentes ao esquema esperado (ex.: customer_id, age, gender, tenure, churn, revenue, segments, etc.)
- Tamanhos e distribuições configuráveis via seed/parâmetros
- Indicadores/artefatos marcados como synthetic_* em metadados/logs para rastreabilidade

## Geração de Insights e Visualizações
- Métricas: churn rate, LTV aproximado, ARPU, distribuição por segmento, coortes simples
- Visualizações: histogramas, boxplots, barras por segmento, heatmaps de correlação
- Saída padrão: arquivos salvos em outputs/ com nomes como:
  - outputs/eda_summary.txt
  - outputs/correlation_heatmap.png
  - outputs/segment_distribution.png
  - outputs/churn_by_segment.png

## Exemplos de Entrada/Saída
Entrada (CSV real, cabeçalho esperado mínimo):
```
customer_id,age,gender,tenure,revenue,churn,segment
1001,34,F,12,129.9,0,Gold
1002,45,M,5,89.0,1,Silver
```
Saídas esperadas:
- Console: resumo descritivo, taxas agregadas, alertas de qualidade
- Arquivos em outputs/: gráficos PNG e relatório TXT conforme seção anterior

## Boas Práticas e Padrões do Pipeline
- Separação clara de módulos (ingestão, preparo, modelagem/estatísticas, visualização)
- Logs e mensagens claras sobre qual fonte foi usada (real vs sintética)
- Parametrização via CLI e seeds para reprodutibilidade
- Estrutura de diretórios estável (data/, outputs/, scripts/)
- Tratamento de erros e mensagens amigáveis (ex.: instruir a criar data/customer_data.csv)
- Compatibilidade headless (CI/CD) com flags --no-show/--no-view

## Integração entre Módulos
- Python e R podem operar de forma independente sobre o mesmo CSV real
- Artefatos em outputs/ são compartilháveis entre linguagens
- Possível integração via arquivos intermediários (parquet/csv) e convenções de nomes

## Roadmap e Possibilidades Futuras
- API Flask para servir métricas e gráficos (endpoint /health, /metrics, /segments)
- Notebooks (Jupyter/Quarto) para análises ad hoc no diretório notebooks/
- Dockerfile para padronização de ambiente e execução única
- CI (GitHub Actions) para lint/test/execução headless dos scripts
- Camadas de modelagem (propensão a churn, clusterização de segmentos)

## Dicas de Execução
- Garanta que data/customer_data.csv exista para usar dados reais
- Crie a pasta outputs/ (os scripts podem criar automaticamente)
- Use --fallback para validações rápidas sem dados reais
- Defina --seed para reproduzir resultados

## Contribuição
Contribuições são bem-vindas! Abra uma issue ou envie um PR com melhorias (documentação, código, visualizações, exemplos de dados, testes).

## Licença
MIT. Veja o arquivo LICENSE se presente, ou inclua um conforme necessário.
