"""
Classe Model para Usuario no GameTracker.
"""

import hashlib
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson.objectid import ObjectId

class Usuario:
    """
    Classe que representa um usuário no sistema.
    Responsável por gerenciar os dados do usuário e a comunicação com o banco de dados.
    """
    
    # Configurações do MongoDB
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DATABASE = 'gametracker'
    
    # Variáveis de classe para compartilhar a conexão entre instâncias
    _client = None
    _db = None
    
    @classmethod
    def _conectar_db(cls):
        """
        Estabelece a conexão com o MongoDB.
        
        Returns:
            bool: True se a conexão foi estabelecida com sucesso, False caso contrário.
        """
        if cls._client is not None:
            return True
            
        try:
            # Criar a conexão com o MongoDB
            cls._client = MongoClient(cls.MONGODB_HOST, cls.MONGODB_PORT)
            
            # Verificar se a conexão está funcionando
            cls._client.admin.command('ping')
            
            # Selecionar o banco de dados
            cls._db = cls._client[cls.MONGODB_DATABASE]
            
            # Criar índice único para email (se ainda não existir)
            cls._db.usuarios.create_index([('email', 1)], unique=True)
            
            print(f"[MODEL] Conexão estabelecida com o MongoDB ({cls.MONGODB_HOST}:{cls.MONGODB_PORT}/{cls.MONGODB_DATABASE})")
            return True
        except ConnectionFailure:
            print(f"[MODEL] Falha ao conectar ao MongoDB ({cls.MONGODB_HOST}:{cls.MONGODB_PORT})")
            cls._client = None
            cls._db = None
            return False
        except Exception as e:
            print(f"[MODEL] Erro ao conectar ao MongoDB: {str(e)}")
            cls._client = None
            cls._db = None
            return False
    
    @classmethod
    def fechar_conexao(cls):
        """
        Fecha a conexão com o MongoDB.
        """
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("[MODEL] Conexão com o MongoDB fechada")
    
    @classmethod
    def inicializar_db_com_dados_exemplo(cls):
        """
        Inicializa o banco de dados com dados de exemplo.
        
        Returns:
            dict: Dicionário com informações sobre o usuário de exemplo criado.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not cls._conectar_db():
            print("[MODEL] Falha ao inicializar banco de dados: sem conexão com o banco de dados")
            return None
        
        try:
            # Limpar coleções existentes
            cls._db.usuarios.drop()
            cls._db.jogos.drop()
            
            print("[MODEL] Coleções existentes removidas.")
            
            # Criar índices
            cls._db.usuarios.create_index([('email', 1)], unique=True)
            
            print("[MODEL] Índices criados.")
            
            # Criar usuário de exemplo
            usuario_id = ObjectId()
            senha = "123456"
            senha_hash = cls._gerar_hash_senha_estatico(senha)
            
            usuario = {
                '_id': usuario_id,
                'nome': 'Usuário de Teste',
                'email': 'teste@exemplo.com',
                'senha_hash': senha_hash
            }
            
            cls._db.usuarios.insert_one(usuario)
            
            print(f"[MODEL] Usuário de exemplo criado: {usuario['nome']} ({usuario['email']})")
            
            # Importar a classe Jogo aqui para evitar importação circular
            from .jogo import Jogo
            
            # Criar jogos de exemplo
            Jogo.criar_jogos_exemplo(str(usuario_id))
            
            print("\n[MODEL] Banco de dados inicializado com sucesso!")
            
            # Retornar informações do usuário de exemplo
            return {
                'email': usuario['email'],
                'senha': senha,
                'id': str(usuario_id)
            }
            
        except Exception as e:
            print(f"[MODEL] Erro ao inicializar banco de dados: {str(e)}")
            return None
    
    @staticmethod
    def _gerar_hash_senha_estatico(senha):
        """
        Gera um hash para a senha (método estático).
        
        Args:
            senha (str): Senha em texto plano.
            
        Returns:
            str: Hash da senha.
        """
        # Usar SHA-256 para gerar o hash da senha
        return hashlib.sha256(senha.encode()).hexdigest()
    
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
        
        # Garantir que a conexão com o banco de dados esteja estabelecida
        self.__class__._conectar_db()
        
    @property
    def id(self):
        return self._id
        
    @property
    def nome(self):
        return self._nome
        
    @property
    def email(self):
        return self._email
    
    def _gerar_hash_senha(self, senha):
        """
        Gera um hash para a senha.
        
        Args:
            senha (str): Senha em texto plano.
            
        Returns:
            str: Hash da senha.
        """
        # Usar SHA-256 para gerar o hash da senha
        return hashlib.sha256(senha.encode()).hexdigest()
    
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
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao cadastrar usuário: sem conexão com o banco de dados")
            return False
        
        # Gerar o hash da senha
        senha_hash = self._gerar_hash_senha(senha)
        
        # Criar o documento do usuário
        usuario_doc = {
            'nome': nome,
            'email': email,
            'senha_hash': senha_hash
        }
        
        try:
            # Inserir o usuário no banco de dados
            resultado = self.__class__._db.usuarios.insert_one(usuario_doc)
            
            # Verificar se a inserção foi bem-sucedida
            if resultado.inserted_id:
                self._id = str(resultado.inserted_id)
                self._nome = nome
                self._email = email
                self._senha_hash = senha_hash
                print(f"[MODEL] Usuário cadastrado: {nome} ({email})")
                return True
            else:
                print(f"[MODEL] Falha ao cadastrar usuário: {nome} ({email})")
                return False
                
        except DuplicateKeyError:
            print(f"[MODEL] Falha ao cadastrar usuário: email já existe ({email})")
            return False
        except Exception as e:
            print(f"[MODEL] Erro ao cadastrar usuário: {str(e)}")
            return False
    
    def autenticar(self, email, senha):
        """
        Autentica um usuário no sistema.
        
        Args:
            email (str): Email do usuário.
            senha (str): Senha do usuário.
            
        Returns:
            bool: True se a autenticação foi bem-sucedida, False caso contrário.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao autenticar usuário: sem conexão com o banco de dados")
            return False
        
        try:
            # Gerar o hash da senha
            senha_hash = self._gerar_hash_senha(senha)
            
            # Buscar o usuário no banco de dados
            usuario = self.__class__._db.usuarios.find_one({
                'email': email,
                'senha_hash': senha_hash
            })
            
            # Verificar se o usuário foi encontrado
            if usuario:
                self._id = str(usuario['_id'])
                self._nome = usuario['nome']
                self._email = usuario['email']
                self._senha_hash = usuario['senha_hash']
                print(f"[MODEL] Usuário autenticado: {self._nome} ({email})")
                return True
            else:
                print(f"[MODEL] Falha na autenticação: {email}")
                return False
                
        except Exception as e:
            print(f"[MODEL] Erro ao autenticar usuário: {str(e)}")
            return False
    
    def buscar_jogos(self):
        """
        Busca os jogos do usuário.
        
        Returns:
            list: Lista de objetos Jogo do usuário.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao buscar jogos: sem conexão com o banco de dados")
            return []
        
        # Verificar se o usuário está autenticado
        if not self._id:
            print("[MODEL] Falha ao buscar jogos: usuário não autenticado")
            return []
        
        try:
            # Importar a classe Jogo aqui para evitar importação circular
            from .jogo import Jogo
            
            # Buscar os jogos do usuário
            jogos_docs = self.__class__._db.jogos.find({'id_usuario': self._id})
            
            # Converter os documentos em objetos Jogo
            jogos = []
            for doc in jogos_docs:
                jogo = Jogo(
                    id=str(doc['_id']),
                    titulo=doc.get('titulo'),
                    plataforma=doc.get('plataforma'),
                    genero=doc.get('genero'),
                    status=doc.get('status'),
                    nota=doc.get('nota'),
                    descricao=doc.get('descricao'),
                    id_usuario=doc.get('id_usuario')
                )
                jogos.append(jogo)
            
            print(f"[MODEL] Buscando jogos para o usuário {self._id}: {len(jogos)} jogos encontrados")
            return jogos
            
        except Exception as e:
            print(f"[MODEL] Erro ao buscar jogos: {str(e)}")
            return []
    
    def salvar(self):
        """
        Salva os dados do usuário no banco de dados.
        
        Returns:
            bool: True se o salvamento foi bem-sucedido, False caso contrário.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao salvar usuário: sem conexão com o banco de dados")
            return False
        
        try:
            # Criar o documento do usuário
            usuario_doc = {
                'nome': self._nome,
                'email': self._email,
                'senha_hash': self._senha_hash
            }
            
            if self._id:
                # Atualizar um usuário existente
                resultado = self.__class__._db.usuarios.update_one(
                    {'_id': ObjectId(self._id)},
                    {'$set': usuario_doc}
                )
                sucesso = resultado.modified_count > 0
            else:
                # Inserir um novo usuário
                resultado = self.__class__._db.usuarios.insert_one(usuario_doc)
                if resultado.inserted_id:
                    self._id = str(resultado.inserted_id)
                    sucesso = True
                else:
                    sucesso = False
            
            if sucesso:
                print(f"[MODEL] Usuário salvo: {self._nome} ({self._email})")
            else:
                print(f"[MODEL] Falha ao salvar usuário: {self._nome} ({self._email})")
            
            return sucesso
            
        except Exception as e:
            print(f"[MODEL] Erro ao salvar usuário: {str(e)}")
            return False
    
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
