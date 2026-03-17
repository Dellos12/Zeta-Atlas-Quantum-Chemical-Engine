import pandas as pd
import os
import json
import sys

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def run():
    step_name = "Passo 5"
    send_telemetry(step_name, 10, "🌡️ [Thermal Expert] Calculando Estabilidade de Gibbs...")
    
    # 1. CARGA DA CAMADA ANTERIOR (Ressonância/Fase)
    path_res = 'data/silver/quantum/resonance_data.parquet'
    if not os.path.exists(path_res):
        send_telemetry("Erro", 0, "❌ Ruptura: Dados de Ressonância (Passo 4) não encontrados.")
        return
        
    # Usamos o Pandas para manter a flexibilidade dos tipos
    df = pd.read_parquet(path_res)
    
    # 2. LEI TÉRMICA DINÂMICA (A Face 4)
    # Base 10.0 + (Aumento por Carbono) + Penalidade por Tensão sp3
    def calc_gibbs(row):
        # Recuperamos o n_carbonos e a hibridização que o Periodic Expert injetou
        n_c = row.get('n_carbonos', 6)
        hib = row.get('hibridizacao', 'sp2')
        
        base_g = 10.0 + (n_c - 6) * 1.3
        penalidade = 5.0 if hib == 'sp3' else 0.0
        
        return round(base_g + penalidade, 2)

    # Injetamos a métrica no Hiperplano
    df['energia_gibbs'] = df.apply(calc_gibbs, axis=1)
    
    # 3. BLINDAGEM DE PASSAGEM (O SEGREDO DO CUBO)
    # Garantimos que a 'eletronegatividade_media' sobreviva para o Solubility Expert
    os.makedirs('data/silver/thermodynamics', exist_ok=True)
    
    # SALVAMENTO INTEGRAL: Não filtramos colunas, passamos o "Todo" adiante
    output_path = 'data/silver/thermodynamics/thermal_data.parquet'
    df.to_parquet(output_path, index=False)
    
    # Telemetria rica para o Rails
    gibbs_mean = df['energia_gibbs'].mean()
    send_telemetry(step_name, 100, "✅ Energia de Gibbs consolidada.", {
        "energia_gibbs": float(gibbs_mean),
        "n_carbonos": int(df['n_carbonos'].iloc[0]) if 'n_carbonos' in df.columns else 6
    })

if __name__ == "__main__":
    run()

