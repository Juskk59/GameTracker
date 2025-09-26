"""
Classe Model para Jogo no GameTracker.
"""

class Jogo:
    """
    Classe que representa um jogo no sistema.
    Responsável por gerenciar os dados do jogo e a comunicação com o banco de dados.
    """
    
    def __init__(self, id=None, titulo=None, plataforma=None, genero=None, 
                 status=None, nota=None, descricao=None, id_usuario=None):
        """
        Inicializa um objeto Jogo.
        
        Args:
            id (str, opcional): ID do jogo no banco de dados.
            titulo (str, opcional): Título do jogo.
            plataforma (str, opcional): Plataforma do jogo.
            genero (str, opcional): Gênero do jogo.
            status (str, opcional): Status do jogo (jogando, finalizado, etc.).
            nota (float, opcional): Nota do jogo (0-10).
            descricao (str, opcional): Descrição/review do jogo.
            id_usuario (str, opcional): ID do usuário dono do jogo.
        """
        self._id = id
        self._titulo = titulo
        self._plataforma = plataforma
        self._genero = genero
        self._status = status
        self._nota = nota
        self._descricao = descricao
        self._id_usuario = id_usuario
    
    @property
    def id(self):
        return self._id
        
    @property
    def titulo(self):
        return self._titulo
        
    @property
    def id_usuario(self):
        return self._id_usuario
    
    def salvar(self):
        """
        Salva os dados do jogo no banco de dados.
        
        Returns:
            bool: True se o salvamento foi bem-sucedido, False caso contrário.
        """
        # Em uma implementação real, salvaríamos os dados no MongoDB
        
        # Simulação de ID se for um novo jogo
        if not self._id:
            import random
            self._id = f"jogo_{random.randint(1000, 9999)}"
            
        print(f"[MODEL] Salvando jogo: {self._titulo} (ID: {self._id})")
        return True
    
    def excluir(self):
        """
        Exclui o jogo do banco de dados.
        
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        # Em uma implementação real, excluiríamos o jogo do MongoDB
        
        print(f"[MODEL] Excluindo jogo: {self._titulo} (ID: {self._id})")
        return True
    
    def atualizar(self, dados):
        """
        Atualiza os dados do jogo.
        
        Args:
            dados (dict): Dicionário com os novos dados do jogo.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        # Em uma implementação real, atualizaríamos os dados no MongoDB
        
        # Atualizar os atributos com os novos dados
        if 'titulo' in dados:
            self._titulo = dados['titulo']
        if 'plataforma' in dados:
            self._plataforma = dados['plataforma']
        if 'genero' in dados:
            self._genero = dados['genero']
        if 'status' in dados:
            self._status = dados['status']
        if 'nota' in dados:
            self._nota = dados['nota']
        if 'descricao' in dados:
            self._descricao = dados['descricao']
            
        print(f"[MODEL] Atualizando jogo: {self._titulo} (ID: {self._id})")
        return True
    
    @staticmethod
    def buscar_todos_do_usuario(id_usuario):
        """
        Busca todos os jogos de um usuário.
        
        Args:
            id_usuario (str): ID do usuário.
            
        Returns:
            list: Lista de objetos Jogo.
        """
        # Em uma implementação real, buscaríamos os jogos no MongoDB
        # usando o ID do usuário
        
        # Simulação de jogos
        jogos = []
        if id_usuario:
            # Criar alguns jogos de exemplo
            jogos = [
                Jogo(
                    id="1",
                    titulo="The Last of Us",
                    plataforma="PlayStation",
                    genero="Ação/Aventura",
                    status="Finalizado",
                    nota=9.5,
                    descricao="Um dos melhores jogos que já joguei.",
                    id_usuario=id_usuario
                ),
                Jogo(
                    id="2",
                    titulo="Cyberpunk 2077",
                    plataforma="PC",
                    genero="RPG",
                    status="Jogando",
                    nota=8.0,
                    descricao="Mundo aberto impressionante.",
                    id_usuario=id_usuario
                ),
                Jogo(
                    id="3",
                    titulo="Zelda: Breath of the Wild",
                    plataforma="Nintendo Switch",
                    genero="Aventura",
                    status="Finalizado",
                    nota=10.0,
                    descricao="Revolucionário.",
                    id_usuario=id_usuario
                )
            ]
            
        print(f"[MODEL] Buscando jogos para o usuário {id_usuario}: {len(jogos)} jogos encontrados")
        return jogos
    
    def to_dict(self):
        """
        Converte o objeto Jogo em um dicionário.
        
        Returns:
            dict: Dicionário com os dados do jogo.
        """
        return {
            '_id': self._id,
            'titulo': self._titulo,
            'plataforma': self._plataforma,
            'genero': self._genero,
            'status': self._status,
            'nota': self._nota,
            'descricao': self._descricao,
            'id_usuario': self._id_usuario
        }
