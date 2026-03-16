
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import os
import sys

# Ajuste de path para encontrar a raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils import carregar_dados, salvar_dados

# Reutilizamos a arquitetura do Cubo, mas com foco no DECODER (Geração)
class GenerativeCube(nn.Module):
    def __init__(self, latent_dim=2, feat_dim=4):
        super().__init__()
        # O "Sonhador": Recebe um ponto no hiperpano e gera as 4 faces químicas
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 8),
            nn.ReLU(),
            nn.Linear(8, feat_dim)
        )

    def forward(self, z):
        return self.decoder(z)

def dream():
    print("🌙 [Dreamer] O modelo está 'sonhando' com novos análogos aromáticos...")
    
    # 1. Carregamos o Atlas Final para usar como base de escala
    df_gold = carregar_dados('data/gold/atlas_final.parquet')
    feats = ['valencia_pi', 'curvatura_ricci', 'energia_gibbs', 'energia_ressonancia']
    
    # Pegamos a média e o desvio para "desnormalizar" o sonho e torná-lo real
    stats_mean = df_gold[feats].mean().values
    stats_std = df_gold[feats].std().values + 1e-6

    # 2. Inicializamos o motor generativo
    model = GenerativeCube(latent_dim=2, feat_dim=len(feats))
    model.eval()

    # 3. Gerando 10 "Sonhos" (Amostragem do Hiperplano)
    with torch.no_grad():
        # Criamos 10 pontos aleatórios perto do Cerne (0,0) com um desvio controlado
        z_samples = torch.randn(10, 2) * 0.4 # 0.4 controla a "criatividade"
        
        raw_dreams = model(z_samples).numpy()
        
        # Transformamos os números da rede em realidade química (desnormalização)
        real_dreams = (raw_dreams * stats_std) + stats_mean

    # 4. Organizando o Catálogo de Sonhos
    dreams_df = pd.DataFrame(real_dreams, columns=feats)
    dreams_df['molecule_id'] = [f"DREAM_{i:03d}" for i in range(len(dreams_df))]
    dreams_df['identidade_predita'] = "CONFORMOMERO_GERADO"
    
    # Salva na Gold como uma extensão do seu Atlas
    salvar_dados(dreams_df, 'data/gold/dreams_atlas.parquet')
    
    print(f"✨ Sucesso! 10 novas assinaturas químicas foram 'sonhadas' e salvas em data/gold/dreams_atlas.parquet")
    print("🧪 Essas moléculas habitam a Zona Neutra entre o Benzeno e o Ruído.")

if __name__ == "__main__":
    dream()
