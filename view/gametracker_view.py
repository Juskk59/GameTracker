import tkinter as tk
from tkinter import messagebox, ttk

class GameTrackerView:

    def __init__(self):
        """
        Inicializa a janela principal da aplicação.
        """
        self.root = tk.Tk()
        self.root.title("GameTracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#4682B4")  # Azul aço, como nos protótipos
        
        # Referência para o controller (será definida posteriormente)
        self.controller = None
        
        # Container principal para as telas
        self.container = tk.Frame(self.root, bg="#4682B4")
        self.container.pack(fill="both", expand=True)
        
        # Dicionário para armazenar as telas
        self.frames = {}
        
        # Variáveis para armazenar dados temporários
        self.current_user = None
        self.current_game = None
    
    def set_controller(self, controller):
        """
        Define o controller para esta view.
        
        Args:
            controller: Instância do GameTrackerController
        """
        self.controller = controller
    
    def mostrar_tela_login(self):
        """
        Exibe a tela de login.
        """
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Título
        titulo = tk.Label(self.container, text="GameTracker", font=("Arial", 24), bg="#4682B4", fg="white")
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(self.container, text="Login", font=("Arial", 18), bg="#4682B4", fg="white")
        subtitulo.pack(pady=10)
        
        # Frame para os campos de entrada
        frame_login = tk.Frame(self.container, bg="#4682B4")
        frame_login.pack(pady=30)
        
        # Campo de email
        tk.Label(frame_login, text="Email:", bg="#4682B4", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(frame_login, width=30)
        self.email_entry.grid(row=0, column=1, pady=5)
        
        # Campo de senha
        tk.Label(frame_login, text="Senha:", bg="#4682B4", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.senha_entry = tk.Entry(frame_login, width=30, show="*")
        self.senha_entry.grid(row=1, column=1, pady=5)
        
        # Frame para os botões
        frame_botoes = tk.Frame(self.container, bg="#4682B4")
        frame_botoes.pack(pady=20)
        
        # Botão de entrar
        btn_entrar = tk.Button(
            frame_botoes, 
            text="Entrar", 
            command=self.processar_login,
            bg="#32CD32",  # Verde lima
            fg="white",
            width=15
        )
        btn_entrar.pack(pady=10)
        
        # Botão de cadastro
        btn_cadastro = tk.Button(
            frame_botoes, 
            text="Criar cadastro", 
            command=self.mostrar_tela_cadastro,
            bg="#32CD32",  # Verde lima
            fg="white",
            width=15
        )
        btn_cadastro.pack(pady=5)
    
    def processar_login(self):
        """
        Processa o login quando o botão Entrar é clicado.
        """
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        
        if not email or not senha:
            self.exibir_mensagem("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Chama o controller para autenticar
        if self.controller:
            self.controller.lidar_login(email, senha)
    
    def mostrar_tela_cadastro(self):
        """
        Exibe a tela de cadastro de usuário.
        """
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Título
        titulo = tk.Label(self.container, text="GameTracker", font=("Arial", 24), bg="#4682B4", fg="white")
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(self.container, text="Registro", font=("Arial", 18), bg="#4682B4", fg="white")
        subtitulo.pack(pady=10)
        
        # Frame para os campos de entrada
        frame_cadastro = tk.Frame(self.container, bg="#4682B4")
        frame_cadastro.pack(pady=30)
        
        # Campo de nome
        tk.Label(frame_cadastro, text="Nome:", bg="#4682B4", fg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.nome_entry = tk.Entry(frame_cadastro, width=30)
        self.nome_entry.grid(row=0, column=1, pady=5)
        
        # Campo de email
        tk.Label(frame_cadastro, text="Email:", bg="#4682B4", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.email_cadastro_entry = tk.Entry(frame_cadastro, width=30)
        self.email_cadastro_entry.grid(row=1, column=1, pady=5)
        
        # Campo de senha
        tk.Label(frame_cadastro, text="Senha:", bg="#4682B4", fg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.senha_cadastro_entry = tk.Entry(frame_cadastro, width=30, show="*")
        self.senha_cadastro_entry.grid(row=2, column=1, pady=5)
        
        # Campo de confirmação de senha
        tk.Label(frame_cadastro, text="Confirme a Senha:", bg="#4682B4", fg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.confirma_senha_entry = tk.Entry(frame_cadastro, width=30, show="*")
        self.confirma_senha_entry.grid(row=3, column=1, pady=5)
        
        # Frame para os botões
        frame_botoes = tk.Frame(self.container, bg="#4682B4")
        frame_botoes.pack(pady=20)
        
        # Botão de cadastrar
        btn_cadastrar = tk.Button(
            frame_botoes, 
            text="Cadastrar", 
            command=self.processar_cadastro,
            bg="#32CD32",  # Verde lima
            fg="white",
            width=15
        )
        btn_cadastrar.pack(pady=10)
        
        # Botão de voltar ao login
        btn_voltar = tk.Button(
            frame_botoes, 
            text="Já possuo conta", 
            command=self.mostrar_tela_login,
            bg="#32CD32",  # Verde lima
            fg="white",
            width=15
        )
        btn_voltar.pack(pady=5)
    
    def processar_cadastro(self):
        """
        Processa o cadastro quando o botão Cadastrar é clicado.
        """
        nome = self.nome_entry.get()
        email = self.email_cadastro_entry.get()
        senha = self.senha_cadastro_entry.get()
        confirma_senha = self.confirma_senha_entry.get()
        
        if not nome or not email or not senha or not confirma_senha:
            self.exibir_mensagem("Erro", "Por favor, preencha todos os campos.")
            return
        
        if senha != confirma_senha:
            self.exibir_mensagem("Erro", "As senhas não coincidem.")
            return
        
        # Chama o controller para cadastrar
        if self.controller:
            self.controller.lidar_cadastro(nome, email, senha)
    
    def mostrar_dashboard(self, jogos):
        """
        Exibe o dashboard com a biblioteca de jogos do usuário.
        
        Args:
            jogos: Lista de jogos do usuário
        """
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Título
        titulo = tk.Label(self.container, text="GameTracker", font=("Arial", 24), bg="#4682B4", fg="white")
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(self.container, text="Biblioteca - Jogos Avaliados", font=("Arial", 18), bg="#4682B4", fg="white")
        subtitulo.pack(pady=5)
        
        # Frame principal
        frame_principal = tk.Frame(self.container, bg="#4682B4")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para botões e estatísticas (lado esquerdo)
        frame_esquerdo = tk.Frame(frame_principal, bg="#4682B4")
        frame_esquerdo.pack(side="left", fill="y", padx=10)
        
        # Botão para adicionar novo jogo
        btn_adicionar = tk.Button(
            frame_esquerdo, 
            text="Adicionar novo Jogo", 
            command=lambda: self.mostrar_tela_jogo(),
            bg="#DDDDDD",
            width=20,
            height=2
        )
        btn_adicionar.pack(pady=10)
        
        # Frame para estatísticas
        frame_estatisticas = tk.Frame(frame_esquerdo, bg="#DDDDDD", padx=10, pady=10)
        frame_estatisticas.pack(pady=20, fill="x")
        
        tk.Label(frame_estatisticas, text="Estatísticas:", font=("Arial", 12, "bold"), bg="#DDDDDD").pack(anchor="w")
        
        # Calcular estatísticas
        num_jogos = len(jogos)
        media_notas = 0
        if num_jogos > 0:
            soma_notas = sum(jogo.get('nota', 0) for jogo in jogos)
            media_notas = soma_notas / num_jogos
        
        tk.Label(frame_estatisticas, text=f"Número de Jogos Avaliados: {num_jogos}", bg="#DDDDDD").pack(anchor="w", pady=5)
        tk.Label(frame_estatisticas, text=f"Média de Notas: {media_notas:.1f}", bg="#DDDDDD").pack(anchor="w")
        
        # Frame para a grade de jogos (lado direito)
        frame_jogos = tk.Frame(frame_principal, bg="#4682B4")
        frame_jogos.pack(side="right", fill="both", expand=True)
        
        # Criar grade de jogos (3x2)
        if not jogos:
            # Mensagem se não houver jogos
            tk.Label(
                frame_jogos, 
                text="Nenhum jogo cadastrado.\nClique em 'Adicionar novo Jogo' para começar.", 
                bg="#DDDDDD",
                font=("Arial", 12),
                width=40,
                height=10
            ).pack(pady=50)
        else:
            # Criar grade com os jogos
            row, col = 0, 0
            for jogo in jogos:
                frame_jogo = tk.Frame(frame_jogos, bg="#DDDDDD", width=200, height=150, padx=10, pady=10)
                frame_jogo.grid(row=row, column=col, padx=10, pady=10)
                frame_jogo.pack_propagate(False)  # Manter tamanho fixo
                
                # Título do jogo
                tk.Label(
                    frame_jogo, 
                    text=jogo.get('titulo', 'Sem título'),
                    font=("Arial", 12, "bold"),
                    bg="#DDDDDD"
                ).pack(pady=5)
                
                # Plataforma
                tk.Label(
                    frame_jogo, 
                    text=f"Plataforma: {jogo.get('plataforma', 'N/A')}",
                    bg="#DDDDDD"
                ).pack(anchor="w")
                
                # Nota
                tk.Label(
                    frame_jogo, 
                    text=f"Nota: {jogo.get('nota', 'N/A')}",
                    bg="#DDDDDD"
                ).pack(anchor="w")
                
                # Status
                tk.Label(
                    frame_jogo, 
                    text=f"Status: {jogo.get('status', 'N/A')}",
                    bg="#DDDDDD"
                ).pack(anchor="w")
                
                # Botões de editar e excluir
                frame_botoes_jogo = tk.Frame(frame_jogo, bg="#DDDDDD")
                frame_botoes_jogo.pack(pady=5)
                
                btn_editar = tk.Button(
                    frame_botoes_jogo,
                    text="Editar",
                    command=lambda j=jogo: self.mostrar_tela_jogo(j),
                    bg="#DDDDDD",
                    width=8
                )
                btn_editar.pack(side="left", padx=2)
                
                btn_excluir = tk.Button(
                    frame_botoes_jogo,
                    text="Excluir",
                    command=lambda j=jogo: self.confirmar_exclusao(j),
                    bg="#DDDDDD",
                    width=8
                )
                btn_excluir.pack(side="left", padx=2)
                
                # Atualizar índices da grade
                col += 1
                if col > 1:  # 2 colunas
                    col = 0
                    row += 1
    
    def mostrar_tela_jogo(self, jogo=None):
        """
        Exibe a tela de cadastro/edição de jogo.
        
        Args:
            jogo: Jogo a ser editado (None para novo jogo)
        """
        # Limpa o container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Título
        titulo = tk.Label(self.container, text="GameTracker", font=("Arial", 24), bg="#4682B4", fg="white")
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(
            self.container, 
            text="Adicionar Avaliação" if not jogo else "Editar Avaliação", 
            font=("Arial", 18), 
            bg="#4682B4", 
            fg="white"
        )
        subtitulo.pack(pady=5)
        
        # Frame principal
        frame_principal = tk.Frame(self.container, bg="#4682B4")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para imagem (lado esquerdo)
        frame_esquerdo = tk.Frame(frame_principal, bg="#4682B4")
        frame_esquerdo.pack(side="left", fill="y", padx=10)
        
        # Placeholder para imagem
        frame_imagem = tk.Frame(frame_esquerdo, bg="#DDDDDD", width=200, height=200)
        frame_imagem.pack(pady=10)
        frame_imagem.pack_propagate(False)  # Manter tamanho fixo
        
        tk.Label(
            frame_imagem, 
            text="Adicionar Suposta\nImagem do Jogo", 
            bg="#DDDDDD",
            font=("Arial", 10)
        ).pack(expand=True)
        
        # Botões de editar e excluir (apenas se estiver editando)
        if jogo:
            frame_botoes_acao = tk.Frame(frame_esquerdo, bg="#4682B4")
            frame_botoes_acao.pack(pady=10)
            
            btn_editar = tk.Button(
                frame_botoes_acao,
                text="Editar Avaliação",
                bg="#DDDDDD",
                width=15
            )
            btn_editar.pack(pady=5)
            
            btn_excluir = tk.Button(
                frame_botoes_acao,
                text="Excluir Avaliação",
                command=lambda: self.confirmar_exclusao(jogo),
                bg="#DDDDDD",
                width=15
            )
            btn_excluir.pack(pady=5)
        
        # Frame para formulário (lado direito)
        frame_direito = tk.Frame(frame_principal, bg="#4682B4")
        frame_direito.pack(side="right", fill="both", expand=True, padx=10)
        
        # Formulário
        # Campo de título
        tk.Label(frame_direito, text="Nome:", bg="#4682B4", fg="white").pack(anchor="w", pady=2)
        self.titulo_entry = tk.Entry(frame_direito, width=40)
        self.titulo_entry.pack(fill="x", pady=2)
        if jogo:
            self.titulo_entry.insert(0, jogo.get('titulo', ''))
        
        # Campo de plataforma
        tk.Label(frame_direito, text="Plataforma:", bg="#4682B4", fg="white").pack(anchor="w", pady=2)
        plataformas = ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile", "Outra"]
        self.plataforma_var = tk.StringVar()
        self.plataforma_combobox = ttk.Combobox(frame_direito, textvariable=self.plataforma_var, values=plataformas)
        self.plataforma_combobox.pack(fill="x", pady=2)
        if jogo:
            self.plataforma_var.set(jogo.get('plataforma', ''))
        
        # Campo de status
        tk.Label(frame_direito, text="Status:", bg="#4682B4", fg="white").pack(anchor="w", pady=2)
        status_opcoes = ["Jogando", "Finalizado", "Pausado", "Abandonado", "Quero Jogar"]
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(frame_direito, textvariable=self.status_var, values=status_opcoes)
        self.status_combobox.pack(fill="x", pady=2)
        if jogo:
            self.status_var.set(jogo.get('status', ''))
        
        # Campo de nota
        tk.Label(frame_direito, text="Nota (0-10):", bg="#4682B4", fg="white").pack(anchor="w", pady=2)
        self.nota_var = tk.DoubleVar()
        self.nota_scale = tk.Scale(frame_direito, from_=0, to=10, resolution=0.5, orient="horizontal", variable=self.nota_var)
        self.nota_scale.pack(fill="x", pady=2)
        if jogo:
            self.nota_var.set(jogo.get('nota', 5.0))
        
        # Campo de descrição
        tk.Label(frame_direito, text="Descrição:", bg="#4682B4", fg="white").pack(anchor="w", pady=2)
        self.descricao_text = tk.Text(frame_direito, width=40, height=5)
        self.descricao_text.pack(fill="both", expand=True, pady=2)
        if jogo:
            self.descricao_text.insert("1.0", jogo.get('descricao', ''))
        
        # Frame para botões
        frame_botoes = tk.Frame(frame_direito, bg="#4682B4")
        frame_botoes.pack(pady=10, fill="x")
        
        # Botão de salvar
        btn_salvar = tk.Button(
            frame_botoes, 
            text="Salvar Avaliação", 
            command=lambda: self.salvar_jogo(jogo),
            bg="#DDDDDD",
            width=15
        )
        btn_salvar.pack(side="right", padx=10)
        
        # Botão de voltar
        btn_voltar = tk.Button(
            frame_botoes, 
            text="Voltar", 
            command=self.voltar_para_dashboard,
            bg="#DDDDDD",
            width=15
        )
        btn_voltar.pack(side="left", padx=10)
    
    def salvar_jogo(self, jogo_existente=None):
        """
        Salva um jogo (novo ou existente).
        
        Args:
            jogo_existente: Jogo a ser atualizado (None para novo jogo)
        """
        # Obter dados do formulário
        titulo = self.titulo_entry.get()
        plataforma = self.plataforma_var.get()
        status = self.status_var.get()
        nota = self.nota_var.get()
        descricao = self.descricao_text.get("1.0", "end-1c")  # Obter texto sem o caractere de nova linha final
        
        if not titulo or not plataforma or not status:
            self.exibir_mensagem("Erro", "Por favor, preencha pelo menos o título, a plataforma e o status.")
            return
        
        # Criar dicionário com os dados do jogo
        dados_jogo = {
            'titulo': titulo,
            'plataforma': plataforma,
            'status': status,
            'nota': nota,
            'descricao': descricao
        }
        
        # Se for edição, incluir o ID do jogo existente
        if jogo_existente and '_id' in jogo_existente:
            dados_jogo['_id'] = jogo_existente['_id']
        
        # Chamar o controller para salvar
        if self.controller:
            if jogo_existente:
                self.controller.lidar_editar_jogo(jogo_existente.get('_id'), dados_jogo)
            else:
                self.controller.lidar_adicionar_jogo(dados_jogo)
    
    def confirmar_exclusao(self, jogo):
        """
        Confirma a exclusão de um jogo.
        
        Args:
            jogo: Jogo a ser excluído
        """
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o jogo '{jogo.get('titulo')}'?"):
            if self.controller:
                self.controller.lidar_excluir_jogo(jogo.get('_id'))
    
    def voltar_para_dashboard(self):
        """
        Volta para o dashboard.
        """
        if self.controller:
            self.controller.carregar_jogos_usuario()
    
    def exibir_mensagem(self, titulo, mensagem):
        """
        Exibe uma mensagem para o usuário.
        
        Args:
            titulo: Título da mensagem
            mensagem: Texto da mensagem
        """
        messagebox.showinfo(titulo, mensagem)
    
    def iniciar(self):
        """
        Inicia a aplicação exibindo a tela de login.
        """
        self.mostrar_tela_login()
        self.root.mainloop()
