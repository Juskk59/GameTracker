from bson.objectid import ObjectId
from pymongo import MongoClient
import base64
import os
from datetime import datetime


class Jogo:
    # Gerencia jogos da biblioteca do usuário
    
    PLATAFORMAS = [
        "PlayStation 5", "PlayStation 4", "Xbox Series X/S",
        "Xbox One", "Nintendo Switch", "PC", "Mobile"
    ]
    
    def __init__(self, id_jogo=None, titulo="", plataforma="", nota=0.0, 
                 descricao="", id_user="", imagem_jogo=None):
        self.id_jogo = id_jogo
        self.titulo = titulo
        self.plataforma = plataforma
        self.nota = nota
        self.descricao = descricao
        self.id_user = id_user
        self.imagem_jogo = imagem_jogo
        self.db = MongoClient('mongodb://localhost:27017/')['gametracker_db']
    
    def criar_jogos_exemplo(self, id_user):
        # Insere 3 jogos de exemplo na primeira vez
        try:
            jogos = self.db['jogos']
            
            # Evita duplicatas se usuário já tem jogos
            if jogos.count_documents({'id_user': ObjectId(id_user)}) > 0:
                return True
            
            jogos_exemplo = [
                {
                    'titulo': 'The Last of Us Part I',
                    'plataforma': 'PlayStation 5',
                    'nota': 9.5,
                    'descricao': 'Um dos melhores jogos que já joguei. História emocionante e gameplay incrível.',
                    'id_user': ObjectId(id_user),
                    'imagem_jogo': None
                },
                {
                    'titulo': 'Elden Ring',
                    'plataforma': 'PC',
                    'nota': 9.0,
                    'descricao': 'Mundo aberto impressionante com gameplay desafiador e lore profunda.',
                    'id_user': ObjectId(id_user),
                    'imagem_jogo': None
                },
                {
                    'titulo': 'Zelda: Tears of the Kingdom',
                    'plataforma': 'Nintendo Switch',
                    'nota': 10.0,
                    'descricao': 'Revolucionário. Liberdade total de exploração e criatividade.',
                    'id_user': ObjectId(id_user),
                    'imagem_jogo': None
                }
            ]
            
            jogos.insert_many(jogos_exemplo)
            return True
        
        except Exception as e:
            print(f"Erro ao criar jogos de exemplo: {str(e)}")
            return False
    
    def salvar(self):
        # Salva ou atualiza um jogo
        try:
            jogos = self.db['jogos']
            
            if not self.titulo or not self.plataforma:
                return False, "Título e plataforma são obrigatórios"
            
            if self.nota < 0 or self.nota > 10:
                return False, "Nota deve estar entre 0 e 10"
            
            dados = {
                'titulo': self.titulo,
                'plataforma': self.plataforma,
                'nota': self.nota,
                'descricao': self.descricao,
                'id_user': ObjectId(self.id_user),
                'imagem_jogo': self.imagem_jogo
            }
            
            if self.id_jogo:
                # Atualiza jogo existente
                jogos.update_one({'_id': ObjectId(self.id_jogo)}, {'$set': dados})
                return True, "Jogo atualizado com sucesso"
            else:
                # Cria novo jogo
                resultado = jogos.insert_one(dados)
                self.id_jogo = str(resultado.inserted_id)
                return True, "Jogo adicionado com sucesso"
        
        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}"
    
    def excluir(self):
        # Remove jogo do banco
        try:
            if not self.id_jogo:
                return False, "ID do jogo não informado"
            
            jogos = self.db['jogos']
            resultado = jogos.delete_one({'_id': ObjectId(self.id_jogo)})
            
            if resultado.deleted_count > 0:
                return True, "Jogo excluído com sucesso"
            else:
                return False, "Jogo não encontrado"
        
        except Exception as e:
            return False, f"Erro ao excluir: {str(e)}"
    
    def buscar_jogos(self, id_user):
        # Retorna todos os jogos do usuário
        try:
            jogos = self.db['jogos']
            return list(jogos.find({'id_user': ObjectId(id_user)}))
        except Exception as e:
            print(f"Erro ao buscar jogos: {str(e)}")
            return []
    
    def obter_estatisticas(self, id_user):
        # Calcula total e média de notas dos jogos
        try:
            jogos = self.db['jogos']
            user_jogos = list(jogos.find({'id_user': ObjectId(id_user)}))
            
            total = len(user_jogos)
            media_nota = sum([j.get('nota', 0) for j in user_jogos]) / total if total > 0 else 0
            
            return {'total': total, 'media': round(media_nota, 2)}
        
        except Exception as e:
            print(f"Erro ao obter estatísticas: {str(e)}")
            return {'total': 0, 'media': 0}
    
    def converter_imagem_para_base64(self, caminho_imagem):
        # Converte imagem em arquivo base64 para armazenar no banco
        try:
            with open(caminho_imagem, 'rb') as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Erro ao converter imagem: {str(e)}")
            return None
    
    def salvar_imagem_em_assets(self, caminho_origem):
        # Copia imagem para pasta assets com nome único
        try:
            import shutil
            
            pasta_assets = 'assets/imagens'
            if not os.path.exists(pasta_assets):
                os.makedirs(pasta_assets)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            nome_arquivo = timestamp + os.path.basename(caminho_origem)
            caminho_destino = os.path.join(pasta_assets, nome_arquivo)
            
            shutil.copy(caminho_origem, caminho_destino)
            return caminho_destino
        except Exception as e:
            print(f"Erro ao salvar imagem: {str(e)}")
            return None