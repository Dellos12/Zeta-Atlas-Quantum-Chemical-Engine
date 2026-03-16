
require 'open3'
require 'json'

class QuantumPipelineJob < ApplicationJob
  queue_as :default

  # 1. Configuração de Caminhos (Simbiose de Ambiente)
  PYTHON_EXEC = "/home/devildev/anaconda3/envs/cadeias_aromaticas/bin/python"
  PYTHON_BASE = "/home/devildev/projeto_cadeias_aromaticas"

  # 2. Orquestração do Motor Quântico
  PIPELINE = [
    { name: "Ingestion", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/ingestion.py" },
    { name: "Chemo Expert", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/chemo_expert.py" },
    { name: "Geometry Engine", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/geometry_engine.py" },
    { name: "Thermal Expert", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/thermal_expert.py" },
    { name: "Resonance Expert", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/resonance_expert.py" },
    { name: "Train Gold Atlas", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/models/train_gold_atlas.py" },
    { name: "Dream Generator", cmd: "#{PYTHON_EXEC} #{PYTHON_BASE}/src/models/dream_generator.py" }
  ]

  def perform(simulation_id)
    @sim = Simulation.find(simulation_id)
    @sim.update(status: 'processing', started_at: Time.current)

    PIPELINE.each do |step|
      @sim.update(current_step: step[:name])
      
      # Executamos o Python no diretório base dele (IMPORTANTE para os imports)
      success = run_python_step(step[:cmd])
      
      unless success
        @sim.update(status: 'failed', current_step: "Erro em: #{step[:name]}")
        return false
      end
    end

    @sim.update(status: 'completed', ended_at: Time.current)
  end

  private

  def run_python_step(cmd)
    # :chdir garante que o Python encontre a pasta 'data' dentro do projeto dele
    Open3.popen2e(cmd, chdir: PYTHON_BASE) do |_stdin, stdout_err, wait_thr|
      stdout_err.each do |line|
        if line.start_with?("[TELEMETRY]")
          process_telemetry(line)
        else
          # Mostra o progresso do MKL/Pandas no terminal do Rails
          puts "[PYTHON-LOG] #{line.strip}"
        end
      end
      wait_thr.value.success?
    end
  rescue StandardError => e
    Rails.logger.error "Falha crítica no Job: #{e.message}"
    false
  end

  def process_telemetry(line)
    raw_json = line.gsub("[TELEMETRY] ", "").strip
    data = JSON.parse(raw_json)
    
    # Captura segura dos dados de estabilidade (Vetorização)
    stability_data = data.dig("data", "benzeno_stability")

    # Verifica se os dados existem e são um Array antes de converter para Vetor
    if data["step"] == "Passo 6" && stability_data.is_a?(Array)
      # Pegamos os 2 primeiros valores (Zeta e Ruído) para a coluna vector
      vector_to_save = stability_data.take(2)
      @sim.update(embedding_zeta: vector_to_save)
      puts "🧬 VETOR ZETA SINCRONIZADO NO BANCO: #{vector_to_save.inspect}"
    end

    # Sincroniza metadados gerais no campo JSONB do Postgres
    @sim.update(metadata: @sim.metadata.deep_merge(data))
  end
end
