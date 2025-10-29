from pymongo import MongoClient
from bson.objectid import ObjectId


class Usuario:
    # Gerencia dados e autenticação do usuário
    
    def __init__(self, id_user=None, nome="", email="", senha=""):
        self.id_user = id_user
        self.nome = nome
        self.email = email
        self.senha = senha
        self.db = MongoClient('mongodb://localhost:27017/')['gametracker_db']
    
    def cadastrar(self):
        # Cria novo usuário no banco
        try:
            usuarios = self.db['usuarios']
            
            # Verifica se email já existe
            if usuarios.find_one({'email': self.email}):
                return False, "Email já cadastrado"
            
            resultado = usuarios.insert_one({
                'nome': self.nome,
                'email': self.email,
                'senha': self.senha
            })
            
            self.id_user = str(resultado.inserted_id)
            return True, "Usuário cadastrado com sucesso"
        
        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"
    
    def autenticar(self):
        # Valida email e senha
        try:
            usuarios = self.db['usuarios']
            
            user = usuarios.find_one({'email': self.email})
            
            if not user:
                return False, None, "Email não encontrado"
            
            if user['senha'] == self.senha:
                user_id = str(user['_id'])
                
                # Cria jogos de exemplo no primeiro login
                from models.jogo import Jogo
                Jogo().criar_jogos_exemplo(user_id)
                
                return True, user_id, "Login realizado com sucesso"
            else:
                return False, None, "Senha incorreta"
        
        except Exception as e:
            return False, None, f"Erro ao autenticar: {str(e)}"