
import pandas as pd
import os
import json
import sys

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def run():
    step_name = "Passo 5.5"
    send_telemetry(step_name, 10, "💧 [Solubility Expert] Calculando LogP (Afinidade Hídrica)...")
    
    # 1. LOCALIZAÇÃO DA CAMADA (Onde o Cubo parou)
    path_thermal = 'data/silver/thermodynamics/thermal_data.parquet'
    
    if not os.path.exists(path_thermal):
        send_telemetry("Erro", 0, f"❌ Ruptura: Dados termodinâmicos não encontrados.")
        return
        
    # 2. CARGA VIA PANDAS (Recuperação de Parâmetros)
    df = pd.read_parquet(path_thermal)

    # 3. RECUPERAÇÃO DA BLINDAGEM (Eletronegatividade do Passo 0)
    # Se a coluna sumiu no caminho, usamos 2.55 (Carbono) como Ponto Zero
    if 'eletronegatividade_media' in df.columns:
        en_media = df['eletronegatividade_media'].iloc[0]
    else:
        en_media = 2.55 # Fallback de estabilidade
        send_telemetry("Aviso", 50, "⚠️ Parâmetro EN não herdado. Usando Ponto Zero (2.55).")

    # 4. LEI DA SOLUBILIDADE INDUSTRIAL (LogP)
    # Regra: Quanto maior a polaridade (Nitrogênio), menor o LogP (Mais solúvel)
    # Benzeno (EN 2.55) -> LogP 2.1 | Piridina (EN 2.62) -> LogP ~ 0.6
    log_p = round(2.1 - (en_media - 2.55) * 21.5, 2)
    
    # Injeta a 6ª Face no DataFrame
    df['log_p'] = log_p

    # 5. CONSOLIDAÇÃO (Atualiza a Prata/Silver para o Gold Atlas)
    # Salvamos o DF inteiro para não perder os "tijolos" das faces anteriores
    df.to_parquet(path_thermal, index=False)
    
    send_telemetry(step_name, 100, "✅ Solubilidade LogP ancorada no Hiperplano.", {
        "log_p": log_p,
        "en_referencia": en_media
    })

if __name__ == "__main__":
    run()
