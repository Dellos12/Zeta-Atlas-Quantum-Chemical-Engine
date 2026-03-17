
require 'open3'
require 'json'
require 'yaml'

class QuantumPipelineJob < ApplicationJob
  queue_as :default

  # 1. Configuração de Caminhos (Simbiose de Ambiente)
  PYTHON_EXEC = "/home/devildev/anaconda3/envs/cadeias_aromaticas/bin/python"
    PYTHON_BASE = Rails.root.join('..', 'projeto_cadeias_aromaticas').to_s

  # 2. Orquestração do Motor (Agora inclui o Passo 0: Periodic Expert)
  PIPELINE_STEPS = [
    "src/periodic_expert.py",
    "src/ingestion.py",
    "src/chemo_expert.py",
    "src/geometry_engine.py",
    "src/thermal_expert.py",
    "src/resonance_expert.py",
    "src/models/train_gold_atlas.py"
  ]

  def perform(simulation_id, formula = "C6H6")
    @sim = Simulation.find(simulation_id)
    
    # 3. O CONTRATO QUÂNTICO (O Diálogo Rails -> Python)
    # Buscamos a "Lei" na Tabela Periódica configurada no Rails
    periodic_table = YAML.load_file(Rails.root.join('config', 'periodic_table.yml'))['elements']
    
    zeta_targets = {
      formula: formula,
      atomic_rules: periodic_table,
      target_gibbs: (formula == "C6H6" ? 10.0 : 15.0), # Alvos dinâmicos por fórmula
      mode: "industrial_validation"
    }

    # Registramos o início e os alvos no banco de dados
    @sim.update(
      status: 'processing', 
      started_at: Time.current,
      metadata: @sim.metadata.merge(zeta_targets)
    )

    # 4. EXECUÇÃO DO PIPELINE COM INJEÇÃO DE AMBIENTE
    run_pipeline(zeta_targets)
  end

  private

  def run_pipeline(targets)
    PIPELINE_STEPS.each do |step_path|
      @sim.update(current_step: step_path.split('/').last)
      
      cmd = "#{PYTHON_EXEC} #{PYTHON_BASE}/#{step_path}"
      
      # INJEÇÃO DE BLINDAGEM: O Python recebe o JSON via variável de ambiente
      env_vars = { "ZETA_TARGETS" => targets.to_json }

      Open3.popen2e(env_vars, cmd, chdir: PYTHON_BASE) do |_stdin, stdout_err, wait_thr|
        stdout_err.each do |line|
          if line.start_with?("[TELEMETRY]")
            process_telemetry(line)
          else
            # Mostra o log do Python no console do Rails
            puts "[PYTHON-LOG] #{line.strip}"
          end
        end
        
        # Se a física romper (erro no Python), o Rails aborta a simbiose
        unless wait_thr.value.success?
          @sim.update(status: 'failed', current_step: "Ruptura no passo: #{step_path}")
          return false
        end
      end
    end

    @sim.update(status: 'completed', ended_at: Time.current)
  end

  def process_telemetry(line)
    raw_json = line.gsub("[TELEMETRY] ", "").strip
    data = JSON.parse(raw_json)
    
    # CAPTURA DE FACES (Vetorização para o pgvector)
    # Se o passo for o Gold Atlas, capturamos o tensor final
    if data["step"] == "Passo 6" && data["data"]["benzeno_stability"].is_a?(Array)
      vector = data["data"]["benzeno_stability"].take(2)
      @sim.update(embedding_zeta: vector)
    end

    # Sincronização acumulativa de metadados
    @sim.update(metadata: @sim.metadata.deep_merge(data))
  end
end
