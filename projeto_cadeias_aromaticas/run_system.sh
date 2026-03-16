#!/bin/bash

# 1. AMBIENTE E HARDWARE (BLINDAGEM INTEL MKL)
echo "🚀 [CONDA] Ativando Ambiente e Alinhando Hardware..."
source ~/anaconda3/etc/profile.d/conda.sh
conda activate cadeias_aromaticas

# Prevenção do erro 'Illegal Instruction' e Otimização de CPU
export MKL_DEBUG_CPU_TYPE=5
export MKL_CBWR=COMPAT
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 2. LIMPEZA DE CAMPO (RESET DO HIPERPLANO)
echo "🧹 [RESET] Limpando memórias e resíduos..."
rm -rf data/silver/*
rm -rf data/gold/*

# 3. PIPELINE DA MATÉRIA (CONSTRUÇÃO DAS 4 FACES)
echo "🏗️  [MATÉRIA] Processando Especialistas Químicos e Geométricos..."
python src/ingestion.py        # Passo 1: Massa
python src/chemo_expert.py     # Passo 2: Carga
python src/geometry_engine.py  # Passo 3: Curvatura (Ricci)
python src/resonance_expert.py # Passo 4: Campo de Força
python src/thermal_expert.py   # Passo 5: Gibbs (Tensão)

# 4. FUSÃO E TREINAMENTO (REDE NEURAL VIVA)
echo "🧠 [PYTORCH] Fundindo as Faces e Calibrando a Incógnita Zeta..."
python src/models/train_gold_atlas.py # Passo 6: O Cerne

# 5. INDEXAÇÃO DE BIG DATA (MEMÓRIA LITERÁRIA)
echo "📚 [MEMÓRIA] Transformando Tratado Técnico em Tensores..."
python src/memory_expert.py    # Passo 7: Big Data Index

# 6. IGNIÇÃO DO SERVIDOR DE TELEMETRIA (gRPC) 📡
echo "🛰️  [gRPC] Ligando o Motor de Telemetria na porta 50051..."
# Rodamos em background para permitir que o script continue ou o usuário interaja
python src/models/telemetria_server.py &

# Pausa para o servidor Python estabilizar o gRPC
sleep 3

echo "-------------------------------------------------------"
echo "✨ [SUCESSO] MOTOR PYTHON OPERANDO VIA gRPC."
echo "Agora a Antena (Rails) pode captar o sinal do Hiperplano."
echo "-------------------------------------------------------"

# 7. MANTER O PROCESSO VIVO
# Se quiser rodar o Oráculo local para testes também:
# python src/models/oracle.py

# Finalização limpa: mata o servidor Python ao sair (Ctrl+C)
trap "kill 0" EXIT
wait

