from tkinter import messagebox
import customtkinter
import string
import random
import sqlite3

# Definir Cores a Usar ----------------------------
Co0 = "#808080"
Co1 = "#FFFFFF"

# Conectando ao banco de dados SQLite (ou criando-o se não existir)
conexao = sqlite3.connect('senhas.db')
cursor = conexao.cursor()

# Criar a tabela se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS senhas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    servico TEXT NOT NULL,
                    senha TEXT NOT NULL
                )''')
conexao.commit()

# Função para gerar senha --------------------------
def gerar_senha():
    caracteres = ""
    
    # Verificar quais opções estão selecionadas
    if chkGrandes.get() == 1:
        caracteres += string.ascii_uppercase
    if chkPequenas.get() == 1:
        caracteres += string.ascii_lowercase
    if chkNumeros.get() == 1:
        caracteres += string.digits
    if chkSimbolos.get() == 1:
        caracteres += string.punctuation
    
    comprimento = int(SChars.get())

    # Verificar se o comprimento é maior que zero e se há caracteres disponíveis
    if comprimento < 1 or not caracteres:
        ESenha.delete(0, 'end')
        LStatus.configure(text="Selecione opções válidas e defina o comprimento")
        return

    # Gerar a senha
    senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
    ESenha.delete(0, 'end')
    ESenha.insert(0, senha)
    LStatus.configure(text="Senha gerada com sucesso")

    # Atualizar o label Lchars com o número de caracteres
    Lchars.configure(text=f'Caracteres {comprimento}')

# Função para copiar a senha ----------------------
def copiar_senha():
    Janela.clipboard_clear()
    Janela.clipboard_append(ESenha.get())
    LStatus.configure(text="Senha copiada para a área de transferência")

# Função para limpar a senha ----------------------
def limpar_senha():
    ESenha.delete(0, 'end')
    EServico.delete(0, 'end')
    chkGrandes.deselect()
    chkPequenas.deselect()
    chkNumeros.deselect()
    chkSimbolos.deselect()
    SChars.set(0)
    Lchars.configure(text="Caracteres 0:")
    LStatus.configure(text="Estado ...")

# Função para salvar a senha na base de dados -----
def salvar_senha():
    servico = EServico.get().strip()
    senha = ESenha.get().strip()
    
    if not senha:
        LStatus.configure(text="Gere uma senha antes de salvar")
        return
    
    # Atribuir um nome padrão ao serviço se não estiver preenchido
    if not servico:
        servico = f"Serviço-{random.randint(1000, 9999)}"
    
    cursor.execute("INSERT INTO senhas (servico, senha) VALUES (?, ?)", (servico, senha))
    conexao.commit()
    
    LStatus.configure(text="Senha salva na base de dados com sucesso")
    
    # Não limpar os campos após salvar
    # limpar_senha()  # Removido para não limpar a senha

# Função para carregar a senha do banco de dados -----
def carregar_senha():
    servico = EServico.get().strip()
    
    if not servico:
        LStatus.configure(text="Insira o nome do serviço para carregar a senha")
        return
    
    cursor.execute("SELECT senha FROM senhas WHERE servico = ?", (servico,))
    resultado = cursor.fetchone()
    
    if resultado:
        ESenha.delete(0, 'end')
        ESenha.insert(0, resultado[0])
        LStatus.configure(text="Senha carregada com sucesso")
    else:
        LStatus.configure(text="Serviço não encontrado na base de dados")

# Função para sair -------------------------------
def sair():
    resposta = messagebox.askyesno("Confirmação", "Deseja sair da aplicação?")
    if resposta:
        conexao.close()  # Fechar a conexão com o banco de dados ao sair
        Janela.destroy()

# Janela ----------------------------
Janela = customtkinter.CTk()
Janela.geometry('800x270+100+100')
Janela.resizable(0, 0)
Janela.title('Gerador de senhas © Dev Joel Portugal 2024')
Janela.config(bg=Co0)

# Entrada para o serviço
EServico = customtkinter.CTkEntry(Janela, width=780, bg_color=Co0, fg_color=Co0, placeholder_text="Nome do Serviço", text_color=Co1)
EServico.place(x=10, y=10)

# Entrada para a senha gerada
ESenha = customtkinter.CTkEntry(Janela, width=780, bg_color=Co0, fg_color=Co0, text_color=Co1)
ESenha.place(x=10, y=45)

# Checkboxes
chkGrandes = customtkinter.CTkCheckBox(Janela, text='Letras Grandes', bg_color=Co0, fg_color=Co0, text_color=Co1, border_color="")
chkGrandes.place(x=10, y=80)

chkPequenas = customtkinter.CTkCheckBox(Janela, text='Letras Pequenas', bg_color=Co0, fg_color=Co0, text_color=Co1, border_color="")
chkPequenas.place(x=155, y=80)

chkNumeros = customtkinter.CTkCheckBox(Janela, text='Números', bg_color=Co0, fg_color=Co0, text_color=Co1, border_color="")
chkNumeros.place(x=320, y=80)

chkSimbolos = customtkinter.CTkCheckBox(Janela, text='Símbolos', bg_color=Co0, fg_color=Co0, text_color=Co1, border_color="")
chkSimbolos.place(x=455, y=80)

# Label e Slider de caracteres
Lchars = customtkinter.CTkLabel(Janela, text='Caracteres 0', bg_color=Co0, fg_color=Co0, text_color=Co1)
Lchars.place(x=10, y=115)

SChars = customtkinter.CTkSlider(Janela, width=760, bg_color=Co0, fg_color=Co0, from_=1, to=255)  # Adicionado limite mínimo e máximo
SChars.place(x=10, y=150)
SChars.set(0)  # Definindo um valor padrão diferente de 0

# Botões de Gerar, Copiar, Salvar, Limpar e Sair
BGerar = customtkinter.CTkButton(Janela, text='Gerar', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=gerar_senha)
BGerar.place(x=10, y=185)

Bcopiar = customtkinter.CTkButton(Janela, text='Copiar', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=copiar_senha)
Bcopiar.place(x=85, y=185)

BSalvar = customtkinter.CTkButton(Janela, text='Salvar', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=salvar_senha)
BSalvar.place(x=160, y=185)

BLimpar = customtkinter.CTkButton(Janela, text='Limpar', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=limpar_senha)
BLimpar.place(x=235, y=185)

BSair = customtkinter.CTkButton(Janela, text='Sair', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=sair)
BSair.place(x=310, y=185)

# Botão para carregar a senha do banco de dados
BCarregar = customtkinter.CTkButton(Janela, text='Carregar', width=65, bg_color=Co0, fg_color=Co0, text_color=Co1, command=carregar_senha)
BCarregar.place(x=385, y=185)

# Status
LStatus = customtkinter.CTkLabel(Janela, text='Estado ...', bg_color=Co0, fg_color=Co0, text_color=Co1)
LStatus.place(x=10, y=220)

Janela.mainloop()
