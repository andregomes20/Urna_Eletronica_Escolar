import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os
import shutil
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- CONFIGURAÇÕES DE DESIGN (PALETA MODERNA) ---
COR_BARRA_LATERAL = "#2C3E50"    # Azul Escuro (Menu)
COR_FUNDO_PRINCIPAL = "#ECF0F1"  # Cinza Claro (Fundo)
COR_CARD = "#FFFFFF"             # Branco (Áreas de conteúdo)
COR_TEXTO = "#2C3E50"            # Cinza Escuro
COR_DESTAQUE = "#3498DB"         # Azul (Botões primários)
COR_VERDE = "#27AE60"            # Verde (Confirmar/Adicionar/Sim)
COR_VERMELHO = "#E74C3C"         # Vermelho (Remover/Cancelar/Não)
COR_LARANJA = "#F39C12"          # Laranja (Corrige/PDF)
COR_TEXTO_MENU = "#ECF0F1"       # Branco gelo

DATA_FILE = "dados_urna.json"
ASSETS_DIR = "assets_urna"

if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# --- CLASSE DE BOTÃO ARREDONDADO ---
class BotaoArredondado(tk.Canvas):
    def __init__(self, parent, width, height, radius, color, text_color, text, command=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.radius = radius
        self.color = color
        self.text_color = text_color
        self.text = text
        self.width = width
        self.height = height

        self.draw_button(self.color)
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self, color):
        self.delete("all")
        x1, y1, x2, y2 = 2, 2, self.width-2, self.height-2
        r = self.radius
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, 
                  x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, 
                  x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.create_polygon(points, fill=color, outline=color, smooth=True)
        self.create_text(self.width/2, self.height/2, text=self.text, fill=self.text_color, font=("Segoe UI", 10, "bold"))

    def on_click(self, event):
        self.draw_button("#555") 
        if self.command: self.command()

    def on_release(self, event):
        self.draw_button(self.color)

    def on_hover(self, event):
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.draw_button(self.color)

# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            d = json.load(f)
            if "modo_votacao" not in d['config']: d['config']['modo_votacao'] = "ambos"
            return d
    return {
        "config": {
            "titulo": "Eleições Escolares",
            "escola_logo": "",
            "senha_admin": "admin",
            "inicio_votacao": None,
            "fim_votacao": None,
            "modo_votacao": "ambos"
        },
        "chapas": {},
        "perguntas": [],
        "votos": []
    }

def salvar_dados(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

dados = carregar_dados()

# --- APLICAÇÃO PRINCIPAL ---
class UrnaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votação")
        self.root.state('zoomed')
        self.root.configure(bg=COR_FUNDO_PRINCIPAL)
        
        # TECLADO FÍSICO ATIVO
        self.root.bind('<Key>', self.leitura_teclado_fisico)

        self.container_principal = tk.Frame(root, bg=COR_FUNDO_PRINCIPAL)
        self.container_principal.pack(fill="both", expand=True)

        self.mostrar_tela_inicial()

    def leitura_teclado_fisico(self, event):
        if event.keysym == 'Escape':
            if messagebox.askyesno("Sair", "Voltar para o menu inicial?"):
                self.mostrar_tela_inicial()
            return
        if event.char in ['0','1','2','3','4','5','6','7','8','9']:
            self.teclar(event.char)

    def limpar_tela(self):
        for widget in self.container_principal.winfo_children():
            widget.destroy()

    # --- TELA INICIAL ---
    def mostrar_tela_inicial(self):
        self.limpar_tela()
        centro = tk.Frame(self.container_principal, bg=COR_FUNDO_PRINCIPAL)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(centro, bg=COR_CARD, padx=50, pady=50)
        card.pack()
        sombra = tk.Frame(centro, bg="#CCC", width=500, height=400)
        sombra.place(in_=card, relx=0.5, rely=0.5, anchor="center", x=5, y=5)
        card.lift()

        if dados['config']['escola_logo'] and os.path.exists(dados['config']['escola_logo']):
            try:
                im = Image.open(dados['config']['escola_logo']).resize((80,80))
                ph = ImageTk.PhotoImage(im)
                lbl = tk.Label(card, image=ph, bg=COR_CARD)
                lbl.image = ph
                lbl.pack(pady=(0, 20))
            except: pass

        tk.Label(card, text="URNA DIGITAL", font=("Segoe UI", 24, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack(pady=(0, 10))
        tk.Label(card, text=dados['config']['titulo'], font=("Segoe UI", 14), bg=COR_CARD, fg="#7F8C8D").pack(pady=(0, 40))

        BotaoArredondado(card, 250, 50, 20, COR_VERDE, "white", "INICIAR VOTAÇÃO", self.iniciar_urna).pack(pady=10)
        BotaoArredondado(card, 250, 50, 20, COR_DESTAQUE, "white", "PAINEL ADMINISTRATIVO", self.login_admin).pack(pady=10)

    # --- LOGIN ADMIN ---
    def login_admin(self):
        senha = simpledialog.askstring("Admin", "Senha de Administrador:", show='*')
        if senha == dados['config']['senha_admin']:
            self.mostrar_painel_admin()
        elif senha is not None:
            messagebox.showerror("Erro", "Senha incorreta")

    # --- PAINEL ADMINISTRATIVO ---
    def mostrar_painel_admin(self):
        self.limpar_tela()
        self.sidebar = tk.Frame(self.container_principal, bg=COR_BARRA_LATERAL, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="ADMIN", font=("Segoe UI", 20, "bold"), bg=COR_BARRA_LATERAL, fg="white").pack(pady=30)

        self.btn_menu(self.sidebar, "⚙ Configurações", self.abrir_config)
        self.btn_menu(self.sidebar, "👥 Candidatos (Chapas)", self.abrir_chapas)
        self.btn_menu(self.sidebar, "❓ Referendos", self.abrir_ref)
        self.btn_menu(self.sidebar, "📊 Resultados", self.abrir_resultados)
        
        # --- BOTÃO SOBRE ---
        self.btn_menu(self.sidebar, "ℹ Sobre", self.abrir_sobre)
        
        btn_sair = tk.Button(self.sidebar, text="← Voltar ao Início", bg=COR_VERMELHO, fg="white", font=("Segoe UI", 10, "bold"),
                             bd=0, command=self.mostrar_tela_inicial, pady=15)
        btn_sair.pack(side="bottom", fill="x")

        self.content_area = tk.Frame(self.container_principal, bg=COR_FUNDO_PRINCIPAL)
        self.content_area.pack(side="right", fill="both", expand=True, padx=40, pady=40)

        self.abrir_config()

    def btn_menu(self, parent, text, command):
        btn = tk.Button(parent, text=text, anchor="w", padx=20, bg=COR_BARRA_LATERAL, fg=COR_TEXTO_MENU,
                        font=("Segoe UI", 11), bd=0, activebackground="#34495E", activeforeground="white",
                        command=command, pady=12)
        btn.pack(fill="x")
        
    def titulo_secao(self, texto):
        for widget in self.content_area.winfo_children(): widget.destroy()
        tk.Label(self.content_area, text=texto, font=("Segoe UI", 22, "bold"), bg=COR_FUNDO_PRINCIPAL, fg=COR_TEXTO).pack(anchor="w", pady=(0, 20))
        self.card_conteudo = tk.Frame(self.content_area, bg=COR_CARD, padx=30, pady=30)
        self.card_conteudo.pack(fill="both", expand=True)
        self.card_conteudo.configure(highlightbackground="#D0D3D4", highlightthickness=1)

    # --- ABA SOBRE (ATUALIZADA COM ANO) ---
    def abrir_sobre(self):
        self.titulo_secao("Sobre o Sistema")
        f = self.card_conteudo
        
        container = tk.Frame(f, bg=COR_CARD)
        container.pack(expand=True)

        tk.Label(container, text="Urna Eletrônica Escolar", font=("Segoe UI", 20, "bold"), bg=COR_CARD, fg=COR_DESTAQUE).pack(pady=10)
        
        tk.Label(container, text="Desenvolvido por:", font=("Segoe UI", 12), bg=COR_CARD, fg="#7F8C8D").pack(pady=(30, 5))
        tk.Label(container, text="Prof. André Eduardo Gomes", font=("Segoe UI", 16, "bold"), bg=COR_CARD, fg=COR_TEXTO).pack()
        
        tk.Label(container, text="Contato / E-mail:", font=("Segoe UI", 12), bg=COR_CARD, fg="#7F8C8D").pack(pady=(20, 5))
        tk.Label(container, text="andre.gomes2004@gmail.com", font=("Segoe UI", 14), bg=COR_CARD, fg="#2980B9").pack()
        
        # --- ANO ADICIONADO ---
        tk.Label(container, text="Ano de Criação: 2025", font=("Segoe UI", 12), bg=COR_CARD, fg="#7F8C8D").pack(pady=(20, 0))

        tk.Label(container, text="Versão 3.2", font=("Segoe UI", 10), bg=COR_CARD, fg="#BDC3C7").pack(pady=(10, 0))

    # --- CONFIGURAÇÕES ---
    def abrir_config(self):
        self.titulo_secao("Configurações Gerais")
        f = self.card_conteudo
        tk.Label(f, text="Título da Eleição:", bg=COR_CARD, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.entry_titulo = tk.Entry(f, font=("Segoe UI", 12), bg="#F8F9F9", relief="flat", highlightbackground="#BDC3C7", highlightthickness=1)
        self.entry_titulo.insert(0, dados['config']['titulo'])
        self.entry_titulo.pack(fill="x", pady=(5, 20), ipady=5)
        
        tk.Label(f, text="Modo de Votação:", bg=COR_CARD, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.var_modo = tk.StringVar(value=dados['config']['modo_votacao'])
        frame_radio = tk.Frame(f, bg=COR_CARD)
        frame_radio.pack(anchor="w", pady=(5, 20))
        for text, val in [("Completo", "ambos"), ("Apenas Chapas", "chapa"), ("Apenas Perguntas", "referendo")]:
            tk.Radiobutton(frame_radio, text=text, variable=self.var_modo, value=val, bg=COR_CARD, font=("Segoe UI", 10)).pack(side="left", padx=(0, 15))

        tk.Label(f, text="Logo da Escola:", bg=COR_CARD, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        BotaoArredondado(f, 200, 40, 10, "#95A5A6", "white", "Escolher Arquivo...", self.upload_logo).pack(anchor="w", pady=(5, 30))
        BotaoArredondado(f, 200, 50, 20, COR_VERDE, "white", "SALVAR ALTERAÇÕES", self.salvar_config_geral).pack(pady=10)
        
        tk.Frame(f, height=2, bg="#ECF0F1").pack(fill="x", pady=30) 
        tk.Label(f, text="Zona de Perigo", bg=COR_CARD, fg=COR_VERMELHO, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        BotaoArredondado(f, 200, 40, 10, COR_VERMELHO, "white", "ZERAR VOTOS", self.zerar_votos).pack(anchor="w", pady=10)

    def upload_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if path:
            dest = os.path.join(ASSETS_DIR, f"logo_escola{os.path.splitext(path)[1]}")
            shutil.copy(path, dest)
            dados['config']['escola_logo'] = dest
            messagebox.showinfo("Sucesso", "Logo atualizado!")

    def salvar_config_geral(self):
        dados['config']['titulo'] = self.entry_titulo.get()
        dados['config']['modo_votacao'] = self.var_modo.get()
        salvar_dados(dados)
        messagebox.showinfo("Sucesso", "Configurações Salvas!")

    def zerar_votos(self):
        if messagebox.askyesno("CUIDADO", "Apagar todos os votos?"):
            dados['votos'] = []
            dados['config']['inicio_votacao'] = None
            dados['config']['fim_votacao'] = None
            salvar_dados(dados)
            messagebox.showinfo("Limpo", "Urna zerada.")

    # --- CHAPAS ---
    def abrir_chapas(self):
        self.titulo_secao("Gerenciar Candidatos (Chapas)")
        f = self.card_conteudo
        form_frame = tk.Frame(f, bg=COR_CARD)
        form_frame.pack(fill="x", pady=(0, 20))
        tk.Label(form_frame, text="Número:", bg=COR_CARD).grid(row=0, column=0, sticky="w")
        self.entry_num = tk.Entry(form_frame, width=8, font=("Segoe UI", 12), bg="#F8F9F9", relief="flat", highlightbackground="#BDC3C7", highlightthickness=1)
        self.entry_num.grid(row=1, column=0, padx=(0, 10), ipady=5)
        tk.Label(form_frame, text="Nome:", bg=COR_CARD).grid(row=0, column=1, sticky="w")
        self.entry_nome = tk.Entry(form_frame, width=30, font=("Segoe UI", 12), bg="#F8F9F9", relief="flat", highlightbackground="#BDC3C7", highlightthickness=1)
        self.entry_nome.grid(row=1, column=1, padx=(0, 10), ipady=5)
        self.temp_foto = ""
        BotaoArredondado(form_frame, 100, 32, 10, "#95A5A6", "white", "Foto", self.sel_foto_chapa).grid(row=1, column=2, padx=5)
        BotaoArredondado(form_frame, 120, 32, 10, COR_VERDE, "white", "Adicionar", self.add_chapa).grid(row=1, column=3, padx=5)
        list_frame = tk.Frame(f, bg="#BDC3C7", padx=1, pady=1)
        list_frame.pack(fill="both", expand=True)
        self.list_chapas = tk.Listbox(list_frame, font=("Segoe UI", 12), bg="white", borderwidth=0, highlightthickness=0, selectbackground=COR_DESTAQUE)
        self.list_chapas.pack(fill="both", expand=True)
        BotaoArredondado(f, 200, 40, 10, COR_VERMELHO, "white", "Remover Selecionado", self.del_chapa).pack(pady=15)
        self.atualiza_list_chapas()

    def sel_foto_chapa(self):
        self.temp_foto = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if self.temp_foto: messagebox.showinfo("Foto", "Foto selecionada.")

    def add_chapa(self):
        n, nome = self.entry_num.get(), self.entry_nome.get()
        if n and nome:
            dest = ""
            if self.temp_foto:
                dest = os.path.join(ASSETS_DIR, f"chapa_{n}{os.path.splitext(self.temp_foto)[1]}")
                shutil.copy(self.temp_foto, dest)
            dados['chapas'][n] = {"nome": nome, "foto": dest}
            salvar_dados(dados)
            self.atualiza_list_chapas()
            self.entry_num.delete(0, tk.END)
            self.entry_nome.delete(0, tk.END)
            self.temp_foto = ""

    def del_chapa(self):
        sel = self.list_chapas.curselection()
        if sel:
            n = self.list_chapas.get(sel[0]).split(" - ")[0]
            del dados['chapas'][n]
            salvar_dados(dados)
            self.atualiza_list_chapas()
    
    def atualiza_list_chapas(self):
        self.list_chapas.delete(0, tk.END)
        for n, d in dados['chapas'].items():
            self.list_chapas.insert(tk.END, f"{n} - {d['nome']}")

    # --- REFERENDOS ---
    def abrir_ref(self):
        self.titulo_secao("Perguntas (Referendo)")
        f = self.card_conteudo
        tk.Label(f, text="Digite a Pergunta (Sim/Não):", bg=COR_CARD, font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_ref = tk.Entry(f, font=("Segoe UI", 12), bg="#F8F9F9", relief="flat", highlightbackground="#BDC3C7", highlightthickness=1)
        self.entry_ref.pack(fill="x", pady=(5, 10), ipady=5)
        BotaoArredondado(f, 180, 40, 10, COR_VERDE, "white", "Adicionar Pergunta", self.add_ref).pack(anchor="w", pady=(0, 20))
        list_frame = tk.Frame(f, bg="#BDC3C7", padx=1, pady=1)
        list_frame.pack(fill="both", expand=True)
        self.list_ref = tk.Listbox(list_frame, font=("Segoe UI", 12), bg="white", borderwidth=0, highlightthickness=0, selectbackground=COR_DESTAQUE)
        self.list_ref.pack(fill="both", expand=True)
        BotaoArredondado(f, 200, 40, 10, COR_VERMELHO, "white", "Remover Pergunta", self.del_ref).pack(pady=15)
        self.atualiza_list_ref()

    def add_ref(self):
        if self.entry_ref.get():
            dados['perguntas'].append(self.entry_ref.get())
            salvar_dados(dados)
            self.entry_ref.delete(0, tk.END)
            self.atualiza_list_ref()

    def del_ref(self):
        sel = self.list_ref.curselection()
        if sel:
            del dados['perguntas'][sel[0]]
            salvar_dados(dados)
            self.atualiza_list_ref()

    def atualiza_list_ref(self):
        self.list_ref.delete(0, tk.END)
        for i, p in enumerate(dados['perguntas']):
            self.list_ref.insert(tk.END, f"{i+1}: {p}")

    # --- RESULTADOS ---
    def abrir_resultados(self):
        self.titulo_secao("Relatórios e Resultados")
        f = self.card_conteudo
        
        # Header com Botão
        topo_frame = tk.Frame(f, bg=COR_CARD)
        topo_frame.pack(fill="x", pady=(0, 20))
        
        # Info Esquerda
        info_total = tk.Frame(topo_frame, bg=COR_CARD)
        info_total.pack(side="left")
        tk.Label(info_total, text="Total de Votos:", font=("Segoe UI", 12), bg=COR_CARD, fg="#7F8C8D").pack(anchor="w")
        tk.Label(info_total, text=str(len(dados['votos'])), font=("Segoe UI", 24, "bold"), bg=COR_CARD, fg=COR_DESTAQUE).pack(anchor="w")

        # Botão Direita
        BotaoArredondado(topo_frame, 260, 50, 20, COR_LARANJA, "white", "🖨 GERAR PDF / IMPRIMIR", self.gerar_pdf).pack(side="right", padx=10)

        # Divisor
        tk.Frame(f, height=1, bg="#E0E0E0").pack(fill="x", pady=(0, 20))

        # Detalhes
        detalhes_frame = tk.Frame(f, bg=COR_FUNDO_PRINCIPAL, padx=10, pady=10)
        detalhes_frame.pack(fill="both", expand=True)

        modo = dados['config']['modo_votacao']

        # Lista Chapas
        if modo in ['ambos', 'chapa']:
            tk.Label(detalhes_frame, text="🏆 Grêmio (Chapas)", font=("Segoe UI", 14, "bold"), bg=COR_FUNDO_PRINCIPAL, fg=COR_TEXTO).pack(anchor="w", pady=(5, 10))
            res_chapa = {k: 0 for k in dados['chapas']}
            res_chapa['BRANCO'] = 0; res_chapa['NULO'] = 0
            for v in dados['votos']:
                if 'chapa' in v:
                    val = v['chapa']
                    if val in res_chapa: res_chapa[val] += 1
                    else: res_chapa['NULO'] += 1
            
            ordenado = sorted(res_chapa.items(), key=lambda x: x[1], reverse=True)
            for chave, votos in ordenado:
                nome_display = "VOTOS EM BRANCO" if chave=='BRANCO' else "VOTOS NULOS" if chave=='NULO' else f"{chave} - {dados['chapas'].get(chave,{}).get('nome','?')}"
                
                row = tk.Frame(detalhes_frame, bg=COR_CARD, pady=8, padx=10)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=nome_display, font=("Segoe UI", 11, "bold"), bg=COR_CARD, width=40, anchor="w").pack(side="left")
                
                # Barra visual
                percent = 0
                total = len(dados['votos'])
                if total > 0: percent = votos/total
                largura = int(200*percent)
                if largura > 0:
                    tk.Frame(row, bg=COR_DESTAQUE if chave not in ['BRANCO','NULO'] else "#BDC3C7", width=largura, height=10).pack(side="left", padx=10)

                tk.Label(row, text=f"{votos} votos", font=("Segoe UI", 11), bg=COR_CARD).pack(side="right")

        # Lista Referendos
        if modo in ['ambos', 'referendo']:
            tk.Label(detalhes_frame, text="❓ Referendos", font=("Segoe UI", 14, "bold"), bg=COR_FUNDO_PRINCIPAL, fg=COR_TEXTO).pack(anchor="w", pady=(30, 10))
            for i, p in enumerate(dados['perguntas']):
                sim, nao, bra, nul = 0, 0, 0, 0
                for v in dados['votos']:
                    if 'referendo' in v and i < len(v['referendo']):
                        r = v['referendo'][i]
                        if r == '1': sim += 1
                        elif r == '2': nao += 1
                        elif r == 'BRANCO': bra += 1
                        else: nul += 1
                
                card_ref = tk.Frame(detalhes_frame, bg=COR_CARD, bd=0, padx=15, pady=15)
                card_ref.pack(fill="x", pady=5)
                tk.Label(card_ref, text=f"{i+1}. {p}", font=("Segoe UI", 11, "bold"), bg=COR_CARD).pack(anchor="w")
                
                res_txt = tk.Frame(card_ref, bg=COR_CARD)
                res_txt.pack(fill="x", pady=(10, 0))
                tk.Label(res_txt, text=f"SIM: {sim}", font=("Segoe UI", 10,"bold"), bg="#D5F5E3", fg="#27AE60", padx=10, pady=2).pack(side="left", padx=(0, 10))
                tk.Label(res_txt, text=f"NÃO: {nao}", font=("Segoe UI", 10,"bold"), bg="#FADBD8", fg="#C0392B", padx=10, pady=2).pack(side="left", padx=(0, 10))
                tk.Label(res_txt, text=f"(Brancos: {bra} | Nulos: {nul})", font=("Segoe UI", 9), bg=COR_CARD, fg="#95A5A6").pack(side="left", padx=10)

    # --- GERAR PDF ---
    def gerar_pdf(self):
        dados['config']['fim_votacao'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        salvar_dados(dados)
        
        inicio = dados['config'].get('inicio_votacao', 'Não registrado')
        fim = dados['config']['fim_votacao']

        fname = f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        c = canvas.Canvas(fname, pagesize=A4)
        w, h = A4
        
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, h-50, dados['config']['titulo'])
        
        c.setFont("Helvetica", 10)
        c.drawString(50, h-70, f"Arquivo gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, h-90, f"Início da Sessão de Votação: {inicio}")
        c.drawString(50, h-105, f"Fim da Sessão de Votação: {fim}")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, h-125, f"Votos Totais Computados: {len(dados['votos'])}")
        
        y = h - 160
        
        if dados['config']['modo_votacao'] in ['ambos', 'chapa']:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColorRGB(0, 0, 0.5)
            c.drawString(50, y, "CHAPAS")
            y -= 25
            res = {k:0 for k in dados['chapas']}; res['BRANCO']=0; res['NULO']=0
            for v in dados['votos']:
                if 'chapa' in v:
                    val = v['chapa']
                    if val in res: res[val]+=1
                    else: res['NULO']+=1
            c.setFont("Helvetica", 12); c.setFillColorRGB(0,0,0)
            for ch, count in sorted(res.items(), key=lambda x:x[1], reverse=True):
                nm = dados['chapas'].get(ch, {}).get('nome', ch)
                c.drawString(70, y, f"{ch} - {nm}: {count} votos")
                y -= 20
            y -= 30

        if dados['config']['modo_votacao'] in ['ambos', 'referendo']:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColorRGB(0, 0, 0.5)
            c.drawString(50, y, "REFERENDOS")
            y -= 25
            for i, p in enumerate(dados['perguntas']):
                s, n, b, nu = 0,0,0,0
                for v in dados['votos']:
                    if 'referendo' in v and i < len(v['referendo']):
                        r = v['referendo'][i]
                        if r=='1': s+=1
                        elif r=='2': n+=1
                        elif r=='BRANCO': b+=1
                        else: nu+=1
                c.setFont("Helvetica-Bold", 11)
                c.drawString(50, y, f"P: {p}")
                y -= 15
                c.setFont("Helvetica", 10)
                c.drawString(70, y, f"SIM: {s} | NÃO: {n} | BRANCO: {b} | NULO: {nu}")
                y -= 30
        
        c.save()
        messagebox.showinfo("Sucesso", f"PDF criado: {fname}")
        os.startfile(fname)

    # --- URNA (VOTAÇÃO) ---
    def iniciar_urna(self):
        modo = dados['config']['modo_votacao']
        if modo == 'ambos' and not dados['chapas']:
            messagebox.showerror("Erro", "Cadastre chapas primeiro.")
            return

        if not dados['config']['inicio_votacao']:
            dados['config']['inicio_votacao'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            salvar_dados(dados)

        self.etapas_votacao = []
        if modo in ['ambos', 'chapa']: self.etapas_votacao.append({'tipo': 'chapa'})
        if modo in ['ambos', 'referendo']:
            for p in dados['perguntas']: self.etapas_votacao.append({'tipo': 'ref', 'pergunta': p})

        self.passo_atual = 0
        self.votos_temporarios = {}
        self.voto_atual = ""
        self.buffer_secreto = ""
        self.construir_tela_urna()
        self.preparar_etapa()

    def construir_tela_urna(self):
        self.limpar_tela()
        self.frame_urna = tk.Frame(self.container_principal, bg=COR_FUNDO_PRINCIPAL)
        self.frame_urna.pack(fill="both", expand=True)
        centro = tk.Frame(self.frame_urna, bg=COR_FUNDO_PRINCIPAL)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        self.tela_visual = tk.Frame(centro, bg="#E8E8E8", width=600, height=500, highlightthickness=1, highlightbackground="#999")
        self.tela_visual.pack_propagate(False)
        self.tela_visual.grid(row=0, column=0, padx=30)
        self.painel_botoes = tk.Frame(centro, bg="#333", padx=20, pady=20, relief="raised", bd=2)
        self.painel_botoes.grid(row=0, column=1, padx=30)

    def preparar_etapa(self):
        self.voto_atual = ""
        self.atualizar_visual()
        self.atualizar_teclado()

    def atualizar_teclado(self):
        for w in self.painel_botoes.winfo_children(): w.destroy()
        etapa = self.etapas_votacao[self.passo_atual]
        if etapa['tipo'] == 'chapa':
            nums = tk.Frame(self.painel_botoes, bg="#333")
            nums.pack(pady=(0,20))
            for i, n in enumerate(['1','2','3','4','5','6','7','8','9']):
                tk.Button(nums, text=n, font=("Arial", 18, "bold"), width=5, height=2, bg="#111", fg="white",
                          activebackground="#444", activeforeground="white", command=lambda x=n: self.teclar(x)).grid(row=i//3, column=i%3, padx=5, pady=5)
            tk.Button(nums, text="0", font=("Arial", 18, "bold"), width=5, height=2, bg="#111", fg="white",
                      activebackground="#444", activeforeground="white", command=lambda: self.teclar("0")).grid(row=3, column=1, padx=5, pady=5)
        elif etapa['tipo'] == 'ref':
            tk.Button(self.painel_botoes, text="SIM (1)", font=("Arial", 16, "bold"), width=12, height=3, bg=COR_DESTAQUE, fg="white", 
                      activebackground="#2980B9", activeforeground="white", command=lambda: self.teclar("1")).pack(pady=10)
            tk.Button(self.painel_botoes, text="NÃO (2)", font=("Arial", 16, "bold"), width=12, height=3, bg=COR_VERMELHO, fg="white", 
                      activebackground="#C0392B", activeforeground="white", command=lambda: self.teclar("2")).pack(pady=10)
        acoes = tk.Frame(self.painel_botoes, bg="#333")
        acoes.pack()
        tk.Button(acoes, text="BRANCO", bg="white", fg="black", width=9, height=3, font=("Arial",10,"bold"), command=self.voto_branco).pack(side="left", padx=5)
        tk.Button(acoes, text="CORRIGE", bg=COR_LARANJA, fg="black", width=9, height=3, font=("Arial",10,"bold"), command=self.corrige).pack(side="left", padx=5)
        tk.Button(acoes, text="CONFIRMA", bg=COR_VERDE, fg="black", width=9, height=4, font=("Arial",10,"bold"), command=self.confirma).pack(side="left", padx=5)

    def atualizar_visual(self):
        for w in self.tela_visual.winfo_children(): w.destroy()
        etapa = self.etapas_votacao[self.passo_atual]
        topo = tk.Frame(self.tela_visual, bg="#E8E8E8", height=50)
        topo.pack(fill="x", padx=10, pady=10)
        if dados['config']['escola_logo'] and os.path.exists(dados['config']['escola_logo']):
            try:
                im = Image.open(dados['config']['escola_logo']).resize((50,50))
                ph = ImageTk.PhotoImage(im)
                l = tk.Label(topo, image=ph, bg="#E8E8E8"); l.image=ph
                l.pack(side="right")
            except: pass
        tk.Label(topo, text=dados['config']['titulo'], bg="#E8E8E8").pack(side="left")
        cont = tk.Frame(self.tela_visual, bg="#E8E8E8")
        cont.pack(fill="both", expand=True, padx=20)
        
        if etapa['tipo'] == 'chapa':
            tk.Label(cont, text="VOTO PARA GRÊMIO", font=("Arial", 16, "bold"), bg="#E8E8E8").pack(anchor="w")
            cx = tk.Frame(cont, bg="#E8E8E8")
            cx.pack(anchor="w", pady=20)
            txt = self.voto_atual if self.voto_atual != "BRANCO" else ""
            for i in range(2):
                d = txt[i] if i < len(txt) else ""
                tk.Label(cx, text=d, font=("Arial", 30), bg="white", relief="solid", bd=1, width=2).pack(side="left", padx=2)
            if self.voto_atual == "BRANCO":
                 tk.Label(cont, text="VOTO EM BRANCO", font=("Arial", 26, "bold"), bg="#E8E8E8").pack(pady=40)
            elif len(self.voto_atual)==2:
                if self.voto_atual in dados['chapas']:
                    ch = dados['chapas'][self.voto_atual]
                    tk.Label(cont, text=ch['nome'], font=("Arial", 20, "bold"), bg="#E8E8E8").pack(anchor="w")
                    if os.path.exists(ch['foto']):
                        im = Image.open(ch['foto']).resize((150,200))
                        ph = ImageTk.PhotoImage(im)
                        l = tk.Label(cont, image=ph, bg="#E8E8E8"); l.image=ph
                        l.place(relx=1.0, rely=0.2, anchor="ne")
                else:
                    tk.Label(cont, text="VOTO NULO", font=("Arial", 26, "bold"), bg="#E8E8E8").pack(pady=40)
        elif etapa['tipo'] == 'ref':
            tk.Label(cont, text="REFERENDO", font=("Arial", 12), bg="#E8E8E8").pack(anchor="w")
            tk.Label(cont, text=etapa['pergunta'], font=("Arial", 16, "bold"), bg="#E8E8E8", wraplength=400, justify="left").pack(anchor="w", pady=20)
            if self.voto_atual == "1": tk.Label(cont, text="1 - SIM", font=("Arial", 30, "bold"), bg="#E8E8E8", fg=COR_DESTAQUE).pack()
            elif self.voto_atual == "2": tk.Label(cont, text="2 - NÃO", font=("Arial", 30, "bold"), bg="#E8E8E8", fg=COR_VERMELHO).pack()
            elif self.voto_atual == "BRANCO": tk.Label(cont, text="BRANCO", font=("Arial", 30, "bold"), bg="#E8E8E8").pack()

    def teclar(self, num):
        self.buffer_secreto += num
        if self.buffer_secreto[-5:] == "99999":
            if messagebox.askyesno("Admin", "Sair para o menu inicial?"):
                self.mostrar_tela_inicial()
            return
        if self.passo_atual < len(self.etapas_votacao):
            etapa = self.etapas_votacao[self.passo_atual]
            limite = 2 if etapa['tipo'] == 'chapa' else 1
            if etapa['tipo'] == 'ref':
                if num in ['1', '2']: 
                    self.voto_atual = num
                    self.atualizar_visual()
            else:
                if len(self.voto_atual) < limite: 
                    self.voto_atual += num
                    self.atualizar_visual()

    def voto_branco(self):
        self.voto_atual = "BRANCO"
        self.atualizar_visual()

    def corrige(self):
        self.voto_atual = ""
        self.atualizar_visual()

    def confirma(self):
        if self.voto_atual == "": return
        etapa = self.etapas_votacao[self.passo_atual]
        if etapa['tipo'] == 'chapa':
            if self.voto_atual == "BRANCO": self.votos_temporarios['chapa'] = "BRANCO"
            elif len(self.voto_atual) == 2:
                self.votos_temporarios['chapa'] = self.voto_atual if self.voto_atual in dados['chapas'] else "NULO"
            else: return
        elif etapa['tipo'] == 'ref':
            if 'referendo' not in self.votos_temporarios: self.votos_temporarios['referendo'] = []
            if self.voto_atual in ['1','2','BRANCO']: self.votos_temporarios['referendo'].append(self.voto_atual)
            else: self.votos_temporarios['referendo'].append("NULO")
        self.passo_atual += 1
        if self.passo_atual < len(self.etapas_votacao): self.preparar_etapa()
        else: self.finalizar()

    def finalizar(self):
        dados['votos'].append(self.votos_temporarios)
        salvar_dados(dados)
        self.limpar_tela()
        tk.Label(self.container_principal, text="FIM", font=("Arial", 60, "bold"), bg=COR_FUNDO_PRINCIPAL).place(relx=0.5, rely=0.5, anchor="center")
        self.root.update()
        self.root.after(3000, self.iniciar_urna)

if __name__ == "__main__":
    root = tk.Tk()
    app = UrnaApp(root)
    root.mainloop()
