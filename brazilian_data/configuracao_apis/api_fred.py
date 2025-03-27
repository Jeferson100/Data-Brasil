import os
import sys
sys.path.append("..")
from dotenv import load_dotenv, set_key
def set_fred_api_key() -> None:
    api_key = input("Please enter your FRED API key: ").strip()
    
    current_dir = os.getcwd()

    # Navega até o diretório raiz (um nível acima do diretório atual)
    base_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    dotenv_path = os.path.abspath(os.path.join(base_dir, '.env'))
    
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Adicionar ou atualizar a chave de API no arquivo .env
    set_key(dotenv_path, 'FRED_API_KEY', api_key)
    
# Execute a função se este arquivo for executado como script principal
if __name__ == "__main__":
    set_fred_api_key()
    
