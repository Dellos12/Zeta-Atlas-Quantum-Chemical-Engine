
# src/thermal_expert.py
import pandas as pd
import os

def run():
    print("🌡️  [Passo 5] Calculando Energia de Gibbs (Estabilidade Térmica)...")
    
    # Carrega os dados consolidados do Passo 4
    path_res = 'data/silver/quantum/resonance_data.parquet'
    if not os.path.exists(path_res):
        print("❌ Erro: Execute o Passo 4 primeiro.")
        return
        
    df = pd.read_parquet(path_res)
    
    # Energia Livre de Gibbs (Valores simulados de Estabilidade de Formação)
    # Quanto maior o valor, maior a "tensão" para manter a estrutura coesa
    termica = {
        'AROM_001': 10.0, # Benzeno (Estável/Frio)
        'AROM_002': 15.2, # Naftaleno
        'AROM_003': 18.5, # Antraceno
        'AROM_004': 22.1  # Fenantreno (Alta Tensão Térmica)
    }
    
    df['energia_gibbs'] = df['molecule_id'].map(termica)
    
    # Salvamos na pasta de thermodynamics (Silver)
    # Agora temos as 4 FACES: Valência, Ricci, Ressonância e Gibbs.
    os.makedirs('data/silver/thermodynamics', exist_ok=True)
    df.to_parquet('data/silver/thermodynamics/thermal_data.parquet', index=False)
    print(f"✅ Energia de Gibbs mapeada em data/silver/thermodynamics/thermal_data.parquet")

if __name__ == "__main__":
    run()
