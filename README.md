# NYC Yellow Taxi Trip Data

Projeto de análise e dashboard de dados de viagens de táxi em Nova York, com foco em limpeza de dados, transformação ETL e visualização interativa em Streamlit.

## Visão Geral

Este projeto explora um dataset real de corridas de táxi de Nova York para demonstrar um fluxo simples de engenharia de dados:

- extração de dados brutos;
- validação e limpeza de inconsistências;
- criação de colunas analíticas;
- armazenamento em Parquet;
- análise exploratória;
- visualização em dashboard interativo.

O objetivo principal é transformar um conjunto de dados bruto em informações úteis para negócios, como desempenho por hora, receita por tipo de pagamento, variação por dia da semana e comportamento por fornecedor.

## Objetivo do Projeto

O projeto busca:

- entender a qualidade dos dados e seus problemas reais;
- aplicar regras de negócio para remover registros inconsistentes;
- construir uma camada analítica limpa reutilizável;
- apresentar métricas e tendências em um painel visual;
- exemplificar um pipeline ETL simples em Python.

## Stack Tecnológica

- Python
- Pandas
- Streamlit
- PyArrow
- Parquet
- Quarto / Jupyter (em apoio documental e análise)
- Git / GitHub

## Estrutura do Repositório

```text
NYC_Yellow_Taxi_Trip_Data/
├── assets/                     # imagens, diagramas e arquivos visuais
├── dashboard/
│   └── dashboard.py           # painel interativo em Streamlit
├── data/
│   ├── input/
│   │   └── yellow_tripdata_2016-03.csv
│   └── output/
│       └── yellow_tripdata_2016-03_cleaned.parquet
├── documents/
│   └── document_main.qmd      # documentação em Quarto/PDF
├── notebooks/
│   └── main.ipynb             # notebook de exploração e análise
├── LICENSE
├── README.md
└── .gitignore
```

## Dataset

O projeto utiliza o conjunto de dados NYC Yellow Taxi Trip Data, com a base correspondente ao mês de março de 2016.

Arquivo principal de entrada:

- `data/input/yellow_tripdata_2016-03.csv`

Arquivo processado e limpo gerado pelo pipeline:

- `data/output/yellow_tripdata_2016-03_cleaned.parquet`

## Fluxo do Pipeline

O processo do projeto segue a lógica de ETL:

![Desenho da Estrutura](assets/Desenho%20da%20Estrutura.png)

*Estrutura do projeto e fluxo principal: extração, transformação, carga e visualização.*

### 1. Extração
- leitura do CSV bruto com Pandas;
- carregamento de uma amostra ou subconjunto relevante para análise local.

### 2. Validação e limpeza
- identificação de colunas nulas;
- conversão de tipos de dados;
- validação de regras de negócio;
- remoção de registros inconsistentes, como:
  - distância zero ou anormal;
  - tarifas negativas;
  - passageiros fora do intervalo esperado;
  - duração de viagem inválida;
  - coordenadas fora do escopo geográfico.

### 3. Transformação
- cálculo de métricas derivadas, como:
  - `trip_duration_min`
  - `hour_of_day`
  - `day_of_week`
  - `trip_speed_mph`
  - `tip_pct`
  - `revenue_per_mile`

### 4. Carregamento
- salvamento da base tratada em formato Parquet para uso em análise e dashboard.

## Dashboard

O dashboard foi construído com Streamlit e disponibiliza filtros e indicadores sobre:

- viagens por hora;
- receita total;
- tarifa média;
- distância média;
- gorjeta média;
- análise por fornecedor;
- análise por tipo de pagamento;
- comparação por dia da semana.

### Mockup do Figma

![Figma](assets/Figma.png)

*Mockup inicial do dashboard desenvolvido no Figma.*

### Screenshots do dashboard

#### Hora

![Hora](assets/Hora.png)

#### Fornecedor

![Fornecedor](assets/Fornecedor.png)

#### Pagamento

![Pagamento](assets/Pagamento.png)

#### Dia da Semana

![Dia da Semana](assets/Dia%20da%20Semana.png)

Para rodar o painel:

O dashboard foi construído com Streamlit e disponibiliza filtros e indicadores sobre:

- viagens por hora;
- receita total;
- tarifa média;
- distância média;
- gorjeta média;
- análise por fornecedor;
- análise por tipo de pagamento;
- comparação por dia da semana.

Para rodar o painel:

```bash
cd dashboard
streamlit run dashboard.py
```

## Como Executar o Projeto

### Requisitos

- Python 3.10+
- pip
- ambiente virtual recomendado

### Criação do ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### Instalação das dependências

```bash
pip install pandas streamlit pyarrow
```

Se o projeto estiver usando outras bibliotecas no notebook ou na documentação, elas também podem ser instaladas conforme necessário.

### Rodando o dashboard

```bash
streamlit run dashboard/dashboard.py
```

## Análises Possíveis

Com os dados limpos, o projeto permite responder perguntas como:

- em quais horários há maior volume de corridas?
- qual é a média de tarifa por dia da semana?
- quais formas de pagamento predominam?
- qual fornecedor concentra mais viagens ou receita?
- como a gorjeta varia em relação ao valor da corrida?

## Documentação

Há também uma documentação em Quarto na pasta `documents/`, com uma visão mais formal do projeto e explicações do pipeline e dos resultados.

## Principais Arquivos

- `dashboard/dashboard.py`: painel interativo com visualizações em Streamlit
- `documents/document_main.qmd`: documento analítico e explicativo do projeto
- `notebooks/main.ipynb`: exploração e experimentos analíticos
- `data/output/yellow_tripdata_2016-03_cleaned.parquet`: base tratada pronta para uso

## Conclusão

Este projeto é uma aplicação prática de engenharia de dados em um contexto real, mostrando como dados brutos podem ser transformados em insight analítico e visualização de negócio. O conjunto combina limpeza, modelagem analítica, dashboard e documentação em um fluxo simples e didático, facilitando a compreensão do processo ETL.