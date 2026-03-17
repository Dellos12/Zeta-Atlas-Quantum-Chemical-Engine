
module OracleInterrogator
  def self.interrogar(id, formula)
    sim = Simulation.find(id)
    puts "⏳ Aguardando o colapso do Hiperplano para #{formula}..."
    
    # Loop de Sincronia Quântica (Máximo 60 segundos)
    60.times do
      sim.reload
      if sim.status == 'completed'
        puts "\n✅ Sincronia Estabelecida!"
        puts "--------------------------------------------------"
        puts "🔬 MOLÉCULA: #{formula}"
        puts "📐 VETOR DE FACES: #{sim.embedding_faces.inspect}"
        puts "🗣️  RESPOSTA: #{sim.interrogar_hiperplano(formula)}"
        puts "--------------------------------------------------"
        return sim
      elsif sim.status == 'failed'
        puts "\n❌ RUPTURA: Falha no passo #{sim.current_step}."
        return sim
      else
        print "."
        sleep 1
      end
    end
    puts "\n⚠️ TIMEOUT: O Hiperplano demorou demais para colapsar."
  end
end
