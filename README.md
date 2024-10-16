# Gestão de Insumos Agrícolas

## Descrição do Projeto

Este projeto tem como objetivo desenvolver um sistema de **Gestão de Insumos Agrícolas**, facilitando o controle de estoque, previsão de uso e geração de relatórios detalhados. O sistema foi criado com foco na automação de tarefas comuns do setor agrícola, como o gerenciamento de insumos e fornecedores, além de permitir a exportação e importação de dados em formato JSON.

![Demonstração do Sistema](./docs/example.gif)

### Funcionalidades Principais

- **Gerenciamento de Insumos**: Cadastre, visualize, edite e exclua insumos com controle de quantidade e fornecedor.
- **Gerenciamento de Fornecedores**: Cadastre, edite e visualize fornecedores.
- **Previsão de Uso de Insumos**: Estime o uso futuro dos insumos com base nos últimos 30 dias de histórico, levando em consideração a taxa de crescimento e a taxa de perdas.
- **Geração de Relatórios**: Relatórios detalhados de uso de insumos por tipo, fornecedor, mês e dia.
- **Exportação e Importação de Dados**: Importação de dados via arquivos JSON e exportação dos dados em formato JSON para análise externa.
- **Navegação entre Páginas**: Navegação simples entre as páginas de gerenciamento de insumos e fornecedores.

## Estrutura do Projeto

O projeto foi desenvolvido em Python utilizando o framework **Tkinter** para a interface gráfica e o banco de dados **Oracle** para a persistência dos dados. A aplicação está dividida em módulos que organizam as funcionalidades da seguinte forma:

```bash
.
├── main.py                 # Configuração da interface principal e navegação
├── common.py               # Funções auxiliares (UUID, timestamp, JSON, etc.)
├── database.py             # Funções de conexão e interação com o banco de dados Oracle (CRUD)
├── supply_page.py          # Interface de gerenciamento de insumos
├── supplier_page.py        # Interface de gerenciamento de fornecedores
├── predict_usage_modal.py  # Modal para previsão de uso de insumos
├── usage_report_modal.py   # Modal para geração de relatórios de uso de insumos
├── docker-compose.yml      # Configuração do Docker para subir o banco de dados Oracle
├── oracle-db/initdb.sql    # Script SQL para criação das tabelas no Oracle
├── requirements.txt        # Dependências do projeto
├── example_supplier_data.json # Dados fictícios de fornecedores para teste
└── example_supply_data.json   # Dados fictícios de insumos para teste
```

> **Nota**: Os arquivos `example_supplier_data.json` e `example_supply_data.json` contêm dados fictícios para testes. **É necessário importar o `example_supplier_data.json` antes de usar o `example_supply_data.json`.**

## Requisitos Técnicos

Para rodar o projeto, você precisará das seguintes ferramentas:

- **Docker**: Para executar o banco de dados Oracle via Docker.
- **Python 3.x**: Linguagem principal do projeto.
- **Tkinter**: Para a interface gráfica.
- **Bibliotecas Python**: Listadas no `requirements.txt`. Incluem o módulo `oracledb` para a conexão com o banco Oracle.

### Instalação das Dependências

1. **Instalar dependências Python**:

```bash
pip install -r requirements.txt
```

2. **Subir o banco de dados Oracle com Docker**:

```bash
docker-compose up -d
```

3. **Criar as tabelas no banco de dados (caso não sejam criadas automaticamente)**:

```bash
docker exec -it oracledatabase bash -c "sqlplus dbuser/dbpass@localhost:1521/eis @/opt/oracle/scripts/setup/initdb.sql"
```

4. **Rodar a aplicação**:

```bash
python main.py
```

## Funcionalidades do Sistema

### 1. **Gerenciamento de Insumos**

- Acesse a aba "Supplies" no menu principal.
- Preencha o tipo, nome, quantidade e fornecedor para registrar um novo insumo.
- Os dados de insumos cadastrados são exibidos em uma tabela.
- Você pode editar, exportar ou importar insumos da base de dados.

### 2. **Gerenciamento de Fornecedores**

- Acesse a aba "Suppliers" no menu principal.
- Preencha o nome e email do fornecedor para registrar um novo fornecedor.
- Os fornecedores cadastrados são exibidos em uma tabela.
- Você pode atualizar os dados de fornecedores e exportá-los ou importá-los de arquivos JSON.

### 3. **Previsão de Uso de Insumos**

- Na aba "Supplies", clique em "Predict Supply Usage" para abrir o modal de previsão.
- Insira as **taxas de crescimento** e **taxas de perdas** (em porcentagem) para prever o uso futuro de insumos.
- A previsão é baseada nos últimos 30 dias de uso e estima o consumo para os próximos 30 dias.

### 4. **Relatórios de Uso de Insumos**

- Clique em "Generate Usage Report" para visualizar relatórios detalhados de uso de insumos.
- Relatórios disponíveis:
  - **Relatório por Tipo**: Exibe o total de insumos utilizados por tipo (ex: sementes, fertilizantes).
  - **Relatório por Insumo**: Mostra o total utilizado de cada insumo específico.
  - **Relatório por Fornecedor**: Detalha o total de insumos fornecidos por cada fornecedor.
  - **Relatório por Mês**: Exibe o uso total de insumos por mês (últimos 3 meses).
  - **Relatório por Dia (Último Mês)**: Mostra o uso diário de insumos nos últimos 30 dias.
- Relatórios podem ser exportados em formato JSON para análise externa.

### 5. **Exportação e Importação de Dados**

- Exporte os dados de insumos e fornecedores em formato JSON.
- Importe dados de insumos e fornecedores de arquivos JSON utilizando a interface.

### 6. **Navegação entre Páginas**

- Use o menu no topo da interface para alternar entre as páginas de gerenciamento de insumos ("Supply") e de fornecedores ("Supplier").

## Estruturas de Dados

### Tabelas no Banco de Dados (Oracle)

1. **Tabela `supplier`**:
   - `id`: UUID (chave primária)
   - `name`: Nome do fornecedor
   - `email`: Email do fornecedor
   - `created_at`: Data de criação
   - `deleted_at`: Campo para soft delete

2. **Tabela `supply`**:
   - `id`: UUID (chave primária)
   - `name`: Nome do insumo
   - `quantity`: Quantidade em estoque
   - `type`: Tipo de insumo (ex: Fertilizantes, Sementes)
   - `supplier_id`: Chave estrangeira para a tabela `supplier`
   - `created_at`: Data de criação
   - `deleted_at`: Campo para soft delete

### Consistência dos Dados

Para garantir a integridade dos dados inseridos, o sistema valida os seguintes campos:

- Email: Validado utilizando uma regex para garantir que o formato está correto.
- Quantidade: Apenas números inteiros são permitidos no campo de quantidade.
- Campos obrigatórios: Todos os campos devem ser preenchidos antes de adicionar ou salvar insumos e fornecedores.
