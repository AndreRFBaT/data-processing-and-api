<script setup>
import { ref } from "vue";
import axios from "axios";

const nome = ref("");
const operadoras = ref([]);
const mensagemErro = ref("");

const buscarOperadoras = async () => {
  if (!nome.value.trim()) {
    operadoras.value = [];
    mensagemErro.value = "Por favor, insira um nome para buscar.";
    return;
  }
  mensagemErro.value = "";  // Resetando a mensagem de erro
  try {
    const response = await axios.get(`http://127.0.0.1:8000/buscar?nome=${nome.value}`);
    operadoras.value = response.data;
    if (operadoras.value.length === 0) {
      mensagemErro.value = "Nenhuma operadora encontrada.";
    }
  } catch (error) {
    // Verificando se o erro é causado por uma falta de resultado (404)
    if (error.response && error.response.status === 404) {
      mensagemErro.value = "Nenhuma operadora encontrada com o nome fornecido.";
    } else {
      // Se ocorrer um erro diferente, exiba uma mensagem genérica
      mensagemErro.value = "Erro ao buscar operadoras. Tente novamente mais tarde.";
    }
  }
};

const handleKeyPress = (event) => {
  if (event.key === "Enter") {
    buscarOperadoras();
  }
};
</script>

<template>
  <div class="container">
    <h2>Buscar Operadoras</h2>
    <input v-model="nome" @keyup.enter="buscarOperadoras" placeholder="Digite o nome da operadora..." />
    <button @click="buscarOperadoras">Buscar</button>

    <!-- Exibindo mensagens de erro -->
    <p v-if="mensagemErro" class="erro">{{ mensagemErro }}</p>

    <!-- Exibindo lista de operadoras -->
    <ul v-if="operadoras.length && nome.trim()">
      <li v-for="operadora in operadoras" :key="operadora.cnpj" class="operadora-item">
        <strong>Razão Social:</strong> {{ operadora.razao_social }} <br />
        <template v-if="operadora.nome_fantasia">
          <strong>Nome Fantasia:</strong> {{ operadora.nome_fantasia }} <br />
        </template>
        <strong>CNPJ:</strong> {{ operadora.cnpj }} <br />
        <strong>Registro ANS:</strong> {{ operadora.registro_ans }} <br />
        <strong>Modalidade:</strong> {{ operadora.modalidade }} <br />
        <strong>UF:</strong> {{ operadora.uf }} <br />
        <strong>Município:</strong> {{ operadora.cidade }} <br />
        <strong>Email:</strong> {{ operadora.endereco_eletronico }} <br />
        <strong>DDD:</strong> {{ operadora.ddd }} <br />
        <strong>Telefone:</strong> {{ operadora.telefone }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
input {
  padding: 8px;
  width: 80%;
  margin-bottom: 10px;
}
button {
  padding: 8px;
  cursor: pointer;
}
.erro {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
.operadora-item {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 15px;
}
</style>
