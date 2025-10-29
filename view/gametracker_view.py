import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import base64


class GameTrackerView:
    # Interface gráfica da aplicação
    
    def __init__(self, controller):
        # Recebe controller já inicializado
        self.root = tk.Tk()
        self.root.title("GameTracker")
        self.root.geometry("750x650")
        self.root.configure(bg="#5B9FB5")
        
        self.controller = controller
        self.usuario_id = None
        self.imagem_selecionada = None
        self.imagem_exibida = None
        
        if not self.controller.conectado:
            messagebox.showerror("Erro", "Falha ao conectar ao MongoDB")
            self.root.destroy()
            return
        
        self.total_login()
    
    def limpar_tela(self):
        # Remove todos os widgets da tela
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def total_login(self):
        # Tela de login
        self.limpar_tela()
        
        frame_title = tk.Frame(self.root, bg="#5B9FB5")
        frame_title.pack(pady=40)
        
        tk.Label(frame_title, text="GameTracker", font=("Arial", 32, "bold"), 
                bg="#5B9FB5", fg="white").pack()
        tk.Label(frame_title, text="Login", font=("Arial", 20), 
                bg="#5B9FB5", fg="white").pack(pady=10)
        
        frame_form = tk.Frame(self.root, bg="#5B9FB5")
        frame_form.pack(pady=30)
        
        tk.Label(frame_form, text="Email", bg="#5B9FB5", fg="white", font=("Arial", 12)).pack()
        email_entry = tk.Entry(frame_form, width=35, font=("Arial", 11), bd=1)
        email_entry.pack(pady=10)
        
        tk.Label(frame_form, text="Senha", bg="#5B9FB5", fg="white", font=("Arial", 12)).pack()
        senha_entry = tk.Entry(frame_form, width=35, show="*", font=("Arial", 11), bd=1)
        senha_entry.pack(pady=10)
        
        tk.Button(frame_form, text="Entrar", bg="#7CB342", fg="white",
                 command=lambda: self.total_login_click(email_entry.get(), senha_entry.get()),
                 width=20, font=("Arial", 12), cursor="hand2", bd=0, pady=8).pack(pady=20)
        
        tk.Button(frame_form, text="Criar cadastro", bg="#7CB342", fg="white",
                 command=self.total_cadastro, width=20, font=("Arial", 12),
                 cursor="hand2", bd=0, pady=8).pack()
    
    def total_login_click(self, email, senha):
        # Valida e processa login
        if not email or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        
        sucesso, user_id, msg = self.controller.lidar_login(email, senha)
        if sucesso:
            self.usuario_id = user_id
            self.dashboard()
        else:
            messagebox.showerror("Erro", msg)
    
    def total_cadastro(self):
        # Tela de cadastro
        self.limpar_tela()
        
        frame_title = tk.Frame(self.root, bg="#5B9FB5")
        frame_title.pack(pady=30)
        
        tk.Label(frame_title, text="GameTracker", font=("Arial", 32, "bold"), 
                bg="#5B9FB5", fg="white").pack()
        tk.Label(frame_title, text="Registro", font=("Arial", 20), 
                bg="#5B9FB5", fg="white").pack(pady=10)
        
        frame_form = tk.Frame(self.root, bg="#5B9FB5")
        frame_form.pack(pady=20)
        
        tk.Label(frame_form, text="Nome", bg="#5B9FB5", fg="white", font=("Arial", 11)).pack()
        nome_entry = tk.Entry(frame_form, width=35, font=("Arial", 10), bd=1)
        nome_entry.pack(pady=8)
        
        tk.Label(frame_form, text="Email", bg="#5B9FB5", fg="white", font=("Arial", 11)).pack()
        email_entry = tk.Entry(frame_form, width=35, font=("Arial", 10), bd=1)
        email_entry.pack(pady=8)
        
        tk.Label(frame_form, text="Senha", bg="#5B9FB5", fg="white", font=("Arial", 11)).pack()
        senha_entry = tk.Entry(frame_form, width=35, show="*", font=("Arial", 10), bd=1)
        senha_entry.pack(pady=8)
        
        tk.Label(frame_form, text="Confirme a Senha", bg="#5B9FB5", fg="white", font=("Arial", 11)).pack()
        conf_senha_entry = tk.Entry(frame_form, width=35, show="*", font=("Arial", 10), bd=1)
        conf_senha_entry.pack(pady=8)
        
        tk.Button(frame_form, text="Cadastrar", bg="#7CB342", fg="white",
                 command=lambda: self.total_cadastro_click(nome_entry.get(), email_entry.get(),
                                                          senha_entry.get(), conf_senha_entry.get()),
                 width=20, font=("Arial", 11), cursor="hand2", bd=0, pady=8).pack(pady=15)
        
        tk.Button(frame_form, text="Voltar ao Login", bg="#7CB342", fg="white",
                 command=self.total_login, width=20, font=("Arial", 11),
                 cursor="hand2", bd=0, pady=8).pack()
    
    def total_cadastro_click(self, nome, email, senha, conf_senha):
        # Valida e processa cadastro
        if not nome or not email or not senha or not conf_senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        
        if senha != conf_senha:
            messagebox.showerror("Erro", "As senhas não conferem")
            return
        
        sucesso, msg = self.controller.lidar_cadastro(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.total_login()
        else:
            messagebox.showerror("Erro", msg)
    
    def dashboard(self):
        # Tela principal - biblioteca de jogos
        self.limpar_tela()
        
        frame_header = tk.Frame(self.root, bg="#5B9FB5")
        frame_header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_header, text="GameTracker\nBiblioteca - Jogos Avaliados", 
                font=("Arial", 16, "bold"), bg="#5B9FB5", fg="white", justify=tk.CENTER).pack()
        
        # Painel esquerdo
        frame_left = tk.Frame(self.root, bg="#5B9FB5", width=120)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)
        
        tk.Button(frame_left, text="Adicionar\nnovo Jogo", bg="white", fg="black",
                 command=self.obter_dados_jogo, font=("Arial", 9), cursor="hand2",
                 bd=1, padx=10, pady=10, wraplength=80).pack(pady=10)
        
        # Box de estatísticas
        frame_stats = tk.Frame(frame_left, bg="white", bd=1)
        frame_stats.pack(pady=10, fill=tk.BOTH, expand=False)
        
        tk.Label(frame_stats, text="Estatísticas:", font=("Arial", 10, "bold"), bg="white").pack(padx=5, pady=5)
        
        stats = self.controller.lidar_obter_estatisticas(self.usuario_id)
        
        tk.Label(frame_stats, text=f"Número de Jogos\nAvaliados:\n{stats['total']}", 
                font=("Arial", 9), bg="white", justify=tk.CENTER).pack(padx=5, pady=5)
        tk.Label(frame_stats, text=f"Nota Média:\n{stats['media']}", 
                font=("Arial", 9), bg="white", justify=tk.CENTER).pack(padx=5, pady=5)
        
        tk.Button(frame_left, text="Sair", bg="#E57373", fg="white",
                 command=self.fazer_logout, font=("Arial", 10), cursor="hand2",
                 bd=0, padx=15, pady=8).pack(pady=20)
        
        # Grid de jogos
        frame_center = tk.Frame(self.root, bg="#5B9FB5")
        frame_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_jogos = tk.Frame(frame_center, bg="#5B9FB5")
        frame_jogos.pack(fill=tk.BOTH, expand=True)
        
        jogos = self.controller.lidar_listar_jogos(self.usuario_id)
        
        for idx, jogo in enumerate(jogos):
            frame_jogo = tk.Frame(frame_jogos, bg="white", bd=1, width=150, height=180)
            frame_jogo.grid(row=idx//2, column=idx%2, padx=10, pady=10, sticky="nsew")
            
            # Exibe imagem ou placeholder
            if jogo.get('imagem_jogo'):
                try:
                    import io
                    img_data = base64.b64decode(jogo['imagem_jogo'])
                    img = Image.open(io.BytesIO(img_data))
                    photo = self.redimensionar_imagem_obj(img, (140, 140))
                    
                    if photo:
                        label_img = tk.Label(frame_jogo, image=photo, bg="white")
                        label_img.image = photo
                        label_img.pack(pady=10)
                    else:
                        self._criar_placeholder(frame_jogo)
                except:
                    self._criar_placeholder(frame_jogo)
            else:
                self._criar_placeholder(frame_jogo)
            
            frame_buttons = tk.Frame(frame_jogo, bg="white")
            frame_buttons.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Button(frame_buttons, text="Editar", bg="#7CB342", fg="white",
                     font=("Arial", 8), cursor="hand2", bd=0,
                     command=lambda id_j=str(jogo['_id']): self.obter_dados_jogo(id_j)).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            tk.Button(frame_buttons, text="Excluir", bg="#E57373", fg="white",
                     font=("Arial", 8), cursor="hand2", bd=0,
                     command=lambda id_j=str(jogo['_id']): self.confirmar_exclusao_direto(id_j)).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def confirmar_exclusao_direto(self, id_jogo):
        # Confirma exclusão do jogo
        if messagebox.askyesno("Confirmar", "Deseja excluir este jogo?"):
            sucesso, msg = self.controller.lidar_excluir_jogo(id_jogo)
            messagebox.showinfo("Resultado", msg)
            self.dashboard()
    
    def fazer_logout(self):
        # Desconecta usuário
        self.usuario_id = None
        self.imagem_selecionada = None
        self.total_login()
    
    def selecionar_imagem(self):
        # Abre seletor de arquivo para imagem
        arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"), ("Todos", "*.*")]
        )
        
        if arquivo:
            caminho_assets = self.controller.lidar_salvar_imagem(arquivo)
            if caminho_assets:
                self.imagem_selecionada = caminho_assets
                self.exibir_preview_imagem(caminho_assets)
            else:
                messagebox.showerror("Erro", "Não foi possível salvar a imagem")
    
    def _criar_placeholder(self, frame):
        # Placeholder para quando não há imagem
        tk.Label(frame, text="Imagem\ndos\nJogos", bg="white",
                font=("Arial", 9), width=17, height=7).pack(pady=10)
    
    def redimensionar_imagem_obj(self, img_obj, tamanho=(140, 140)):
        # Redimensiona imagem mantendo proporção
        try:
            ratio = min(tamanho[0] / img_obj.width, tamanho[1] / img_obj.height)
            nova_width = int(img_obj.width * ratio)
            nova_height = int(img_obj.height * ratio)
            
            img = img_obj.resize((nova_width, nova_height), Image.Resampling.LANCZOS)
            imagem_final = Image.new('RGB', tamanho, (255, 255, 255))
            x = (tamanho[0] - nova_width) // 2
            y = (tamanho[1] - nova_height) // 2
            imagem_final.paste(img, (x, y))
            
            return ImageTk.PhotoImage(imagem_final)
        except Exception as e:
            print(f"Erro ao processar imagem: {str(e)}")
            return None
    
    def redimensionar_imagem(self, caminho_imagem, tamanho=(140, 140)):
        # Carrega imagem do arquivo
        try:
            img = Image.open(caminho_imagem)
            img = img.convert("RGB")
            return self.redimensionar_imagem_obj(img, tamanho)
        except Exception as e:
            print(f"Erro ao redimensionar: {str(e)}")
            return None
    
    def exibir_preview_imagem(self, caminho_imagem):
        # Exibe preview da imagem selecionada
        try:
            photo = self.redimensionar_imagem(caminho_imagem, (160, 160))
            
            if photo and hasattr(self, 'label_imagem'):
                self.imagem_exibida = photo
                self.label_imagem.config(image=self.imagem_exibida, width=160, height=160)
                self.label_imagem.image = photo
            
            if hasattr(self, 'btn_adicionar_img'):
                self.btn_adicionar_img.config(text="✓ Imagem\nselecionada")
        except Exception as e:
            print(f"Erro ao exibir imagem: {str(e)}")
    
    def exibir_preview_imagem_base64(self, base64_string):
        # Exibe preview de imagem em base64 (do banco)
        try:
            import io
            img_data = base64.b64decode(base64_string)
            img = Image.open(io.BytesIO(img_data))
            
            ratio = min(160 / img.width, 160 / img.height)
            nova_width = int(img.width * ratio)
            nova_height = int(img.height * ratio)
            img = img.resize((nova_width, nova_height), Image.Resampling.LANCZOS)
            
            imagem_final = Image.new('RGB', (160, 160), (255, 255, 255))
            x = (160 - nova_width) // 2
            y = (160 - nova_height) // 2
            imagem_final.paste(img, (x, y))
            
            self.imagem_exibida = ImageTk.PhotoImage(imagem_final)
            
            if hasattr(self, 'label_imagem'):
                self.label_imagem.config(image=self.imagem_exibida, width=160, height=160)
                self.label_imagem.image = self.imagem_exibida
        except Exception as e:
            print(f"Erro ao exibir base64: {str(e)}")
    
    def obter_dados_jogo(self, id_jogo=None):
        # Tela para adicionar ou editar jogo
        self.limpar_tela()
        self.imagem_selecionada = None
        self.imagem_exibida = None
        
        frame_title = tk.Frame(self.root, bg="#5B9FB5")
        frame_title.pack(pady=15)
        
        tk.Label(frame_title, text="GameTracker\nAdicionar Avaliação", 
                font=("Arial", 16, "bold"), bg="#5B9FB5", fg="white", justify=tk.CENTER).pack()
        
        frame_main = tk.Frame(self.root, bg="#5B9FB5")
        frame_main.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Lado esquerdo - imagem
        frame_left = tk.Frame(frame_main, bg="#5B9FB5")
        frame_left.pack(side=tk.LEFT, padx=10, fill=tk.BOTH)
        
        self.label_imagem = tk.Label(frame_left, text="Imagem do Jogo", bg="white", 
                                    width=20, height=12, font=("Arial", 10))
        self.label_imagem.pack(pady=5)
        
        self.btn_adicionar_img = tk.Button(frame_left, text="Adicionar\nimagem", bg="white", 
                                          fg="black", command=self.selecionar_imagem, font=("Arial", 9),
                                          cursor="hand2", bd=1, padx=10, pady=8, wraplength=80)
        self.btn_adicionar_img.pack(pady=5)
        
        # Lado direito - formulário
        frame_right = tk.Frame(frame_main, bg="#5B9FB5")
        frame_right.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_right, text="Nome", bg="#5B9FB5", fg="white", font=("Arial", 10)).pack(anchor=tk.W)
        titulo_entry = tk.Entry(frame_right, width=35, font=("Arial", 10), bd=1)
        titulo_entry.pack(pady=5, fill=tk.X)
        
        tk.Label(frame_right, text="Plataforma", bg="#5B9FB5", fg="white", font=("Arial", 10)).pack(anchor=tk.W)
        
        frame_plataformas = tk.Frame(frame_right, bg="#5B9FB5")
        frame_plataformas.pack(pady=5, fill=tk.X)
        
        plataformas = self.controller.lidar_obter_plataformas()
        plataforma_var = tk.StringVar()
        
        # Cria radiobuttons para plataformas
        for plat in plataformas:
            tk.Radiobutton(frame_plataformas, text=plat, variable=plataforma_var, value=plat,
                          bg="#5B9FB5", fg="white", selectcolor="#7CB342", font=("Arial", 9)).pack(anchor=tk.W)
        
        tk.Label(frame_right, text="Nota", bg="#5B9FB5", fg="white", font=("Arial", 10)).pack(anchor=tk.W)
        nota_var = tk.DoubleVar(value=0.0)
        tk.Scale(frame_right, from_=0, to=10, orient=tk.HORIZONTAL, variable=nota_var, 
                bg="#7CB342", fg="white", highlightthickness=0).pack(pady=5, fill=tk.X)
        
        tk.Label(frame_right, text="Descrição", bg="#5B9FB5", fg="white", font=("Arial", 10)).pack(anchor=tk.W)
        descricao_text = tk.Text(frame_right, width=35, height=5, font=("Arial", 9), bd=1)
        descricao_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Carrega dados se for edição
        if id_jogo:
            jogos = self.controller.lidar_listar_jogos(self.usuario_id)
            jogo = next((j for j in jogos if str(j['_id']) == id_jogo), None)
            
            if jogo:
                titulo_entry.insert(0, jogo['titulo'])
                plataforma_var.set(jogo['plataforma'])
                nota_var.set(jogo['nota'])
                descricao_text.insert("1.0", jogo['descricao'])
                
                if jogo.get('imagem_jogo'):
                    try:
                        self.exibir_preview_imagem_base64(jogo['imagem_jogo'])
                        self.imagem_selecionada = None
                    except:
                        pass
        
        # Botões
        frame_buttons = tk.Frame(self.root, bg="#5B9FB5")
        frame_buttons.pack(pady=10)
        
        if id_jogo:
            tk.Button(frame_buttons, text="Salvar Avaliação", bg="#7CB342", fg="white",
                     command=lambda: self.salvar_edicao(id_jogo, titulo_entry.get(),
                                                       plataforma_var.get(), nota_var.get(),
                                                       descricao_text.get("1.0", tk.END)),
                     font=("Arial", 10), cursor="hand2", bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
            
            tk.Button(frame_buttons, text="Excluir Avaliação", bg="#E57373", fg="white",
                     command=lambda: self.confirmar_exclusao(id_jogo),
                     font=("Arial", 10), cursor="hand2", bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        else:
            tk.Button(frame_buttons, text="Salvar Avaliação", bg="#7CB342", fg="white",
                     command=lambda: self.salvar_novo(titulo_entry.get(), plataforma_var.get(),
                                                      nota_var.get(), descricao_text.get("1.0", tk.END)),
                     font=("Arial", 10), cursor="hand2", bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_buttons, text="Voltar", bg="#7CB342", fg="white",
                 command=self.dashboard, font=("Arial", 10), cursor="hand2",
                 bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    def salvar_novo(self, titulo, plataforma, nota, descricao):
        # Salva novo jogo
        if not titulo or not plataforma:
            messagebox.showwarning("Aviso", "Preencha pelo menos título e plataforma")
            return
        
        imagem_base64 = None
        if self.imagem_selecionada:
            imagem_base64 = self.controller.lidar_converter_imagem(self.imagem_selecionada)
        
        sucesso, msg = self.controller.lidar_add_jogo(
            titulo, plataforma, nota, descricao.strip(), self.usuario_id, imagem_base64
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.dashboard()
        else:
            messagebox.showerror("Erro", msg)
    
    def salvar_edicao(self, id_jogo, titulo, plataforma, nota, descricao):
        # Atualiza jogo existente
        if not titulo or not plataforma:
            messagebox.showwarning("Aviso", "Preencha pelo menos título e plataforma")
            return
        
        imagem_base64 = None
        if self.imagem_selecionada:
            imagem_base64 = self.controller.lidar_converter_imagem(self.imagem_selecionada)
        
        sucesso, msg = self.controller.lidar_edit_jogo(
            id_jogo, titulo, plataforma, nota, descricao.strip(), imagem_base64
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.dashboard()
        else:
            messagebox.showerror("Erro", msg)
    
    def confirmar_exclusao(self, id_jogo):
        # Confirma exclusão de jogo
        if messagebox.askyesno("Confirmar", "Deseja excluir esta avaliação?"):
            sucesso, msg = self.controller.lidar_excluir_jogo(id_jogo)
            messagebox.showinfo("Resultado", msg)
            self.dashboard()
    
    def executar(self):
        # Inicia a aplicação
        self.root.mainloop()