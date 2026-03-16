import pandas as pd
import torch
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer, util

# Ajuste para garantir que o Python encontre os agentes na pasta src/grammar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.grammar.endofora_expert import EndoforaAgent
from src.grammar.topology_expert import TopologyAgent
from src.grammar.phase_expert import PhaseAgent

class AromaticOracle:
    def __init__(self):
        print("🔮 [Passo 9] Sintonizando Hiperplano (Linguagem + Matéria)...")
        
        # 1. Carregando os 3 Mundos
        self.nlp = SentenceTransformer('all-MiniLM-L6-v2')
        self.df_atlas = pd.read_parquet('data/gold/atlas_final.parquet')
        self.df_memoria = pd.read_pickle('data/silver/memoria_indexada.pkl')
        
        # 2. Inicializando Agentes Gramaticais (A Sintaxe Autônoma)
        self.endofora = EndoforaAgent()
        self.topology = TopologyAgent()
        self.phase = PhaseAgent()

    def consultar_big_data(self, query_emb):
        """Busca na Memória Indexada a sentença literária mais próxima"""
        memoria_embeddings = np.stack(self.df_memoria['vetor'].values)
        cos_scores = util.cos_sim(query_emb, memoria_embeddings).flatten()
        best_idx = torch.argmax(cos_scores).item()
        return self.df_memoria.iloc[best_idx]['contexto'], cos_scores[best_idx].item()

    def interrogar(self, query):
        # --- FASE 1: O SENO DA LINGUAGEM (PROCESSAMENTO DE ONDA) ---
        query_emb = self.nlp.encode(query, convert_to_tensor=True)
        
        # Resolve Endófora (Deste/Este) - O Agente mantém o fio da meada
        mol_id = self.endofora.resolver(query)
        
        # Ajusta Confiança X (Agente de Fase: E/No/Com)
        confianca_base = 0.85
        confianca_x = self.phase.ajustar_frequencia(query, confianca_base)

        # --- FASE 2: A MEMÓRIA (CONSULTA AO BIG DATA) ---
        contexto_lit, score_lit = self.consultar_big_data(query_emb)

        # --- FASE 3: O COSSENO DA MATÉRIA (ZETA DA REDE NEURAL) ---
        row = self.df_atlas[self.df_atlas['molecule_id'] == mol_id].iloc
        
        # O Agente Topológico transporta a nomenclatura para o Zeta
        zeta_projetado = self.topology.aplicar_nomenclatura(query, row['zeta'])
        
        # Evocação de Fechamento (A Matéria escreve a Linguagem)
        nome_evocado, fisica_evocada = self.topology.evocar_sentenca(zeta_projetado)

        # --- SÍNTESE FINAL (A INTERSECÇÃO X) ---
        print("\n" + "═"*80)
        print(f"📡 INTERSECÇÃO DE FASE [X]: {confianca_x:.2%}")
        print(f"📖 MEMÓRIA LITERÁRIA: {contexto_lit}")
        print("-" * 80)
        print(f"📢 DIAGNÓSTICO: O sujeito {mol_id} ({row['identidade_final']})")
        print(f"   ∟ Zeta Projetado: {zeta_projetado:.6f}")
        print(f"   ∟ Ressonância:    {row['energia_ressonancia']:.1f} kcal/mol")
        print("-" * 80)
        print(f"🔮 EVOCAÇÃO DO CAMPO: Posição {nome_evocado} ({fisica_evocada})")
        
        if query.strip().lower().endswith("posição"):
            print(f"📝 FRASE COMPLETADA: '{query} {nome_evocado.lower()}'")
        print("═"*80)

    def loop(self):
        print("\n" + "╔" + "═"*63 + "╗")
        print("║   ORÁCULO FINAL: O ENCONTRO DO SENO E DO COSSENO              ║")
        print("╚" + "═"*63 + "╝")
        while True:
            try:
                p = input("\n[SENTENÇA VETORIAL] > ")
                if p.lower() in ['sair', 'exit', 'quit']: break
                if not p.strip(): continue
                self.interrogar(p)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    oracle = AromaticOracle()
    oracle.loop()

