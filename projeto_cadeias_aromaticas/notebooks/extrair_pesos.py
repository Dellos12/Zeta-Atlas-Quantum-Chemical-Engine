
import torch
import pandas as pd
import numpy as np
import sys
import os

# Ajuste para encontrar o modelo no src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.train_gold_atlas import IdentityCubeNet

def interrogar():
    print("🔍 Interrogando os pesos do Cubo Mágico...")
    
    # 1. Carregar os nomes das features usadas
    features = ['valencia_pi', 'curvatura_ricci', 'energia_gibbs', 'energia_ressonancia']
    
    # 2. Instanciar o modelo (usamos as dimensões do nosso projeto: 4 IDs, 4 Features)
    model = IdentityCubeNet(num_molecules=4, feat_dim=4)
    
    # 3. Extrair Pesos da camada Linear (Faces do Cubo)
    # Pegamos os pesos que conectam as features à saída Zeta/Ruído
    weights = model.fc.weight.data.numpy()
    
    # A importância é a média absoluta da influência de cada feature nas 2 saídas
    importancia = np.abs(weights).mean(axis=0)[4:] # Pulamos os 4 pesos do Embedding
    
    df_pesos = pd.DataFrame({
        'Face_do_Cubo': features,
        'Influencia_no_Gradiente': importancia
    }).sort_values(by='Influencia_no_Gradiente', ascending=False)
    
    # Salva na pasta notebooks para fácil acesso
    df_pesos.to_csv('notebooks/importancia_faces.csv', index=False)
    
    print("\n⚖️  RESULTADO DO INTERROGATÓRIO:")
    print(df_pesos)
    print("\n✅ Pesos extraídos e salvos em: notebooks/importancia_faces.csv")

if __name__ == "__main__":
    interrogar()
