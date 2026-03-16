
class EndoforaAgent:
    def __init__(self):
        self.memoria_sujeito = "AROM_001" # Inicia no Cerne

    def resolver(self, query, id_detectado=None):
        if id_detectado:
            self.memoria_sujeito = id_detectado
            return id_detectado
        # Se usar pronome, evoca o último sujeito da memória
        if "deste" in query.lower() or "este" in query.lower():
            print(f"🔗 [Endófora] Agente vinculando '{query.split()[0]}' ao Sujeito: {self.memoria_sujeito}")
            return self.memoria_sujeito
        return id_detectado

