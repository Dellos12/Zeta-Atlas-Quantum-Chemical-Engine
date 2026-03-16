class TopologyAgent:
    def __init__(self):
        # Mapeamento de Tensão Topológica (A Geometria do Caminho)
        self.fases = {"para": 0.01, "meta": 0.05, "orto": 0.12}

    def aplicar_nomenclatura(self, query, zeta_base):
        for p in query.lower().split():
            if p in self.fases:
                desvio = self.fases[p]
                print(f"📐 [Topologia] Agente projetando Geometria {p.upper()} (Offset: {desvio})")
                return zeta_base + desvio
        return zeta_base

    def evocar_sentenca(self, zeta):
        abs_z = abs(zeta)
        if abs_z <= 0.02: return "PARA", "Simetria Axial (1,4)"
        if abs_z <= 0.05: return "META", "Alternância (1,3)"
        return "ORTO", "Tensão de Proximidade (1,2)"


