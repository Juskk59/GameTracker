
from view import GameTrackerView
from controller import GameTrackerController

if __name__ == "__main__":
    # Criar a view
    view = GameTrackerView()
    
    # Criar o controller e passar a view
    controller = GameTrackerController(view)
    
    # Iniciar a aplicação
    controller.iniciar()
