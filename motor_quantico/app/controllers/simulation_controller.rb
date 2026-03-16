class SimulationsController < ApplicationController
  # GET /simulations
  def index
    @simulations = Simulation.order(created_at: :desc)
  end

  # POST /simulations
  def create
    @simulation = Simulation.create(name: "Simulação #{Time.current.to_i}")
    
    # Isso coloca o seu motor Python na fila do Sidekiq/ActiveJob
    QuantumPipelineJob.perform_later(@simulation.id)
    
    redirect_to @simulation, notice: "Motor Quântico Iniciado!"
  end

  # GET /simulations/:id
  def show
    @simulation = Simulation.find(params[:id])
  end
end

