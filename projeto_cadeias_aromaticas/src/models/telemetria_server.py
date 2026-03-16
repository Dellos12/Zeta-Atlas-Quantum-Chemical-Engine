
import grpc
from concurrent import futures
import torch
import numpy as np
import sys
import os

# Adiciona a raiz ao path para localizar src.grammar e os modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import telemetria_pb2
import telemetria_pb2_grpc
from src.models.oracle import AromaticOracle

class OraculoServicer(telemetria_pb2_grpc.OraculoServiceServicer):
    def __init__(self):
        # Inicializa o Cerebro (Atlas Gold, Memoria e Agentes)
        self.brain = AromaticOracle()
        print("🧠 [MOTOR VETORIAL] Hiperplano em fase 384-D.")

    def InterseccaoGeometrica(self, request, context):
        # 1. RECEBE O SENO (Linguagem)
        # O gRPC entrega uma lista; convertemos para Tensor PyTorch
        vetor_recebido = list(request.vetor)
        
        # VALIDACAO DE FASE (Dimensao do MiniLM-L6-v2)
        if len(vetor_recebido) != 384:
            print(f"⚠️ DISSONANCIA: {len(vetor_recebido)} dims recebidas. Esperado 384.")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return telemetria_pb2.TensorCosseno()

        vetor_seno = torch.tensor(vetor_recebido, dtype=torch.float32)

        # 2. CALCULA O COSSENO (Materia)
        #Stack da memoria indexada no Passo 7
        memoria_embs = torch.stack([torch.tensor(v) for v in self.brain.df_memoria['vetor'].values])
        
        # Similaridade de Cosseno (Interseccao X)
        scores = torch.nn.functional.cosine_similarity(vetor_seno.unsqueeze(0), memoria_embs)
        best_idx = torch.argmax(scores).item()
        angulo_x = scores[best_idx].item()

        # 3. BUSCA NO ATLAS GOLD (Zeta e Ricci)
        mol_id = self.brain.df_atlas.iloc[best_idx % len(self.brain.df_atlas)]['molecule_id']
        row = self.brain.df_atlas[self.brain.df_atlas['molecule_id'] == mol_id].iloc

        # 4. EVOCACAO TOPOLOGICA
        zeta_base = row['zeta']
        nome_evoc, fisica = self.brain.topology.evocar_sentenca(zeta_base)

        print(f"📡 [gRPC] Intersecção X: {angulo_x:.2%} | Sujeito: {mol_id} | Zeta: {zeta_base:.6f}")

        # 5. DEVOLVE O ESTADO DE REPOUSO
        return telemetria_pb2.TensorCosseno(
            molecule_id=mol_id,
            vetor_materia=memoria_embs[best_idx].tolist(), # O Cosseno da Materia
            zeta=float(zeta_base),
            angulo_interseccao=float(angulo_x),
            ricci_curvatura=float(row['curvatura_ricci']),
            evocacao=f"{nome_evoc} ({fisica})"
        )

def serve():
    # MKL_DEBUG_CPU_TYPE=5 deve estar ativo para evitar Core Dump
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    telemetria_pb2_grpc.add_OraculoServiceServicer_to_server(OraculoServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 [MOTOR] On-line na porta 50051.")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
