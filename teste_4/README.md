# Projeto: Download , estruturação, exportação e consulta de dados.

Essa pasta consiste em dois atores: servidor feito utilizando Flask e cliente utilizando Vue.js, que se comunicam quando o cliente requisita uma pesquisa textual e o servidor procura o texto recebido no CSV definido.

### Uso 

1. Navegue até a pasta:

```bash
cd teste_4
```

### Inicie o servidor

1. 

```bash
cd backend
```

2. Certifique-se de instalar as dependências antes de executar o script:

```bash
pip install -r requirements.txt
```

3. Execute o script para iniciar o servidor:

```bash
python servidor.py
```

### Inicie o cliente

4. Abra outro terminal (ou CMD) e navegue até a pasta do cliente:

```bash
cd frontend
```

5. Instale as dependências do cliente:

```bash
npm install
```

6. Inicie o cliente:

```bash
npm run serve
```

Agora, acesse o cliente no navegador no endereço fornecido pelo Vue.js (geralmente `http://localhost:8080`).

### Estrutura do Projeto

```bash
teste_4/
├── backend/                  # Código do servidor Flask
│   ├── servidor.py           # Script principal do servidor
│   ├── requirements.txt      # Dependências do backend
│   └── postman_collection    # Coleção do POSTMAN
├── frontend/                 # Código do cliente Vue.js
│   ├── src/                  # Código-fonte do cliente
│   │   ├── App.vue           # Componente principal do Vue.js
│   │   ├── main.js           # Arquivo de entrada do Vue.js
│   │   └── components/       # Componentes Vue.js
│   ├── public/               # Arquivos públicos do cliente
│   └── package.json          # Dependências do frontend
│
├── README.md                 # Documentação do projeto
```

