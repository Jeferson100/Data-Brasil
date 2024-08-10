import os
import sys
sys.path.append("..")
from dotenv import load_dotenv, set_key
def set_fred_api_key():
    api_key = input("Por favor, insira sua chave de API do FRED: ").strip()
    
    base_dir = '/workspaces/Predicoes_macroeconomicas'
    
    dotenv_path = os.path.abspath(os.path.join(base_dir, '.env'))
    
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Adicionar ou atualizar a chave de API no arquivo .env
    set_key(dotenv_path, 'FRED_API_KEY', api_key)
    
# Execute a função se este arquivo for executado como script principal
if __name__ == "__main__":
    set_fred_api_key()
    
