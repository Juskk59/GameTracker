from pymongo import MongoClient
from bson.objectid import ObjectId
from models.usuario import Usuario
from models.jogo import Jogo


class GameTrackerController:
    # Controller que gerencia as requisições da View
    
    def __init__(self):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            self.db = client['gametracker_db']
            client.admin.command('ping')
            print("✓ Conexão com MongoDB estabelecida!")
            self.conectado = True
        except Exception as e:
            print(f"✗ Erro ao conectar: {str(e)}")
            self.db = None
            self.conectado = False
    
    def lidar_login(self, email, senha):
        # Processa login do usuário
        if not self.conectado:
            return False, None, "Banco de dados não conectado"
        usuario = Usuario(email=email, senha=senha)
        return usuario.autenticar()
    
    def lidar_cadastro(self, nome, email, senha):
        # Processa cadastro de novo usuário
        if not self.conectado:
            return False, "Banco de dados não conectado"
        usuario = Usuario(nome=nome, email=email, senha=senha)
        return usuario.cadastrar()
    
    def lidar_add_jogo(self, titulo, plataforma, nota, descricao, id_user, imagem_base64=None):
        # Adiciona novo jogo à biblioteca
        if not self.conectado:
            return False, "Banco de dados não conectado"
        jogo = Jogo(titulo=titulo, plataforma=plataforma, nota=nota,
                   descricao=descricao, id_user=id_user, imagem_jogo=imagem_base64)
        return jogo.salvar()
    
    def lidar_edit_jogo(self, id_jogo, titulo, plataforma, nota, descricao, imagem_base64=None):
        # Atualiza um jogo existente
        if not self.conectado:
            return False, "Banco de dados não conectado"
        
        try:
            jogos = self.db['jogos']
            
            dados = {
                'titulo': titulo,
                'plataforma': plataforma,
                'nota': nota,
                'descricao': descricao
            }
            
            # Só atualiza imagem se uma nova foi enviada
            if imagem_base64 is not None:
                dados['imagem_jogo'] = imagem_base64
            
            resultado = jogos.update_one({'_id': ObjectId(id_jogo)}, {'$set': dados})
            
            return (True, "Jogo atualizado com sucesso") if resultado.modified_count > 0 else (False, "Nenhuma alteração")
        
        except Exception as e:
            return False, f"Erro ao atualizar: {str(e)}"
    
    def lidar_excluir_jogo(self, id_jogo):
        # Remove jogo da biblioteca
        if not self.conectado:
            return False, "Banco de dados não conectado"
        jogo = Jogo(id_jogo=id_jogo)
        return jogo.excluir()
    
    def lidar_listar_jogos(self, id_user):
        # Busca todos os jogos do usuário
        if not self.conectado:
            return []
        jogo = Jogo()
        return jogo.buscar_jogos(id_user)
    
    def lidar_obter_estatisticas(self, id_user):
        # Calcula estatísticas da biblioteca
        if not self.conectado:
            return {'total': 0, 'media': 0}
        jogo = Jogo()
        return jogo.obter_estatisticas(id_user)
    
    def lidar_obter_plataformas(self):
        # Retorna lista de plataformas disponíveis
        return Jogo.PLATAFORMAS
    
    def lidar_converter_imagem(self, caminho_imagem):
        # Converte imagem para base64
        jogo = Jogo()
        return jogo.converter_imagem_para_base64(caminho_imagem)
    
    def lidar_salvar_imagem(self, caminho_origem):
        # Salva imagem em assets
        jogo = Jogo()
        return jogo.salvar_imagem_em_assets(caminho_origem)