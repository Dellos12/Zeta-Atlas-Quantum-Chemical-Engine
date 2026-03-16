
# src/chemo_expert.py
import pandas as pd
import os

def run():
    print("🧪 [Passo 2] Extraindo Valência Pi (Carga Quântica)...")
    
    # Carrega a massa gerada no Passo 1
    path_bronze = 'data/bronze/raw_atlas.parquet'
    if not os.path.exists(path_bronze):
        print("❌ Erro: Execute o Passo 1 primeiro.")
        return
        
    df = pd.read_parquet(path_bronze)
    
    # Atribuição da Regra de Hückel (Elétrons Pi deslocalizados)
    # Benzeno(6), Naftaleno(10), Antraceno(14), Fenantreno(14)
    valencias = {
        'AROM_001': 6.0, 
        'AROM_002': 10.0, 
        'AROM_003': 14.0, 
        'AROM_004': 14.0
    }
    
    df['valencia_pi'] = df['molecule_id'].map(valencias)
    
    # Salvamos na prata (Silver) para o próximo especialista
    os.makedirs('data/silver/quantum', exist_ok=True)
    df.to_parquet('data/silver/quantum/chem_data.parquet', index=False)
    print(f"✅ Valência Pi extraída e salva em data/silver/quantum/chem_data.parquet")

if __name__ == "__main__":
    run()
