import torch
from sentence_transformers import SentenceTransformer
import os

def export():
    model_name = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)
    
    # Pasta de destino no Rails (ajuste o caminho se necessário)
    target_dir = '../antena_telemetria/bin/data'
    os.makedirs(target_dir, exist_ok=True)

    print(f"📦 Exportando {model_name} para ONNX...")

    # 1. Exportar o Modelo para ONNX
    dummy_input = {
        'input_ids': torch.ones(1, 128, dtype=torch.long),
        'attention_mask': torch.ones(1, 128, dtype=torch.long)
    }
    
    torch.onnx.export(
        model[0].auto_model, # O modelo transformer base
        (dummy_input['input_ids'], dummy_input['attention_mask']),
        os.path.join(target_dir, "model.onnx"),
        input_names=['input_ids', 'attention_mask'],
        output_names=['last_hidden_state'],
        dynamic_axes={'input_ids': {0: 'batch_size', 1: 'sequence'}, 
                     'attention_mask': {0: 'batch_size', 1: 'sequence'}},
        opset_version=14
    )

    # 2. Salvar o Tokenizador (necessário para o Rails 'ler' o texto)
    model.tokenizer.save_pretrained(target_dir)
    # Renomeie o arquivo gerado de tokenizer.json (se necessário)
    print(f"✅ Modelo e Tokenizador entregues em: {target_dir}")

if __name__ == "__main__":
    export()

