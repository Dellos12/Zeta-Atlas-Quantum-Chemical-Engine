# src/memory_expert.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import sys

def run():
    print("🧠 [Passo 7] Indexando Memória da Matéria (Big Data Mode)...")
    
    # Motor de Linguagem Natural
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    caminho_txt = 'data/bronze/memoria_materia.txt'
    if not os.path.exists(caminho_txt):
        print("❌ Erro: Crie o arquivo data/bronze/memoria_materia.txt primeiro.")
        return

    # Lê o tratado técnico
    with open(caminho_txt, 'r', encoding='utf-8') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
    
    # Gera os vetores semânticos (O 'Seno' da Linguagem)
    embeddings = model.encode(linhas)
    
    # Cria o dataframe de memória indexada
    df_memoria = pd.DataFrame({
        'contexto': linhas,
        'vetor': list(embeddings)
    })
    
    # Salvamos na prata (Silver) como um objeto serializado (PKL)
    os.makedirs('data/silver', exist_ok=True)
    df_memoria.to_pickle('data/silver/memoria_indexada.pkl')
    print(f"✅ Memória de {len(linhas)} sentenças integrada ao Hiperplano.")

if __name__ == "__main__":
    run()

