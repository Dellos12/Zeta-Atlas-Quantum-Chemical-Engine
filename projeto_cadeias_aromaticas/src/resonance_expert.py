
import pandas as pd
import os, json

def run():
    print("[TELEMETRY] " + json.dumps({"step": "Passo 4", "progress": 10, "message": "🌐 Parametrizando Ressonância..."}))
    df = pd.read_parquet('data/silver/geometry/geo_data.parquet')
    
    # Lei de Fase: 6.0 kcal/mol por elétron Pi no estado sp2
    df['energia_ressonancia'] = df.apply(lambda x: x['valencia_pi'] * 6.0 if x['hibridizacao'] == 'sp2' else 0.0, axis=1)
    
    os.makedirs('data/silver/quantum', exist_ok=True)
    df.to_parquet('data/silver/quantum/resonance_data.parquet', index=False)
    print("[TELEMETRY] " + json.dumps({"step": "Passo 4", "progress": 100, "message": "✅ Campo de Ressonância estabilizado."}))

if __name__ == "__main__": run()
