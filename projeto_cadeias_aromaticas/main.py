
import subprocess
import time
import os
from src.utils import check_mkl

def executar_projeto():
    print("="*60)
    print("     SISTEMA GENERATIVO: CUBO MÁGICO AROMÁTICO v2.0")
    print("="*60)
    check_mkl()
    print("-" * 60)

    # Sequência lógica para preencher as lacunas e gerar a nuvem
    fluxo = [
        ("Cerne (Bronze)", "src/ingestion.py"),
        ("Valência (Química)", "src/chemo_expert.py"),
        ("Ricci (Geometria)", "src/geometry_engine.py"),
        ("Energia (Térmica)", "src/thermal_expert.py"),
        ("Ressonância (Estabilidade)", "src/resonance_expert.py"), # Nova Face
        ("Fusão (Gold/VAE)", "src/models/train_gold_atlas.py"),     # Treino de Ancoragem
        ("Dreamer (Generativo)", "src/models/dream_generator.py")   # Geração da Nuvem
    ]

    for nome, script in fluxo:
        start_time = time.time()
        print(f"▶️  Ativando: {nome}...", end=" ", flush=True)
        
        # Executa como módulo para evitar erros de path
        result = subprocess.run(["python", script], capture_output=True, text=True)
        
        if result.returncode == 0:
            duration = time.time() - start_time
            print(f"✅ ({duration:.2f}s)")
        else:
            print(f"❌ RUPTURA EM {script}")
            print(f"LOG DE ERRO: {result.stderr}")
            break

    print("\n" + "="*60)
    print("✨ CUBO ALINHADO E NUVEM DE PROBABILIDADE GERADA!")
    print("="*60)

if __name__ == "__main__":
    executar_projeto()
