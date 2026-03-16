class PhaseAgent:
    def __init__(self):
        # Conectores como Vetores de Adição de Fase
        self.conectores = {"e": 1.1, "no": 1.05, "com": 1.15}

    def ajustar_frequencia(self, query, score_base):
        mult = 1.0
        for p in query.lower().split():
            if p in self.conectores:
                mult *= self.conectores[p]
        return score_base * mult

