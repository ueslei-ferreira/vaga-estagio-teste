# Projeto: Download , estruturação, exportação e consulta de dados.

Esta pasta contém 3 códigos para processamento de arquivos CSV, para download dos arquivos, estruturação e inserção em Banco de dados e consultas aos dados inseridos, os dados foram armazenados usando PostgreSQL.

### Configuração do Banco de Dados

Antes de executar os scripts 2 e 3, é necessário criar o banco de dados no PostgreSQL. Siga os passos abaixo:

1. Acesse o PostgreSQL usando o terminal ou uma ferramenta de gerenciamento, como pgAdmin.
2. Execute o seguinte comando para criar o banco de dados:

```sql
CREATE DATABASE "seu_banco";
```

3. Certifique-se de que as credenciais no script (`dbname`, `user`, `password`, `host`, `port`) correspondem às configurações do seu PostgreSQL.
4. Após criar o banco de dados, execute os scripts normalmente.

### Uso

1. Navegue até a pasta:

```bash
cd teste_3
```

2. Certifique-se de instalar as dependências antes de executar o script:

```bash
pip install -r requirements.txt
```

3. Execução:

Execute o script para download dos dados com o seguinte comando:

```bash
python baixa_csvs.py
```

Execute o script para estruturação das tabelas e inserção dos dados, com o seguinte comando:

```bash
python estruturar_dados.py
```

Execute o script para as consultas dos dados com o seguinte comando:

```bash
python consultas.py
```

Estrutura do Projeto :

```bash
    teste_1/
    ├── baixa_csvs.py          # Script 1
    ├── estruturar_dados.py    # Script 2
    ├── consultas.py           # Script 3
    ├── README.md              # Documentação do projeto
    └── requirements.txt       # Dependências do projeto
```