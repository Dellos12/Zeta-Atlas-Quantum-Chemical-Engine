import pandas as pd
import os
import json
import sys
import re

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def parse_formula(formula):
    """Extrai contagem de átomos: C6H6 -> {'C': 6, 'H': 6}"""
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    return {el: (int(num) if num else 1) for el, num in matches}

def run():
    send_telemetry("Passo 0", 10, "⚛️ [Periodic Expert] Sincronizando Leis do Rails...")
    
    # 1. Captura o Contrato (Blindagem vinda do Rails)
    targets_raw = os.environ.get("ZETA_TARGETS", "{}")
    targets = json.loads(targets_raw)
    
    formula = targets.get("formula", "C6H6")
    atomic_rules = targets.get("atomic_rules", {}) # Tabela Periódica do Rails
    
    # 2. Cálculo de Massa e Valência Baseado na Lei do Rails
    atom_counts = parse_formula(formula)
    massa_total = 0
    valencia_total = 0
    
    for el, count in atom_counts.items():
        if el in atomic_rules:
            massa_total += atomic_rules[el]['mass'] * count
            valencia_total += atomic_rules[el]['valence_electrons'] * count
        else:
            send_telemetry("Alerta", 0, f"⚠️ Elemento {el} não blindado na tabela!")

    # 3. Definição da Hibridização (Regra de Decisão do Hiperplano)
    # Se a proporção C/H permitir anel (como C6H6), blindamos como sp2
    hibridizacao = "sp2" if atom_counts.get('C', 0) == atom_counts.get('H', 0) else "sp3"

    config = {
        'molecule_id': f"GEN_{formula}",
        'formula': formula,
        'massa_calculada': round(massa_total, 3),
        'valencia_disponivel': valencia_total,
        'hibridizacao': hibridizacao,
        'target_gibbs': targets.get("target_gibbs", 10.0)
    }

    # 4. Consolidação da Blindagem (Bronze)
    os.makedirs('data/bronze', exist_ok=True)
    pd.DataFrame([config]).to_parquet('data/bronze/raw_atlas.parquet', index=False)
    
    send_telemetry("Passo 0", 100, f"✅ Hiperplano blindado para {formula}.", config)

if __name__ == "__main__":
    run()

