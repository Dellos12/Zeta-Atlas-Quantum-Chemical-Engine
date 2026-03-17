import pandas as pd
import os
import json
import sys

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def run():
    send_telemetry("Passo 3", 10, "📐 [Geometry Engine] Analisando Curvatura de Campo...")
    
    # 1. Carrega os dados processados pelo Periodic Expert e Chemo Expert
    path_silver_chem = 'data/silver/quantum/chem_data.parquet'
    if not os.path.exists(path_silver_chem):
        send_telemetry("Erro", 0, "❌ Falha: Dados quânticos (Passo 2) ausentes.")
        return
        
    df = pd.read_parquet(path_silver_chem)
    
    # 2. LÓGICA DE REATIVIDADE GEOMÉTRICA (A Blindagem)
    # Em vez de dicionário fixo, usamos a hibridização vinda do Passo 0
    def calcular_curvatura(row):
        hibridizacao = row.get('hibridizacao', 'sp2')
        
        if hibridizacao == 'sp2':
            # Geometria Plana (Benzeno/Aromáticos) -> Ricci baixo
            return 0.15 
        elif hibridizacao == 'sp3':
            # Geometria Tetraédrica (Ciclohexano/Saturados) -> Ricci alto (não-euclidiano)
            return 0.85
        else:
            return 0.50 # Estado de transição ou erro

    # 3. Aplica a Lei Geométrica no Hiperplano
    df['curvatura_ricci'] = df.apply(calcular_curvatura, axis=1)
    
    # 4. Consolidação na Camada Silver
    os.makedirs('data/silver/geometry', exist_ok=True)
    df.to_parquet('data/silver/geometry/geo_data.parquet', index=False)
    
    send_telemetry("Passo 3", 100, "✅ Curvatura de Ricci mapeada conforme hibridização.", {
        "media_ricci": df['curvatura_ricci'].mean()
    })

if __name__ == "__main__":
    run()

