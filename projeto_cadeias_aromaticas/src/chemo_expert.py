import pandas as pd
import os, json, sys

def send_telemetry(step, progress, message, data=None):
    print(f"[TELEMETRY] {json.dumps({'step': step, 'progress': progress, 'message': message, 'data': data or {}})}")
    sys.stdout.flush()

def run():
    send_telemetry("Passo 2", 10, "🧪 [Chemo Expert] Extraindo Valência Pi via Pandas...")
    path_bronze = 'data/bronze/raw_atlas.parquet'
    if not os.path.exists(path_bronze): return
        
    df = pd.read_parquet(path_bronze)
    
    # Lógica de Hibridização via Pandas
    df['valencia_pi'] = df.apply(lambda x: float(x['n_carbonos']) if x['hibridizacao'] == 'sp2' else 0.0, axis=1)
    
    os.makedirs('data/silver/quantum', exist_ok=True)
    df.to_parquet('data/silver/quantum/chem_data.parquet', index=False)
    send_telemetry("Passo 2", 100, "✅ Valência Pi consolidada.")

if __name__ == "__main__": run()

