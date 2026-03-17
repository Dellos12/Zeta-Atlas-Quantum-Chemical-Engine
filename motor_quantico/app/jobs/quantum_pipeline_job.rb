
require 'open3'
require 'json'
require 'yaml'

class QuantumPipelineJob < ApplicationJob
  queue_as :default

  # 1. Configuração de Caminhos (Simbiose de Ambiente)
  PYTHON_EXEC = "/home/devildev/anaconda3/envs/cadeias_aromaticas/bin/python -u"
  PYTHON_BASE = File.expand_path("../projeto_cadeias_aromaticas", Rails.root)

  # 2. Orquestração Industrial (Agora com 8 Passos: Incluindo Solubilidade)
  PIPELINE_STEPS = [
    "src/periodic_expert.py",    # Passo 0: Blindagem Atômica
    "src/ingestion.py",          # Passo 1: Unificação Bronze
    "src/chemo_expert.py",       # Passo 2: Valência Pi
    "src/geometry_engine.py",    # Passo 3: Ricci (Geometria)
    "src/resonance_expert.py",   # Passo 4: Fase (Ressonância)
    "src/thermal_expert.py",     # Passo 5: Gibbs (Tensão)
    "src/solubility_expert.py",  # Passo 5.5: LogP (Afinidade Hídrica) <--- NOVO
    "src/models/train_gold_atlas.py" # Passo 6: Fusão Gold (Tensor Final)
  ]

  def perform(simulation_id, formula = "C6H6")
    @sim = Simulation.find(simulation_id)
    
    # Busca as Leis Universais na Tabela Periódica
    periodic_table = YAML.load_file(Rails.root.join('config', 'periodic_table.yml'))['elements']
    
    zeta_targets = {
      formula: formula,
      atomic_rules: periodic_table,
      target_gibbs: (formula == "C6H6" ? 10.0 : 15.0)
    }

    @sim.update(status: 'processing', metadata: @sim.metadata.merge(zeta_targets))
    
    # Injeção de Blindagem e Performance (Hardware LTS-CPU)
    env_vars = { 
      "ZETA_TARGETS" => zeta_targets.to_json,
      "POLARS_SKIP_CPU_CHECK" => "1", 
      "OMP_NUM_THREADS" => "1", 
      "PYTHONUNBUFFERED" => "1" 
    }

    run_pipeline(env_vars)
  end

  private

  def run_pipeline(env)
    PIPELINE_STEPS.each do |step_path|
      current_script = step_path.split('/').last
      @sim.update(current_step: current_script)
      
      full_path = File.join(PYTHON_BASE, step_path)
      
      Open3.popen2e(env, "#{PYTHON_EXEC} #{full_path}", chdir: PYTHON_BASE) do |_, out, wait|
        out.each { |line| process_telemetry(line) }
        
        unless wait.value.success?
          @sim.update(status: 'failed', current_step: "Ruptura no passo: #{current_script}")
          raise "Erro Crítico no Hiperplano: #{current_script}" 
        end
      end
    end

    @sim.update(status: 'completed', ended_at: Time.current)
  end

  def process_telemetry(line)
    return unless line.start_with?("[TELEMETRY]")
    data = JSON.parse(line.gsub("[TELEMETRY] ", "").strip)
    
    # Sincroniza metadados acumulativos (Pandas/MXNet)
    @sim.metadata = @sim.metadata.deep_merge(data)

    # Captura final no Passo 6
    if data["step"] == "Passo 6"
      m = @sim.metadata["data"]
      # Atribui as faces capturadas ao longo de todos os experts
      @sim.update(
        embedding_faces: [
          m["valencia_pi"].to_f,
          m["curvatura_ricci"].to_f,
          m["energia_ressonancia"].to_f,
          m["energia_gibbs"].to_f
        ]
      )
      # Captura o Vetor Zeta estabilizado pelo MXNet
      @sim.update(embedding_zeta: data["data"]["benzeno_stability"].flatten.take(2).map(&:to_f)) if data["data"]["benzeno_stability"]
    end

    @sim.save if data["progress"] == 100
  end
end
