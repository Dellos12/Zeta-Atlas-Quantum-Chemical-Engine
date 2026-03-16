class CreateSimulations < ActiveRecord::Migration[8.1]
  def change
    create_table :simulations do |t|
      t.string :name
      t.string :status
      t.string :current_step
      t.jsonb :metadata
      t.datetime :started_at
      t.datetime :ended_at

      t.timestamps
    end
  end
end
