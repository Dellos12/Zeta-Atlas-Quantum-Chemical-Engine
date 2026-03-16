# src/resonance_expert.py
import pandas as pd
import os

def run():
    print("🌐 [Passo 4] Parametrizando Campo de Ressonância (Estabilidade de Fase)...")
    
    # Carrega a métrica geométrica do Passo 3
    path_geo = 'data/silver/geometry/geo_data.parquet'
    if not os.path.exists(path_geo):
        print("❌ Erro: Execute o Passo 3 primeiro.")
        return
        
    df = pd.read_parquet(path_geo)
    
    # Energia de Ressonância (kcal/mol) - A 'vontade' da molécula em permanecer aromática
    # Benzeno(36), Naftaleno(72), Antraceno(108), Fenantreno(106.5)
    ressonancias = {
        'AROM_001': 36.0, 
        'AROM_002': 72.0, 
        'AROM_003': 108.0, 
        'AROM_004': 106.5  # Perda de fase por assimetria
    }
    
    df['energia_ressonancia'] = df['molecule_id'].map(ressonancias)
    
    # Salvamos na pasta de quantum (Silver) para consolidar os dados moleculares
    os.makedirs('data/silver/quantum', exist_ok=True)
    df.to_parquet('data/silver/quantum/resonance_data.parquet', index=False)
    print(f"✅ Campo de Ressonância parametrizado em data/silver/quantum/resonance_data.parquet")

if __name__ == "__main__":
    run()


