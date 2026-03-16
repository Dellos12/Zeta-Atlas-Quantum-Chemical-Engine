import pandas as pd
import os
from utils import send_telemetry

def run():
    send_telemetry("Ingestion", 10, "Iniciando consolidação do Catálogo...")
    
    catalogo = [
        {'molecule_id': 'AROM_001', 'name': 'Benzeno', 'smiles': 'c1ccccc1'},
        {'molecule_id': 'AROM_002', 'name': 'Naftaleno', 'smiles': 'c1ccc2ccccc2c1'},
        {'molecule_id': 'AROM_003', 'name': 'Antraceno', 'smiles': 'c1ccc2cc3ccccc3cc2c1'},
        {'molecule_id': 'AROM_004', 'name': 'Fenantreno', 'smiles': 'c1ccc2c(c1)ccc3ccccc32'}
    ]
    
    os.makedirs('data/bronze', exist_ok=True)
    df = pd.DataFrame(catalogo)
    df.to_parquet('data/bronze/raw_atlas.parquet', index=False)
    
    send_telemetry("Ingestion", 100, "✅ Massa Crítica Pronta e Ancorada.")

if __name__ == "__main__": 
    run()



