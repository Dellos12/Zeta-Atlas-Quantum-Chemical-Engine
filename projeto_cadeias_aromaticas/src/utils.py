import pandas as pd
import os
import torch
import sys
import json

def send_telemetry(step, progress, message, data=None):
    """Envia progresso em tempo real para o Rails."""
    payload = {
        "step": step,
        "progress": progress,
        "message": message,
        "data": data or {}
    }
    print(f"[TELEMETRY] {json.dumps(payload)}")
    sys.stdout.flush()

def carregar_dados(caminho):
    if not os.path.exists(caminho):
        send_telemetry("Error", 0, f"Arquivo não encontrado: {caminho}")
        raise FileNotFoundError(f"⚠️ {caminho}")
    return pd.read_parquet(caminho, engine='pyarrow')

def salvar_dados(df, caminho):
    diretorio = os.path.dirname(caminho)
    os.makedirs(diretorio, exist_ok=True)
    df.to_parquet(caminho, engine='pyarrow', index=False)

def check_mkl():
    mkl_disponivel = torch.backends.mkl.is_available()
    send_telemetry("Hardware", 100, "MKL Check", {"mkl": mkl_disponivel, "torch": torch.__version__})
    return mkl_disponivel


