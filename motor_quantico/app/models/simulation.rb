class Simulation < ApplicationRecord
  # Registra os vetores para busca matemática e espacial
  has_neighbors :embedding_zeta, :embedding_faces

  after_initialize :set_defaults, if: :new_record?

  # Constantes de Geometria Sagrada e Bioatividade
  LEI_SP2_RICCI = 0.25 # Limite para aromaticidade plana
  LEI_SP3_RICCI = 0.70 # Limite para saturação tridimensional
  LIMITE_FARMACO_RES = 20.0 # Ressonância mínima para estabilidade heterocíclica

  def set_defaults
    self.status ||= 'pending'
    self.current_step ||= 'Aguardando Início'
    self.metadata ||= {}
  end

  # O ORÁCULO DE DECIFRAÇÃO: Traduzindo Tensores em Identidade Química
  def interrogar_hiperplano(formula_proposta)
    id_real = metadata.dig("data", "molecule_id")
    return "Hiperplano sem âncora de ID capturada" if id_real.nil?
    return "Vetor de faces incompleto para decifração" if embedding_faces.blank?

    # Desempacota: [Valência, Ricci, Ressonância, Gibbs]
    v_pi, ricci, res, gibbs = embedding_faces
    
    # Extraímos a Eletronegatividade do metadado (calculada pelo Periodic Expert)
    en_media = metadata.dig("data", "eletronegatividade_media") || 2.55

    case id_real
    when /_SP2$/
      if ricci < LEI_SP2_RICCI && res >= 30
        "ID: #{id_real} | POSIÇÃO: CERNE (sp2). Hidrocarboneto Aromático: Anel Hexagonal Plano (Benzeno)."
      else
        "ID: #{id_real} | POSIÇÃO: RUPTURA. Tensão geométrica detectada na estrutura plana."
      end

    when /_SP3$/
      if ricci > LEI_SP3_RICCI
        "ID: #{id_real} | POSIÇÃO: EXPANSÃO (sp3). Cicloalcano: Geometria Tetraédrica Saturada (Ciclohexano)."
      else
        "ID: #{id_real} | POSIÇÃO: ANOMALIA. Hibridização sp3 não colapsou em volume tridimensional."
      end

    when /_HET$/
      # LÓGICA DE FÁRMACOS (Piridina e similares)
      if ricci < LEI_SP2_RICCI && res >= LIMITE_FARMACO_RES
        "ID: #{id_real} | POSIÇÃO: HETEROCICLO AROMÁTICO. Análogo de Piridina detectado. " \
        "Assinatura de FÁRMACO com Polaridade Elevada (EN: #{en_media})."
      else
        "ID: #{id_real} | POSIÇÃO: INSTABILIDADE MEDICINAL. Assimetria de campo rompeu a fase aromática."
      end

    else
      "ID: #{id_real} | POSIÇÃO: DESCONHECIDA. Molécula Sintética fora do mapeamento padrão."
    end
  end

  # Método auxiliar para o Dashboard: Alerta de Solubilidade (LogP)
  def alerta_biodisponibilidade
    log_p = metadata.dig("data", "log_p")
    return "Sem dados de LogP" if log_p.nil?

    if log_p.to_f.between?(0.0, 3.0)
      "🟢 Ótima solubilidade para absorção oral."
    else
      "🔴 Baixa solubilidade ou excesso de lipofilicidade."
    end
  end
end

