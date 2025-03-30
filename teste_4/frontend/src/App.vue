<template>
  <div id="app">
    <h1>Busca de Operadoras</h1>
    <div class="search-container">
      <input v-model="termo" placeholder="Digite CNPJ, Razão Social ou Nome Fantasia" :disabled="carregando" />
      <button @click="buscar" :disabled="carregando || !termo.trim()">
        {{ carregando ? 'Buscando...' : 'Buscar' }}
      </button>
    </div>

    <!-- Carregando -->
    <div v-if="carregando" class="loading">
      <p>Carregando resultados...</p>
    </div>

    <!-- Resultados -->
    <ul v-else-if="resultados.length">
      <li v-for="(item, index) in resultados" :key="index">
        <div v-for="(value, key) in item" :key="key">
          <strong>{{ key.replace(/_/g, ' ') }}:</strong> {{ value || 'N/A' }}
        </div>
        <hr>
      </li>
    </ul>

    <!-- Nenhum resultado -->
    <p v-else-if="!carregando && termo.trim()">
      Nenhum resultado encontrado
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  /**
   * Componente Vue para buscar e exibir registros de operadoras.
   * 
   * Data:
   * - termo: Termo de busca inserido pelo usuário.
   * - resultados: Lista de registros retornados pelo backend.
   * - carregando: Indica se a busca está em andamento.
   * 
   * Métodos:
   * - cleanItem: Limpa valores inválidos dos registros retornados.
   * - buscar: Realiza a busca no backend e processa os resultados.
   */
  data() {
    return {
      termo: '', // Termo de busca inserido pelo usuário
      resultados: [], // Lista de resultados retornados pelo backend
      carregando: false // Indica se a busca está em andamento
    };
  },
  methods: {
    /**
     * Limpa valores inválidos de um item retornado pelo backend.
     * 
     * Substitui valores nulos, indefinidos ou NaN por 'N/A'.
     * 
     * @param {Object} item - Objeto representando um registro.
     * @returns {Object} - Objeto com valores inválidos substituídos.
     */
    cleanItem(item) {
      const cleaned = {};
      for (const [key, value] of Object.entries(item)) {
        if (value !== null && value !== undefined && value !== 'NaN' && !Number.isNaN(value)) {
          cleaned[key] = value;
        } else {
          cleaned[key] = 'N/A';
        }
      }
      return cleaned;
    },

    /**
     * Realiza a busca no backend com base no termo inserido pelo usuário.
     * 
     * Envia uma requisição GET para o endpoint '/busca' e processa os resultados.
     * Exibe mensagens de erro no console em caso de falha.
     */
    async buscar() {
      this.carregando = true; // Indica que a busca está em andamento
      this.resultados = []; // Limpa os resultados anteriores

      try {
        console.log("Enviando requisição para:", 'http://localhost:5000/busca?q=' + this.termo);

        const response = await axios.get('http://localhost:5000/busca', {
          params: { q: this.termo }
        });

        console.log("Resposta do servidor:", response.data);

        if (Array.isArray(response.data)) {
          this.resultados = response.data.map(this.cleanItem); // Limpa os valores inválidos
        } else {
          console.error("Resposta inesperada do servidor:", response.data);
        }
      } catch (error) {
        console.error("Erro detalhado:", error.response ? error.response.data : error.message);
      } finally {
        this.carregando = false; // Indica que a busca foi concluída
      }
    }
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin: 50px;
}

input {
  padding: 8px;
  width: 300px;
}

button {
  padding: 8px 20px;
  margin-left: 10px;
}

ul {
  list-style: none;
  padding: 0;
  text-align: left;
  margin-top: 20px;
}

li {
  padding: 15px;
  border-bottom: 1px solid #ddd;
}

/* Container da busca */
.search-container {
  margin-bottom: 20px;
}

/* Mensagem de carregamento */
.loading {
  margin: 20px 0;
  padding: 15px;
  background: #f0f0f0;
  border-radius: 4px;
  font-style: italic;
}

/* Desabilita inputs durante carregamento */
input:disabled,
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>