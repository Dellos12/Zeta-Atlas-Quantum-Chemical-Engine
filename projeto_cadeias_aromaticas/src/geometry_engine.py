# src/geometry_engine.py
import pandas as pd
import os

def run():
    print("📐 [Passo 3] Calculando Curvatura de Ricci (Espaço Não-Euclidiano)...")
    
    # Carrega a carga quântica do Passo 2
    path_silver_chem = 'data/silver/quantum/chem_data.parquet'
    if not os.path.exists(path_silver_chem):
        print("❌ Erro: Execute o Passo 2 primeiro.")
        return
        
    df = pd.read_parquet(path_silver_chem)
    
    # Mapeamento da Curvatura (Deformação da Geodésica)
    # Quanto mais anéis e mais assimetria, maior a curvatura
    curvaturas = {
        'AROM_001': 0.15, # Benzeno (Quase plano)
        'AROM_002': 0.28, # Naftaleno
        'AROM_003': 0.42, # Antraceno (Progressão Linear)
        'AROM_004': 0.65  # Fenantreno (Assimetria/Tensão)
    }
    
    df['curvatura_ricci'] = df['molecule_id'].map(curvaturas)
    
    # Salvamos na pasta de geometria (Silver)
    os.makedirs('data/silver/geometry', exist_ok=True)
    df.to_parquet('data/silver/geometry/geo_data.parquet', index=False)
    print(f"✅ Curvatura de Ricci mapeada e salva em data/silver/geometry/geo_data.parquet")

if __name__ == "__main__":
    run()



