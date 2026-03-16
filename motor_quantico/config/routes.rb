require 'sidekiq/web' # Importante para o painel de controle do Sidekiq

Rails.application.routes.draw do
  # Rota de monitoramento do Rails (Health check)
  get "up" => "rails/health#show", as: :rails_health_check

  # Rotas das Simulações
  resources :simulations, only: [:index, :show, :create]
  
  # Dashboard do Sidekiq (Para você ver o motor rodando no navegador)
  mount Sidekiq::Web => '/sidekiq'

  # Define a página inicial do projeto
  root "simulations#index"
end

