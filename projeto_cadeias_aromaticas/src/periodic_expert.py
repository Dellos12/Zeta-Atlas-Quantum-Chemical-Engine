
import polars as pl
import os
import json
import sys
import re

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def parse_formula(formula):
    """Extrai a contagem de átomos da string (Ex: C5H5N -> {'C': 5, 'H': 5, 'N': 1})"""
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    return {el: (int(num) if num else 1) for el, num in matches}

def run():
    send_telemetry("Passo 0", 10, "⚛️ [Periodic Expert] Calculando Eletronegatividade e Heterociclo...")
    
    # 1. Captura o Contrato Blindado do Rails
    targets_raw = os.environ.get("ZETA_TARGETS", "{}")
    targets = json.loads(targets_raw)
    formula = targets.get("formula", "C6H6")
    rules = targets.get("atomic_rules", {})
    
    # 2. Análise Estequiométrica
    atom_counts = parse_formula(formula)
    n_c = atom_counts.get('C', 6)
    n_h = atom_counts.get('H', 6)
    
    # 3. CÁLCULO DE POLARIDADE (A Nova Face do Hiperplano)
    massa_total = 0
    en_acumulada = 0
    total_atomos = 0
    is_hetero = False

    for el, count in atom_counts.items():
        if el in rules:
            massa_total += rules[el]['mass'] * count
            en_acumulada += rules[el]['electronegativity'] * count
            total_atomos += count
            # Se houver algo além de C e H, é um fármaco potencial (Heterociclo)
            if el not in ['C', 'H']:
                is_hetero = True
        else:
            send_telemetry("Alerta", 0, f"⚠️ Elemento {el} fora da Tabela Periódica!")

    en_media = round(en_acumulada / total_atomos, 3) if total_atomos > 0 else 2.55

    # 4. LEI DE HIBRIDIZAÇÃO E POSICIONAMENTO DE ID
    hibridizacao = "sp2" if n_h <= n_c else "sp3"
    
    # Sufixo de ID: HET (Fármaco), SP2 (Aromático), SP3 (Saturado)
    if is_hetero:
        suffix = "HET"
    else:
        suffix = hibridizacao.upper()
    
    molecule_id = f"GEN_{formula}_{suffix}"

    # 5. CONSOLIDAÇÃO DO GENOMA (Bronze)
    config = {
        'molecule_id': molecule_id,
        'formula': formula,
        'n_carbonos': n_c,
        'massa_calculada': round(massa_total, 3),
        'eletronegatividade_media': en_media,
        'hibridizacao': hibridizacao,
        'is_hetero': 1 if is_hetero else 0,
        'target_gibbs': targets.get("target_gibbs", 10.0)
    }

    os.makedirs('data/bronze', exist_ok=True)
    # Salvamos via Polars-LTS para manter a velocidade industrial
    pl.DataFrame([config]).write_parquet('data/bronze/raw_atlas.parquet')
    
    send_telemetry("Passo 0", 100, f"✅ Hiperplano parametrizado para {formula}.", config)

if __name__ == "__main__":
    run()
