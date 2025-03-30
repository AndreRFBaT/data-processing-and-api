# Tarefa de criação de APIs e servidor.

## Execução do arquivo `server.py`*

* Execução do servidor com o comando `uvicorn server:app --reload`*

![alt text](/test_api/imagens_api/image.png)

* Execução da API utilizando Vue.js com o comando `npm run dev`*

![alt text](/test_api/imagens_api/image-1.png)

* Swagger com o link `http://127.0.0.1:8000/docs`*

![alt text](/test_api/imagens_api/image-2.png)

* API executando localmente

![alt text](/test_api/imagens_api/image-3.png)

### Testes de fazer consultas:

* Busca por nome da operadora por razão social:

![alt text](/test_api/imagens_api/image-4.png)

* Busca por nome fantasia da operadora:

![alt text](/test_api/imagens_api/image-5.png)

* Busca contendo caracteres especiais:

![alt text](/test_api/imagens_api/image-6.png)

* Busca por números:

![alt text](/test_api/imagens_api/image-7.png)

* Busca por letras aleatórias:

![alt text](/test_api/imagens_api/image-8.png)

* Busca inexistente:

![alt text](/test_api/imagens_api/image-9.png)

* Busca vazia:

![alt text](/test_api/imagens_api/image-10.png)
---


# Script utilizando JavaScript para fazer as consultas:

```javascript
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
```

---

# Script utilizando Python para o servidor:

```python
# acesso ao swagger
# http://127.0.0.1:8000/docs
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Configuração do FastAPI
app = FastAPI(
    title="Operadoras de Saúde",
    description="Busca operadoras de saúde no CSV",
    version="1.0"
)

# Configuração do CORS correta
app.add_middleware(
    CORSMiddleware,
    # Permite qualquer origem (ou restrinja para "http://localhost:5173")
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar os dados do CSV
df_operadoras = pd.read_csv("operadoras.csv", encoding="utf-8", delimiter=";")

# Endpoint de busca
df_operadoras = df_operadoras.fillna('')

# Endpoint de busca
@app.get("/buscar")
async def buscar_operadoras(nome: str = Query(..., description="Nome da operadora")):
    """Busca operadoras de saúde pelo nome ou nome fantasia.

    Este endpoint permite buscar operadoras de saúde com base no nome fornecido.
    Ele retorna uma lista de operadoras que contêm o nome fornecido em sua razão
    social ou nome fantasia.

    Args:
        nome (str): Nome da operadora a ser buscado.

    Returns:
        list: Uma lista de dicionários contendo informações essenciais das operadoras
              encontradas, incluindo razão social, nome fantasia, CNPJ, registro ANS,
              modalidade, UF, cidade, endereço eletrônico, DDD e telefone.

    Raises:
        HTTPException: Se o nome não for fornecido ou se nenhuma operadora for encontrada
                       com o nome fornecido.
    """

    if not nome.strip():
        raise HTTPException(status_code=400, detail="Por favor, insira um nome para buscar.")
    # Filtrar as operadoras pelo nome ou nome fantasia
    resultados = df_operadoras[
        df_operadoras["razao_social"].str.contains(nome, case=False, na=False, regex=False) |
        df_operadoras["nome_fantasia"].str.contains(nome, case=False, na=False, regex=False)
    ]

    # Verificar se não encontrou resultados
    if resultados.empty:
        raise HTTPException(status_code=404, detail="Nenhuma operadora encontrada com o nome fornecido.")

    # Pegando as colunas essenciais
    colunas_desejadas = [
        "razao_social", "nome_fantasia", "cnpj", "registro_ans",
        "modalidade", "uf", "cidade",
        "endereco_eletronico", "ddd", "telefone"
    ]

    # Garantindo que todas as colunas existem no DataFrame antes de retornar
    colunas_existentes = [col for col in colunas_desejadas if col in df_operadoras.columns]
    resultados_essenciais = resultados[colunas_existentes]

    return resultados_essenciais.to_dict(orient="records")

# Iniciar o servidor corretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```