import os
from openai import OpenAI
from dotenv import load_dotenv
import json 

load_dotenv()

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key= os.getenv("OPENAI_API_KEY")

)






lista_de_resenha = []

with open("Resenhas_App_Chatgpt.txt", "r", encoding="utf-8") as resenhas_gpt:
    for linha in resenhas_gpt:
        lista_de_resenha.append(linha.strip().replace("$", " "))


lista_de_resenha_modificada = []

for indice, linha in enumerate(lista_de_resenha):
    resposta = client_openai.chat.completions.create(
    model="google/gemma-3-4b",
    messages=[
        {"role": "user",
        
         "content":f"""
        abaixo esta uma resenha bruta:

        \"\"\"{linha}\"\"\"

        separe as resenhas nas seguintes categoria:
        'usuario' - mostrando o id, que é o {indice}

        'resenha_original' - mostrando o texto original

        'resenha_pt' - o texto traduzido para português brasil
        
        'avaliacao' - Positiva; Negativa; Neutra

        exemplo:
        '34314135413213&Henrique Roberto$I like this product very much'

        exemplo de saida:
            {{
                "ID": '34314135413213',
                "usuario": "Henrique Roberto",
                "resenha_original": "I like this product very much",
                "resenha_pt": "Eu gostei muito desse produto",
                "avaliacao": "Positiva"
            }}
        
        regra essencial: TEM QUE SER EM FORMATO JSON
        """}
    ],
    temperature=0
)
    
    json_string = resposta.choices[0].message.content
    json_string =(json_string.replace("```json","").replace("```", ""))
    try:
        dict_convertido = json.loads(json_string)
        if isinstance(dict_convertido, list):
            lista_de_resenha_modificada.extend(dict_convertido)
        else:
            lista_de_resenha_modificada.append(dict_convertido)
    except json.JSONDecodeError:
        print("Erro ao converter JSON:", json_string)

print(lista_de_resenha_modificada)



def analisar_resenhas(lista_de_resenha_modificada):

    positiva = 0
    negativa = 0
    neutra = 0

    texto_final = ""

    for item in lista_de_resenha_modificada:

        avaliacao = item.get("avaliacao")

        if avaliacao == "Positiva":
            positiva += 1
        
        elif avaliacao == "Negativa":
            negativa += 1

        elif avaliacao == "Neutra":
            neutra += 1

        texto_final += item.get("resenha_pt", "") + " | "

    contagem = {
        "Positivas": positiva,
        "Negativas": negativa,
        "Neutras": neutra
    }

    texto_final = texto_final.rstrip(" | ")
    return contagem, texto_final

contagem, texto_unificado = analisar_resenhas(lista_de_resenha_modificada)

print("\nContagem de Sentimentos:")
print(contagem)
print("\nTexto Unificado")
print(texto_unificado)