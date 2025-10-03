"""
Classe Controller para o GameTracker.
"""

from model.usuario import Usuario
from model.jogo import Jogo

class GameTrackerController:
    """
    Classe que controla o fluxo da aplicação.
    Responsável por coordenar a comunicação entre a View e o Model.
    """
    
    def __init__(self, view):
        """
        Inicializa o controller.
        
        Args:
            view: Instância da classe GameTrackerView.
        """
        self.view = view
        self.model_usuario = None
        self.model_jogo = None
        
        # Configurar a view para usar este controller
        self.view.set_controller(self)
        
        # Verificar a conexão com o banco de dados
        self._verificar_conexao_db()
    
    def _verificar_conexao_db(self):
        """
        Verifica a conexão com o banco de dados.
        """
        print("[CONTROLLER] Verificando conexão com o banco de dados...")
        
        # Tentar conectar ao MongoDB usando a classe Usuario
        if not Usuario._conectar_db():
            print("[CONTROLLER] Falha ao conectar ao banco de dados")
            self.view.exibir_mensagem(
                "Erro de Conexão",
                "Não foi possível conectar ao banco de dados. Verifique se o MongoDB está em execução."
            )
    
    def lidar_login(self, email, senha):
        """
        Lida com o login do usuário.
        
        Args:
            email (str): Email do usuário.
            senha (str): Senha do usuário.
        """
        print(f"[CONTROLLER] Tentativa de login: {email}")
        
        # Criar uma instância de Usuario e tentar autenticar
        self.model_usuario = Usuario()
        sucesso = self.model_usuario.autenticar(email, senha)
        
        if sucesso:
            # Carregar os jogos do usuário e mostrar o dashboard
            self.carregar_jogos_usuario()
        else:
            # Mostrar mensagem de erro
            self.view.exibir_mensagem("Erro de Login", "Email ou senha incorretos.")
    
    def lidar_cadastro(self, nome, email, senha):
        """
        Lida com o cadastro de um novo usuário.
        
        Args:
            nome (str): Nome do usuário.
            email (str): Email do usuário.
            senha (str): Senha do usuário.
        """
        print(f"[CONTROLLER] Tentativa de cadastro: {nome} ({email})")
        
        # Criar uma instância de Usuario e tentar cadastrar
        self.model_usuario = Usuario()
        sucesso = self.model_usuario.cadastrar(nome, email, senha)
        
        if sucesso:
            # Mostrar mensagem de sucesso e voltar para a tela de login
            self.view.exibir_mensagem("Cadastro Realizado", "Cadastro realizado com sucesso! Faça login para continuar.")
            self.view.mostrar_tela_login()
        else:
            # Mostrar mensagem de erro
            self.view.exibir_mensagem("Erro de Cadastro", "Não foi possível realizar o cadastro. O email já pode estar em uso.")
    
    def carregar_jogos_usuario(self):
        """
        Carrega os jogos do usuário atual e mostra o dashboard.
        """
        print("[CONTROLLER] Carregando jogos do usuário")
        
        if not self.model_usuario:
            self.view.exibir_mensagem("Erro", "Usuário não autenticado.")
            self.view.mostrar_tela_login()
            return
        
        # Buscar os jogos do usuário
        jogos = self.model_usuario.buscar_jogos()
        
        # Converter os objetos Jogo para dicionários
        jogos_dict = [jogo.to_dict() for jogo in jogos]
        
        # Mostrar o dashboard com os jogos
        self.view.mostrar_dashboard(jogos_dict)
    
    def lidar_adicionar_jogo(self, dados_jogo):
        """
        Lida com a adição de um novo jogo.
        
        Args:
            dados_jogo (dict): Dados do jogo a ser adicionado.
        """
        print(f"[CONTROLLER] Adicionando jogo: {dados_jogo.get('titulo')}")
        
        if not self.model_usuario:
            self.view.exibir_mensagem("Erro", "Usuário não autenticado.")
            self.view.mostrar_tela_login()
            return
        
        # Adicionar o ID do usuário aos dados do jogo
        dados_jogo['id_usuario'] = self.model_usuario.id
        
        # Criar uma instância de Jogo e salvar
        self.model_jogo = Jogo(**dados_jogo)
        sucesso = self.model_jogo.salvar()
        
        if sucesso:
            # Mostrar mensagem de sucesso e voltar para o dashboard
            self.view.exibir_mensagem("Jogo Adicionado", "Jogo adicionado com sucesso!")
            self.carregar_jogos_usuario()
        else:
            # Mostrar mensagem de erro
            self.view.exibir_mensagem("Erro", "Não foi possível adicionar o jogo. Tente novamente.")
    
    def lidar_editar_jogo(self, id_jogo, dados_jogo):
        """
        Lida com a edição de um jogo existente.
        
        Args:
            id_jogo (str): ID do jogo a ser editado.
            dados_jogo (dict): Novos dados do jogo.
        """
        print(f"[CONTROLLER] Editando jogo: {id_jogo}")
        
        if not self.model_usuario:
            self.view.exibir_mensagem("Erro", "Usuário não autenticado.")
            self.view.mostrar_tela_login()
            return
        
        # Buscar o jogo pelo ID
        self.model_jogo = Jogo.buscar_por_id(id_jogo)
        
        if not self.model_jogo:
            self.view.exibir_mensagem("Erro", "Jogo não encontrado.")
            self.carregar_jogos_usuario()
            return
        
        # Verificar se o jogo pertence ao usuário atual
        if self.model_jogo.id_usuario != self.model_usuario.id:
            self.view.exibir_mensagem("Erro", "Você não tem permissão para editar este jogo.")
            self.carregar_jogos_usuario()
            return
        
        # Atualizar os dados do jogo
        sucesso = self.model_jogo.atualizar(dados_jogo)
        
        if sucesso:
            # Mostrar mensagem de sucesso e voltar para o dashboard
            self.view.exibir_mensagem("Jogo Atualizado", "Jogo atualizado com sucesso!")
            self.carregar_jogos_usuario()
        else:
            # Mostrar mensagem de erro
            self.view.exibir_mensagem("Erro", "Não foi possível atualizar o jogo. Tente novamente.")
    
    def lidar_excluir_jogo(self, id_jogo):
        """
        Lida com a exclusão de um jogo.
        
        Args:
            id_jogo (str): ID do jogo a ser excluído.
        """
        print(f"[CONTROLLER] Excluindo jogo: {id_jogo}")
        
        if not self.model_usuario:
            self.view.exibir_mensagem("Erro", "Usuário não autenticado.")
            self.view.mostrar_tela_login()
            return
        
        # Buscar o jogo pelo ID
        self.model_jogo = Jogo.buscar_por_id(id_jogo)
        
        if not self.model_jogo:
            self.view.exibir_mensagem("Erro", "Jogo não encontrado.")
            self.carregar_jogos_usuario()
            return
        
        # Verificar se o jogo pertence ao usuário atual
        if self.model_jogo.id_usuario != self.model_usuario.id:
            self.view.exibir_mensagem("Erro", "Você não tem permissão para excluir este jogo.")
            self.carregar_jogos_usuario()
            return
        
        # Excluir o jogo
        sucesso = self.model_jogo.excluir()
        
        if sucesso:
            # Mostrar mensagem de sucesso e voltar para o dashboard
            self.view.exibir_mensagem("Jogo Excluído", "Jogo excluído com sucesso!")
            self.carregar_jogos_usuario()
        else:
            # Mostrar mensagem de erro
            self.view.exibir_mensagem("Erro", "Não foi possível excluir o jogo. Tente novamente.")
    
    def calcular_estatisticas(self):
        """
        Calcula estatísticas sobre os jogos do usuário.
        
        Returns:
            dict: Dicionário com as estatísticas.
        """
        print("[CONTROLLER] Calculando estatísticas")
        
        if not self.model_usuario:
            return {'total_jogos': 0, 'media_notas': 0}
        
        # Buscar os jogos do usuário
        jogos = self.model_usuario.buscar_jogos()
        
        # Calcular estatísticas
        total_jogos = len(jogos)
        soma_notas = sum(jogo._nota for jogo in jogos if jogo._nota is not None)
        media_notas = soma_notas / total_jogos if total_jogos > 0 else 0
        
        return {
            'total_jogos': total_jogos,
            'media_notas': round(media_notas, 1)
        }
    
    def iniciar(self):
        """
        Inicia a aplicação.
        """
        print("[CONTROLLER] Iniciando aplicação")
        self.view.iniciar()
