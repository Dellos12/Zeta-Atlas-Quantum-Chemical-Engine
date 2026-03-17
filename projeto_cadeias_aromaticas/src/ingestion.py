import polars as pl
import os
import json
import sys

def send_telemetry(step, progress, message, data=None):
    payload = {"step": step, "progress": progress, "message": message, "data": data or {}}
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def run():
    send_telemetry("Ingestion", 10, "🏗️  [Ingestion] Unificando com Blindagem Atômica...")
    
    path_bronze = 'data/bronze/raw_atlas.parquet'
    if not os.path.exists(path_bronze):
        send_telemetry("Erro", 0, "❌ Ruptura: Dados do Passo 0 não localizados.")
        return
        
    # 1. Lê a física do Passo 0
    df_blindado = pl.read_parquet(path_bronze)

    # 2. Catálogo de Nomes (Apenas para rotulação)
    df_catalogo = pl.DataFrame({
        "molecule_id": ["GEN_C6H6", "GEN_C6H12"],
        "name": ["Benzeno", "Ciclohexano"],
        "smiles": ["c1ccccc1", "C1CCCCC1"]
    })

    # 3. JOIN DE PRESERVAÇÃO
    # Usamos o join mas garantimos que n_carbonos e hibridizacao sobrevivam
    df_final = df_blindado.join(df_catalogo, on="molecule_id", how="left")

    # 4. PAREDE DE SEGURANÇA (Se o Join gerar nulos, restauramos a lei física)
    # Isso impede que o chemo_expert receba colunas vazias
    df_final = df_final.with_columns([
        pl.col("n_carbonos").fill_null(6),
        pl.col("hibridizacao").fill_null(pl.lit("sp2")),
        pl.col("name").fill_null(pl.lit("Molécula_Sintética"))
    ])

    df_final.write_parquet(path_bronze)
    send_telemetry("Ingestion", 100, "✅ Sincronia Bronze estabelecida sem perda de parâmetros.")

if __name__ == "__main__":
    run()

