"""
Classe Model para Usuario no GameTracker.
"""

class Usuario:
    """
    Classe que representa um usuário no sistema.
    Responsável por gerenciar os dados do usuário e a comunicação com o banco de dados.
    """
    
    def __init__(self, id=None, nome=None, email=None, senha_hash=None):
        """
        Inicializa um objeto Usuario.
        
        Args:
            id (str, opcional): ID do usuário no banco de dados.
            nome (str, opcional): Nome do usuário.
            email (str, opcional): Email do usuário.
            senha_hash (str, opcional): Hash da senha do usuário.
        """
        self._id = id
        self._nome = nome
        self._email = email
        self._senha_hash = senha_hash
        
    @property
    def id(self):
        return self._id
        
    @property
    def nome(self):
        return self._nome
        
    @property
    def email(self):
        return self._email
    
    def cadastrar(self, nome, email, senha):
        """
        Cadastra um novo usuário no sistema.
        
        Args:
            nome (str): Nome do usuário.
            email (str): Email do usuário.
            senha (str): Senha do usuário (será convertida em hash).
            
        Returns:
            bool: True se o cadastro foi bem-sucedido, False caso contrário.
        """
        # Em uma implementação real, verificaríamos se o email já existe
        # e salvaríamos os dados no MongoDB
        
        # Simulação de cadastro bem-sucedido
        self._nome = nome
        self._email = email
        self._senha_hash = f"hash_de_{senha}"  # Simulação de hash
        self._id = f"user_{email.replace('@', '_at_')}"  # ID simulado
        
        print(f"[MODEL] Usuário cadastrado: {nome} ({email})")
        return True
    
    def autenticar(self, email, senha):
        """
        Autentica um usuário no sistema.
        
        Args:
            email (str): Email do usuário.
            senha (str): Senha do usuário.
            
        Returns:
            bool: True se a autenticação foi bem-sucedida, False caso contrário.
        """
        # Em uma implementação real, buscaríamos o usuário no MongoDB
        # e verificaríamos a senha com o hash armazenado
        
        # Simulação de autenticação bem-sucedida se o email contiver "user"
        if "user" in email:
            self._email = email
            self._senha_hash = f"hash_de_{senha}"
            self._nome = f"Usuário {email.split('@')[0]}"
            self._id = f"user_{email.replace('@', '_at_')}"
            print(f"[MODEL] Usuário autenticado: {self._nome} ({email})")
            return True
        else:
            print(f"[MODEL] Falha na autenticação: {email}")
            return False
    
    def buscar_jogos(self):
        """
        Busca os jogos do usuário.
        
        Returns:
            list: Lista de jogos do usuário.
        """
        # Em uma implementação real, buscaríamos os jogos no MongoDB
        # usando o ID do usuário
        
        # Simulação de jogos
        from .jogo import Jogo
        
        jogos = []
        if self._id:
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
                    id_usuario=self._id
                ),
                Jogo(
                    id="2",
                    titulo="Cyberpunk 2077",
                    plataforma="PC",
                    genero="RPG",
                    status="Jogando",
                    nota=8.0,
                    descricao="Mundo aberto impressionante.",
                    id_usuario=self._id
                ),
                Jogo(
                    id="3",
                    titulo="Zelda: Breath of the Wild",
                    plataforma="Nintendo Switch",
                    genero="Aventura",
                    status="Finalizado",
                    nota=10.0,
                    descricao="Revolucionário.",
                    id_usuario=self._id
                )
            ]
            
        print(f"[MODEL] Buscando jogos para o usuário {self._id}: {len(jogos)} jogos encontrados")
        return jogos
    
    def salvar(self):
        """
        Salva os dados do usuário no banco de dados.
        
        Returns:
            bool: True se o salvamento foi bem-sucedido, False caso contrário.
        """
        # Em uma implementação real, salvaríamos os dados no MongoDB
        
        print(f"[MODEL] Salvando usuário: {self._nome} ({self._email})")
        return True
    
    def to_dict(self):
        """
        Converte o objeto Usuario em um dicionário.
        
        Returns:
            dict: Dicionário com os dados do usuário.
        """
        return {
            '_id': self._id,
            'nome': self._nome,
            'email': self._email,
            'senha_hash': self._senha_hash
        }
