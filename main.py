"""
Arquivo principal para iniciar a aplicação GameTracker.
"""

import sys
from view.gametracker_view import GameTrackerView
from controller.gametracker_controller import GameTrackerController
from model.usuario import Usuario

def verificar_conexao_db():
    """
    Verifica a conexão com o MongoDB.
    
    Returns:
        bool: True se a conexão foi estabelecida com sucesso, False caso contrário.
    """
    print(f"Verificando conexão com o MongoDB ({Usuario.MONGODB_HOST}:{Usuario.MONGODB_PORT}/{Usuario.MONGODB_DATABASE})...")
    
    # Tentar estabelecer a conexão usando a classe Usuario
    sucesso = Usuario._conectar_db()
    
    if sucesso:
        print("Conexão com o MongoDB estabelecida com sucesso!")
    else:
        print("Falha ao conectar ao MongoDB. Verifique se o servidor está em execução.")
    
    return sucesso

def inicializar_banco_dados():
    """
    Inicializa o banco de dados com dados de exemplo.
    
    Returns:
        bool: True se a inicialização foi bem-sucedida, False caso contrário.
    """
    print("Inicializando banco de dados com dados de exemplo...")
    
    # Usar o método da classe Usuario para inicializar o banco de dados
    resultado = Usuario.inicializar_db_com_dados_exemplo()
    
    if resultado:
        print("\nBanco de dados inicializado com sucesso!")
        print("\nCredenciais de acesso:")
        print(f"Email: {resultado['email']}")
        print(f"Senha: {resultado['senha']}")
        return True
    else:
        print("Falha ao inicializar o banco de dados.")
        return False

if __name__ == "__main__":
    # Verificar a conexão com o banco de dados
    if not verificar_conexao_db():
        print("Não foi possível conectar ao banco de dados. A aplicação será encerrada.")
        sys.exit(1)
    
    # Perguntar se deseja inicializar o banco de dados com dados de exemplo
    resposta = input("Deseja inicializar o banco de dados com dados de exemplo? (s/n): ")
    if resposta.lower() == 's':
        inicializar_banco_dados()
    
    # Criar a view
    view = GameTrackerView()
    
    # Criar o controller e passar a view
    controller = GameTrackerController(view)
    
    # Iniciar a aplicação
    controller.iniciar()
