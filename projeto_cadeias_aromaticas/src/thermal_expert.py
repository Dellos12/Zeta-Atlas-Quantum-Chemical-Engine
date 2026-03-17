
import pandas as pd
import os
import json
import sys
import numpy as np

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def get_rails_targets():
    """Lê os alvos industriais enviados pelo Rails via JSON."""
    try:
        targets_raw = os.environ.get("ZETA_TARGETS", "{}")
        return json.loads(targets_raw)
  # Se o Rails não enviar nada, usamos o Benzeno como padrão
    except:
        return {"target_gibbs": 10.0, "tolerance": 0.05}

def calculate_stability_delta(gibbs_real, target_gibbs):
    """Calcula o quão longe a molécula está do desejo industrial."""
    return abs(gibbs_real - target_gibbs)

def run():
    send_telemetry("Passo 5", 5, "🌡️ Iniciando Thermodynamics Engine (Modo Industrial)...")
    
    # 1. Carregamos as metas do Rails
    targets = get_rails_targets()
    target_g = targets.get('target_gibbs', 10.0) # Ponto Zero por padrão
    
    path_res = 'data/silver/quantum/resonance_data.parquet'
    if not os.path.exists(path_res):
        send_telemetry("Erro", 0, "❌ Falha: Dados de Ressonância não encontrados.")
        return
        
    df = pd.read_parquet(path_res)

    # 2. Física Dinâmica: Gibbs baseada na complexidade (Carbonos)
    # Simulamos o cálculo real de Gibbs aqui
    mapeamento_carbonos = {'AROM_001': 6, 'AROM_002': 10, 'AROM_003': 14, 'AROM_004': 14}
    df['n_carbonos'] = df['molecule_id'].map(mapeamento_carbonos)
    
    # Lei Térmica: G = 10 + (C-6) * 1.3
    df['energia_gibbs_real'] = 10.0 + (df['n_carbonos'] - 6) * 1.3

    # 3. O Diálogo Industrial: Comparação com o Alvo
    # Criamos o Delta de Estabilidade (O quanto a física obedece ao negócio)
    df['delta_estabilidade'] = df['energia_gibbs_real'].apply(lambda x: calculate_stability_delta(x, target_g))

    # 4. Classificação de Viabilidade Industrial
    df['viabilidade_industrial'] = df['delta_estabilidade'] < 2.0 # Tolerância de 2 kcal/mol
    
    os.makedirs('data/silver/thermodynamics', exist_ok=True)
    df.to_parquet('data/silver/thermodynamics/thermal_data.parquet', index=False)
    
    send_telemetry("Passo 5", 100, "✅ Termodinâmica Processada.", {
        "target_solicitado": target_g,
        "media_gibbs_real": df['energia_gibbs_real'].mean(),
        "viabilidade_count": int(df['viabilidade_industrial'].sum())
    })

if __name__ == "__main__":
    run()
