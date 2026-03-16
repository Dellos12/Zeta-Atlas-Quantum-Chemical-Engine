class SetupQuantumVectors < ActiveRecord::Migration[7.1]
  def change
    # Em vez de create_table, vamos alterar a existente
    change_table :simulations do |t|
      # VETOR 1: Estabilidade (Zeta e Ruído) -> Dimensão 2
      t.column :embedding_zeta, :vector, limit: 2
      
      # VETOR 2: Faces Quânticas (Valencia, Ricci, Ressonância, Gibbs) -> Dimensão 4
      t.column :embedding_faces, :vector, limit: 4
    end
  end
end

