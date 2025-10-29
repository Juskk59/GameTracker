"""
GameTracker - Gerenciador de Biblioteca de Jogos
Aplicação desktop com padrão MVC utilizando Python, Tkinter e MongoDB
"""

from controller.gametracker_controller import GameTrackerController
from view.gametracker_view import GameTrackerView


def main():
    # Inicializa o controller (responsável pelas conexões)
    controller = GameTrackerController()
    
    # Verifica se conseguiu conectar ao banco
    if not controller.conectado:
        print("\n✗ Erro: Não foi possível conectar ao MongoDB")
        print("✗ Certifique-se de que o MongoDB está rodando em localhost:27017")
        return
    
    print("=" * 50)
    print("GameTracker - Gerenciador de Jogos")
    print("=" * 50)
    print("\nIniciando aplicação...\n")
    
    # Cria a view passando o controller já inicializado
    app = GameTrackerView(controller)
    
    # Inicia o loop de eventos
    app.executar()


if __name__ == "__main__":
    main()