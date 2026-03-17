
import pandas as pd
import os, json, sys

def run():
    print("[TELEMETRY] " + json.dumps({"step": "Passo 3", "progress": 10, "message": "📐 Mapeando Curvatura de Ricci..."}))
    df = pd.read_parquet('data/silver/quantum/chem_data.parquet')
    
    # Ricci Reativo: sp2 (0.15) vs sp3 (0.85)
    df['curvatura_ricci'] = df['hibridizacao'].map({'sp2': 0.15, 'sp3': 0.85}).fillna(0.50)
    
    os.makedirs('data/silver/geometry', exist_ok=True)
    df.to_parquet('data/silver/geometry/geo_data.parquet', index=False)
    print("[TELEMETRY] " + json.dumps({"step": "Passo 3", "progress": 100, "message": "✅ Geometria mapeada.", "data": {"curvatura_ricci": df['curvatura_ricci'].mean()}}))

if __name__ == "__main__": run()
