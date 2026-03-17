class Simulation < ApplicationRecord
  has_neighbors :embedding_zeta, :embedding_faces
  after_initialize :set_defaults, if: :new_record?

  # Carregamos a Tabela Periódica como Referência de Verdade
  def periodic_data
    @periodic_data ||= YAML.load_file(Rails.root.join('config', 'periodic_table.yml'))['elements']
  end

  def set_defaults
    self.status ||= 'pending'
    self.current_step ||= 'Aguardando Início'
    self.metadata ||= {}
  end

  # O Diálogo: O Rails pergunta à física se o vetor condiz com a estequiometria
  def interrogar_hiperplano(formula)
    return "Sem dados de face capturados" if embedding_faces.blank?

    # Desempacota as 4 Faces: [Valência, Ricci, Ressonância, Gibbs]
    v_pi, ricci, res, gibbs = embedding_faces

    # Extração de massa do contrato (Ex: C6H6)
    c_count = formula.scan(/C(\d*)/).flatten.first.to_i
    c_count = 1 if c_count == 0 && formula.include?("C")
    
    # Validação Semântica: O dado condiz com a Lei Periódica?
    validacao_valencia = (v_pi == c_count * 1.0) # 1 elétron Pi por carbono sp2
    
    if validacao_valencia && ricci < 0.2
      "Assinatura Confirmada: #{formula} estruturado como Anel Hexagonal plano (Aromático). Estabilidade Zeta: #{embedding_zeta[0]}."
    elsif ricci > 0.7
      "Assinatura Confirmada: #{formula} estruturado como Cadeia Saturada (sp3). Geometria Tetraédrica."
    else
      "Anomalia Geométrica: A curvatura de Ricci (#{ricci}) sugere tensão não-euclidiana para #{formula}."
    end
  end
end

