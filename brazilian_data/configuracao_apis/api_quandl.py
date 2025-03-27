import os
from dotenv import load_dotenv, set_key

def set_quandl_api_key() -> None:
    api_key = input("Por favor, insira sua chave de API do Quandl: ").strip()

    # Carregar variáveis de ambiente existentes do arquivo .env
    dotenv_path = '.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Adicionar ou atualizar a chave de API no arquivo .env
    set_key(dotenv_path, 'QUANDL_API_KEY', api_key)
    
    if os.getenv('QUANDL_API_KEY') == api_key:
        print("Chave de API salva com sucesso no arquivo .env.")
    else:
        print('Chave de API não encontrada. Verifique se o arquivo .env foi criado corretamente.')

if __name__ == "__main__":
    set_quandl_api_key()