"""
Classe Model para Jogo no GameTracker.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

class Jogo:
    """
    Classe que representa um jogo no sistema.
    Responsável por gerenciar os dados do jogo e a comunicação com o banco de dados.
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
    def criar_jogos_exemplo(cls, id_usuario):
        """
        Cria jogos de exemplo para um usuário.
        
        Args:
            id_usuario (str): ID do usuário para o qual criar os jogos.
            
        Returns:
            int: Número de jogos criados.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not cls._conectar_db():
            print("[MODEL] Falha ao criar jogos de exemplo: sem conexão com o banco de dados")
            return 0
        
        try:
            # Criar jogos de exemplo
            jogos = [
                {
                    '_id': ObjectId(),
                    'titulo': 'The Last of Us',
                    'plataforma': 'PlayStation',
                    'genero': 'Ação/Aventura',
                    'status': 'Finalizado',
                    'nota': 9.5,
                    'descricao': 'Um dos melhores jogos que já joguei. História emocionante e gameplay incrível.',
                    'id_usuario': id_usuario
                },
                {
                    '_id': ObjectId(),
                    'titulo': 'Cyberpunk 2077',
                    'plataforma': 'PC',
                    'genero': 'RPG',
                    'status': 'Jogando',
                    'nota': 8.0,
                    'descricao': 'Mundo aberto impressionante, apesar dos bugs.',
                    'id_usuario': id_usuario
                },
                {
                    '_id': ObjectId(),
                    'titulo': 'Zelda: Breath of the Wild',
                    'plataforma': 'Nintendo Switch',
                    'genero': 'Aventura',
                    'status': 'Finalizado',
                    'nota': 10.0,
                    'descricao': 'Revolucionário. Liberdade total de exploração.',
                    'id_usuario': id_usuario
                }
            ]
            
            # Inserir os jogos no banco de dados
            resultado = cls._db.jogos.insert_many(jogos)
            
            # Verificar se a inserção foi bem-sucedida
            if resultado.inserted_ids:
                print(f"[MODEL] {len(resultado.inserted_ids)} jogos de exemplo criados para o usuário {id_usuario}")
                return len(resultado.inserted_ids)
            else:
                print(f"[MODEL] Falha ao criar jogos de exemplo para o usuário {id_usuario}")
                return 0
                
        except Exception as e:
            print(f"[MODEL] Erro ao criar jogos de exemplo: {str(e)}")
            return 0
    
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
        
        # Garantir que a conexão com o banco de dados esteja estabelecida
        self.__class__._conectar_db()
    
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
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao salvar jogo: sem conexão com o banco de dados")
            return False
        
        # Verificar se o jogo tem um usuário associado
        if not self._id_usuario:
            print("[MODEL] Falha ao salvar jogo: sem usuário associado")
            return False
        
        try:
            # Criar o documento do jogo
            jogo_doc = {
                'titulo': self._titulo,
                'plataforma': self._plataforma,
                'genero': self._genero,
                'status': self._status,
                'nota': self._nota,
                'descricao': self._descricao,
                'id_usuario': self._id_usuario
            }
            
            if self._id:
                # Atualizar um jogo existente
                resultado = self.__class__._db.jogos.update_one(
                    {'_id': ObjectId(self._id)},
                    {'$set': jogo_doc}
                )
                sucesso = resultado.modified_count > 0
            else:
                # Inserir um novo jogo
                resultado = self.__class__._db.jogos.insert_one(jogo_doc)
                if resultado.inserted_id:
                    self._id = str(resultado.inserted_id)
                    sucesso = True
                else:
                    sucesso = False
            
            if sucesso:
                print(f"[MODEL] Jogo salvo: {self._titulo} (ID: {self._id})")
            else:
                print(f"[MODEL] Falha ao salvar jogo: {self._titulo}")
            
            return sucesso
            
        except Exception as e:
            print(f"[MODEL] Erro ao salvar jogo: {str(e)}")
            return False
    
    def excluir(self):
        """
        Exclui o jogo do banco de dados.
        
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not self.__class__._conectar_db():
            print("[MODEL] Falha ao excluir jogo: sem conexão com o banco de dados")
            return False
        
        # Verificar se o jogo tem um ID
        if not self._id:
            print("[MODEL] Falha ao excluir jogo: sem ID")
            return False
        
        try:
            # Excluir o jogo
            resultado = self.__class__._db.jogos.delete_one({'_id': ObjectId(self._id)})
            
            # Verificar se a exclusão foi bem-sucedida
            if resultado.deleted_count > 0:
                print(f"[MODEL] Jogo excluído: {self._titulo} (ID: {self._id})")
                return True
            else:
                print(f"[MODEL] Falha ao excluir jogo: {self._titulo} (ID: {self._id})")
                return False
                
        except Exception as e:
            print(f"[MODEL] Erro ao excluir jogo: {str(e)}")
            return False
    
    def atualizar(self, dados):
        """
        Atualiza os dados do jogo.
        
        Args:
            dados (dict): Dicionário com os novos dados do jogo.
            
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
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
            
        # Salvar as alterações no banco de dados
        return self.salvar()
    
    @staticmethod
    def buscar_todos_do_usuario(id_usuario):
        """
        Busca todos os jogos de um usuário.
        
        Args:
            id_usuario (str): ID do usuário.
            
        Returns:
            list: Lista de objetos Jogo.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not Jogo._conectar_db():
            print("[MODEL] Falha ao buscar jogos: sem conexão com o banco de dados")
            return []
        
        try:
            # Buscar os jogos do usuário
            jogos_docs = Jogo._db.jogos.find({'id_usuario': id_usuario})
            
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
            
            print(f"[MODEL] Buscando jogos para o usuário {id_usuario}: {len(jogos)} jogos encontrados")
            return jogos
            
        except Exception as e:
            print(f"[MODEL] Erro ao buscar jogos: {str(e)}")
            return []
    
    @staticmethod
    def buscar_por_id(id_jogo):
        """
        Busca um jogo pelo ID.
        
        Args:
            id_jogo (str): ID do jogo.
            
        Returns:
            Jogo: Objeto Jogo ou None se não encontrado.
        """
        # Verificar se a conexão com o banco de dados está estabelecida
        if not Jogo._conectar_db():
            print("[MODEL] Falha ao buscar jogo: sem conexão com o banco de dados")
            return None
        
        try:
            # Buscar o jogo pelo ID
            doc = Jogo._db.jogos.find_one({'_id': ObjectId(id_jogo)})
            
            # Verificar se o jogo foi encontrado
            if doc:
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
                return jogo
            else:
                print(f"[MODEL] Jogo não encontrado: ID {id_jogo}")
                return None
                
        except Exception as e:
            print(f"[MODEL] Erro ao buscar jogo: {str(e)}")
            return None
    
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
