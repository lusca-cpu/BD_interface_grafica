from tkinter import *
from tkinter import ttk
from sqlite import bancoDeDados  # Import the correct class from your module

def limpar_tela():
    # Remove todos os widgets do frame
    for widget in frm.winfo_children():
        widget.destroy()


def salvar(nome_entry, email_entry, senha_entry):  
    nome = str(nome_entry.get())
    email = str(email_entry.get())
    senha = str(senha_entry.get())

    conn = bancoDeDados()
    conn.criar_tabelas()
    if nome and email and senha:
        conn.cursor.execute("INSERT INTO user (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        
        conn.conection.commit()
        ttk.Label(frm, text="Conta criada com sucesso!", font="Arial 14", foreground="green").grid(column=1, row=6)
        conn.conection.close()

def excluir_conta(usuario):
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute("DELETE FROM user WHERE id = ?", (usuario[0],))
    conn.conection.commit()
    conn.conection.close()

def criar_conta():
    limpar_tela()

    ttk.Label(frm, text="Criar Conta", font="Arial 16").grid(column=1, row=0)

    ttk.Label(frm, text="nome: ", font="Arial 16").grid(column=0, row=1)
    nome_entry = ttk.Entry(frm, font="Arial 16")
    nome_entry.grid(column=1, row=1)

    ttk.Label(frm, text="email: ", font="Arial 16").grid(column=0, row=2)
    email_entry = ttk.Entry(frm, font="Arial 16")
    email_entry.grid(column=1, row=2)

    ttk.Label(frm, text="senha: ", font="Arial 16").grid(column=0, row=3)
    senha_entry = ttk.Entry(frm, font="Arial 16", show="*")
    senha_entry.grid(column=1, row=3)

    ttk.Button(frm, text="Salvar", command=lambda: salvar(nome_entry, email_entry, senha_entry)).grid(column=1, row=4)
    ttk.Button(frm, text="Voltar", command=login).grid(column=2, row=4)


def verificar_login(email_entry, senha_entry):
    email_digitado = email_entry.get()
    senha_digitada = senha_entry.get()

    # Conectar ao banco de dados
    conn = bancoDeDados()
    conn.criar_tabelas()

    # Consultar o banco de dados para verificar se as credenciais existem
    query = "SELECT * FROM user WHERE email = ? AND senha = ?"
    conn.cursor.execute(query, (email_digitado, senha_digitada))
    resultado = conn.cursor.fetchone()

    conn.conection.close()

    if resultado:
        # Login bem-sucedido: redirecionar para a função `anime`
        limpar_tela()
        anime(resultado)  # Passar os dados do usuário, se necessário
    else:
        # Login falhou: Exibir mensagem de erro
        ttk.Label(frm, text="E-mail ou senha incorretos!", font="Arial 12", foreground="red").grid(column=1, row=4)


def trocar_senha():
    limpar_tela()

    # Mensagem inicial
    ttk.Label(frm, text="Recuperação de Senha", font="Arial 16 bold").grid(column=1, row=0, columnspan=2)

    # Campo para o email
    ttk.Label(frm, text="Email: ", font="Arial 16").grid(column=0, row=2)
    email = ttk.Entry(frm, font="Arial 16")
    email.grid(column=1, row=2)

    # Campo para nova senha
    ttk.Label(frm, text="Nova Senha: ", font="Arial 16").grid(column=0, row=3)
    nova_senha = ttk.Entry(frm, font="Arial 16", show="*")
    nova_senha.grid(column=1, row=3)

    # Botão para confirmar a troca
    ttk.Button(
        frm,
        text="Alterar Senha",
        command=lambda: verificar_email_e_trocar_senha(email, nova_senha)
    ).grid(column=1, row=4)

    # Botão para voltar à tela de login
    ttk.Button(frm, text="Voltar", command=login).grid(column=1, row=5)

def verificar_email_e_trocar_senha(email_entry, nova_senha_entry):
    email = email_entry.get()
    nova_senha = nova_senha_entry.get()

    # Conectar ao banco de dados e verificar se o email existe
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
    usuario = conn.cursor.fetchone()

    if usuario:
        # Atualizar a senha no banco de dados
        conn.cursor.execute("UPDATE user SET senha = ? WHERE email = ?", (nova_senha, email))
        conn.conection.commit()
        conn.conection.close()

        # Mostrar mensagem de sucesso
        ttk.Label(frm, text="Senha alterada com sucesso!", font="Arial 14", foreground="green").grid(column=1, row=6)
    else:
        # Mostrar mensagem de erro
        ttk.Label(frm, text="Email não encontrado!", font="Arial 14", foreground="red").grid(column=1, row=6)


def salvar_anime(nome_anime, temporada, episodio, id_user):
    anime = str(nome_anime.get())
    temporada = str(temporada.get())
    episodio = str(episodio.get())

    conn = bancoDeDados()
    conn.criar_tabelas()
    if anime and temporada and episodio:
        conn.cursor.execute("INSERT INTO anime (id_user, nome_anime, temporada, episodio) VALUES (?, ?, ?, ?)", (id_user,anime, temporada, episodio))
        
        conn.conection.commit()
        conn.conection.close()

    
def anime(usuario):
    limpar_tela()

    # Exibe o nome do usuário logado na tela
    ttk.Label(frm, text=f"Bem-vindo, {usuario[1]}!", font="Arial 16").grid(column=1, row=0)  # Nome do usuário

    ttk.Label(frm, text="Adicione um novo anime, temporada e o episodio.", font="Arial 16").grid(column=1, row=1)

    ttk.Label(frm, text="Anime: ", font="Arial 16").grid(column=0, row=2)
    nome_anime = ttk.Entry(frm, font="Arial 16")
    nome_anime.grid(column=1, row=2)

    ttk.Label(frm, text="Temporada: ", font="Arial 16").grid(column=0, row=3)
    temporada = ttk.Entry(frm, font="Arial 16")
    temporada.grid(column=1, row=3)

    ttk.Label(frm, text="Episodio: ", font="Arial 16").grid(column=0, row=4)
    episodio = ttk.Entry(frm, font="Arial 16")
    episodio.grid(column=1, row=4)

    ttk.Button(frm, text="Adicionar", command=lambda: [salvar_anime(nome_anime, temporada, episodio, usuario[0]), exibir_animes(usuario)]).grid(column=1, row=5)
    ttk.Button(frm, text="Vizualizar animes", command=lambda: [exibir_animes(usuario)]).grid(column=1, row=6)
    ttk.Button(frm, text="Excluir conta", command=lambda: [excluir_conta(usuario), login()]).grid(column=3, row=6)
    ttk.Button(frm, text="Voltar", command=login).grid(column=1, row=7)


# Exibe os animes associados ao usuário logado com opções de editar e excluir
def exibir_animes(usuario):
    # Consulta os animes do usuário no banco de dados
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute("SELECT id, nome_anime, temporada, episodio FROM anime WHERE id_user = ?", (usuario[0],))
    animes = conn.cursor.fetchall()
    conn.conection.close()

    # Remove widgets antigos (se necessário)
    for widget in frm.winfo_children():
        widget.destroy()

    ttk.Label(frm, text="Lista de Animes", font="Arial 16 bold").grid(column=1, row=0, columnspan=2)

    # Adiciona cada anime à tabela
    for idx, registro_anime in enumerate(animes, start=1):  # Renomeado para registro_anime
        anime_id, nome_anime, temporada, episodio = registro_anime

        # Exibe informações do anime
        ttk.Label(frm, text=f"Anime: {nome_anime}", font="Arial 14").grid(column=0, row=idx, sticky="w", padx=10, pady=5)
        ttk.Label(frm, text=f"Temporada: {temporada}", font="Arial 14").grid(column=1, row=idx, sticky="w", padx=10, pady=5)
        ttk.Label(frm, text=f"Episódio: {episodio}", font="Arial 14").grid(column=2, row=idx, sticky="w", padx=10, pady=5)

        # Botões de ações
        ttk.Button(frm, text="Editar", command=lambda a=anime_id: editar_anime(a, usuario)).grid(column=3, row=idx, padx=5)
        ttk.Button(frm, text="Excluir", command=lambda a=anime_id: excluir_anime(a, usuario)).grid(column=4, row=idx, padx=5)

    # Botão para adicionar novo anime
    ttk.Button(frm, text="Adicionar Anime", command=lambda: anime(usuario)).grid(column=1, row=len(animes) + 1, columnspan=2, pady=10)


def excluir_anime(anime_id, usuario):
    """Exclui um anime baseado no ID e atualiza a tabela."""
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
    conn.conection.commit()
    conn.conection.close()

    # Atualiza a tabela após exclusão
    exibir_animes(usuario)


def editar_anime(anime_id, usuario):
    """Abre um formulário para editar o anime selecionado."""
    # Consulta os dados do anime pelo ID
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute("SELECT nome_anime, temporada, episodio FROM anime WHERE id = ?", (anime_id,))
    anime = conn.cursor.fetchone()
    conn.conection.close()

    limpar_tela()

    # Campos de edição
    ttk.Label(frm, text="Editar Anime", font="Arial 16").grid(column=1, row=0)

    ttk.Label(frm, text="Anime: ", font="Arial 16").grid(column=0, row=1)
    nome_anime = ttk.Entry(frm, font="Arial 16")
    nome_anime.insert(0, anime[0])  # Preenche com o valor atual
    nome_anime.grid(column=1, row=1)

    ttk.Label(frm, text="Temporada: ", font="Arial 16").grid(column=0, row=2)
    temporada = ttk.Entry(frm, font="Arial 16")
    temporada.insert(0, anime[1])  # Preenche com o valor atual
    temporada.grid(column=1, row=2)

    ttk.Label(frm, text="Episódio: ", font="Arial 16").grid(column=0, row=3)
    episodio = ttk.Entry(frm, font="Arial 16")
    episodio.insert(0, anime[2])  # Preenche com o valor atual
    episodio.grid(column=1, row=3)

    # Botões de salvar e voltar
    ttk.Button(frm, text="Salvar", command=lambda: salvar_edicao(anime_id, nome_anime, temporada, episodio, usuario)).grid(column=1, row=4)
    ttk.Button(frm, text="Voltar", command=lambda: anime(usuario)).grid(column=1, row=5)


def salvar_edicao(anime_id, nome_anime, temporada, episodio, usuario):
    """Salva as alterações feitas no anime."""
    conn = bancoDeDados()
    conn.criar_tabelas()
    conn.cursor.execute(
        "UPDATE anime SET nome_anime = ?, temporada = ?, episodio = ? WHERE id = ?",
        (nome_anime.get(), temporada.get(), episodio.get(), anime_id)
    )
    conn.conection.commit()
    conn.conection.close()

    # Volta para a lista após salvar
    anime(usuario)


def login():
    limpar_tela()

    ttk.Label(frm, text="Seja Bem Vindo!", font="Arial 16").grid(column=1, row=0)

    ttk.Label(frm, text="email: ", font="Arial 16").grid(column=0, row=2)
    email = ttk.Entry(frm, font="Arial 16")
    email.grid(column=1, row=2)

    ttk.Label(frm, text="senha: ", font="Arial 16").grid(column=0, row=3)
    senha = ttk.Entry(frm, font="Arial 16", show="*")
    senha.grid(column=1, row=3)

    ttk.Button(frm, text="Esqueceu a Senha?", command=trocar_senha).grid(column=1, row=4)

    ttk.Button(frm, text="Criar conta", command=criar_conta).grid(column=0, row=5)
    ttk.Button(frm, text="Entrar", command=lambda: verificar_login(email, senha)).grid(column=1, row=5)
    ttk.Button(frm, text="Fechar", command=root.destroy).grid(column=2, row=5)


######## MAIN #########
root = Tk()
root.title('Trabalho 3')
frm = ttk.Frame(root, padding=100)
frm.grid()

login()  # Exibe a tela de login inicialmente

root.mainloop()
