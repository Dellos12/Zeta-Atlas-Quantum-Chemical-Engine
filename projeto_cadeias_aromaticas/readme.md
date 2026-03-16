
# 1. Criação do Cerne (ID 0 = Benzeno)
# Garante a ancoragem fixa para o treinamento do PyTorch.
python src/ingestion.py

# 2. Parametrização Quântica (Valência Pi)
# Define a densidade eletrônica real via RDKit.
python src/chemo_expert.py

# 3. Mapeamento Topológico (Curvatura de Ricci)
# Define a forma geométrica e conectividade.
python src/geometry_engine.py

# 4. Cálculo de Estabilidade (Energia de Gibbs)
# Define a tensão térmica e o gradiente de ruptura.
python src/thermal_expert.py

# 5. Preenchimento de Lacunas (Energia de Ressonância)
# Adiciona a face que evita a ruptura em anéis fundidos (Naftaleno/Antraceno).
python src/resonance_expert.py

# 6. Fusão e Treinamento do Motor Generativo (Gold/Zeta)
# O PyTorch calibra o Benzeno no Ponto Zero (MKL/Intel).
python src/models/train_gold_atlas.py

# 7. Geração da Nuvem (O Modelo "Sonha" com Análogos)
# Cria as assinaturas que preenchem as lacunas de literatura.
python src/models/dream_generator.py

# 8. Interrogatório Lógico (Extração de Pesos)
# Salva a 'importancia_faces.csv' para auditoria no Notebook.
python notebooks/extrair_pesos.py

# 9. EXPORTAÇÃO PARA C++ (O NOVO PASSO CRÍTICO) 🚀
# Converte Parquet -> CSV e PyTorch -> ONNX dentro de IA/menbrana_IA/bin/data/
python src/utils/export_to_cpp.py


# 🧬 Zeta-Atlas: Quantum Chemical Engine

O **Zeta-Atlas** é um ecossistema de simbiose tecnológica que une a agilidade do **Ruby on Rails 8** com a precisão da **Química Computacional em Python**. O projeto mapeia a estabilidade de cadeias aromáticas através de um pipeline de 7 passos, ancorando a física no "Ponto Zero" (Benzeno).

## 🚀 Arquitetura do Sistema
O projeto opera em um modelo de **Data Lakehouse** (Bronze -> Silver -> Gold):

1. **Rails Core (Ruby 3.3.10):** Maestro responsável pela orquestração de processos, monitoramento de telemetria e armazenamento vetorial (pgvector).
2. **Quantum Experts (Python/Conda):** Módulos especializados que calculam a física molecular:
   - **Chemo Expert:** Valência Pi (Regra de Hückel).
   - **Geometry Engine:** Curvatura de Ricci (Espaço não-euclidiano).
   - **Resonance Expert:** Campo de Fase e Estabilidade.
   - **Thermal Expert:** Energia de Gibbs e Gradiente de Ruptura.
3. **Gold Atlas (PyTorch):** Motor generativo otimizado para Intel MKL que "sonha" com novas assinaturas químicas.

## 📊 O Vetor de 4 Faces
Cada molécula é reduzida a um tensor de rank 1 no PostgreSQL, permitindo buscas por similaridade geométrica e térmica:
`[Valência, Curvatura, Ressonância, Gibbs]`

## 🛠️ Tecnologias
- **Web/Orchestration:** Ruby on Rails 8.1, Sidekiq/Solid Queue.
- **Data Science:** Python 3.9+, Pandas, PyTorch (Intel MKL), Polars.
- **Database:** PostgreSQL + `pgvector` (via Docker).
- **Environment:** Anaconda (Cadeias Aromáticas).

## 🧬 Prova de Conceito (PoC)
O motor validou com sucesso a ancoragem do **Benzeno** no Zeta `0.0012`, provando a precisão da calibração quântica frente aos análogos gerados pelo Dreamer.

## 🛡️ Integridade da PoC (SHA-256)
A calibração do Ponto Zero (Benzeno) está selada no arquivo `CHECKSUM_POC.sha256`.

