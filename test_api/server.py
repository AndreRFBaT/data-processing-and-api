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
