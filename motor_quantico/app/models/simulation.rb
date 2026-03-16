class Simulation < ApplicationRecord
  # Registra os vetores para o pgvector (neighbor)
  has_neighbors :embedding_zeta, :embedding_faces

  # REMOVEMOS A LINHA 'serialize :metadata, coder: JSON'
  # O Rails 8 já faz isso nativamente para colunas jsonb.

  after_initialize :set_defaults, if: :new_record?

  def set_defaults
    self.status ||= 'pending'
    self.current_step ||= 'Aguardando Início'
    # Garante que comece como um Hash vazio se for nil
    self.metadata ||= {}
  end
end

