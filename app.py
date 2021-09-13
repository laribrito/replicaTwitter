from flask import Flask, redirect, url_for, session, request, render_template
from model import db
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)
app.secret_key = b'jhdakjrtyfuygiuhijebson145shsOhkhhujk666'
@app.route("/")
def index():
    if "usuario" in session: #Verifica se "usuario" existe na sessão
        return render_template("PAGINAINICIAL.html", logado=session["usuario"])
    else:
        return render_template("LOGIN.html")

@app.route("/autenticacao/", methods=["POST"])
def autenticacao():
    usuario = db.busca_usuario(request.form["login"])
    if sha256_crypt.verify(request.form["senha"], usuario["senha"]): #testa com uma função do hash se a senha está correta
        session["usuario"] = request.form["login"]
        session["nome"] = usuario["nome"]
        return redirect(url_for("index"))
    else:
        return f"Erro de autenticação."

"""
@app.route("/cadastro/<login>/<nome>/<senha1>/<senha2>") #cadastro um novo usuário
def cadastro(login, nome, senha1, senha2):
    if senha1 == senha2: #confima se as senhas digitadas são iguais
        senha_hash = sha256_crypt.hash(senha1) #efetua o hash na senha
        db.cadastra_usuario(login, \
        senha_hash, nome)
        return f"Usuário cadastrado."
    else:
        return f"As senhas não coincidem"
"""
    
@app.route("/cadastro/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        if request.form["senha1"] == request.form["senha2"]: #confima se as senhas digitadas são iguais
            senha_hash = sha256_crypt.hash(request.form["senha1"]) #efetua o hash na senha
            db.cadastra_usuario(request.form["login"], \
            senha_hash, request.form["nome"])
            return f"Usuário cadastrado."
        else:
            return f"As senhas não coincidem"
    else:
        return render_template("CADASTRO.html")

@app.route("/perfil/<nome>")
@app.route("/perfil")
def perfil(nome=None):
    if nome == session["usuario"] or not nome:
        user = db.busca_usuario(session["usuario"])
        return render_template("PERFIL.html", user=user, logado=session["usuario"])
    else:
        user = db.busca_usuario(nome)
        return render_template("PERFIL.html", user=user, logado=session["usuario"])

@app.route("/perfil/edicao")
def edicao():
    return render_template("EDICAO.html", logado=session["usuario"])

# Pasta com as imagens
app.config['PERFIL_FOLDER'] = 'static/imagens/perfil'
@app.route('/perfil/avatar/<login>')
def perfil_avatar(login):
    # Verifica se o arquivo existe
    if os.path.isfile(f"{app.config['PERFIL_FOLDER']}/{login}"):
        return redirect(f"/{app.config['PERFIL_FOLDER']}/{login}")
    # Se não, exibe o avatar padrão
    else:
        return redirect("/static/imagens/padrao.png")

@app.route('/perfil/foto', methods=["POST"])
def perfil_foto():
    if "foto" not in request.files:
        return "Nenhum arquivo enviado."
    arquivo = request.files["foto"]
    if arquivo.filename == '':
        return "Nenhum arquivo selecionado."
    if arquivo_permitido(arquivo.filename):
        arquivo.save(os.path.join(app.config['PERFIL_FOLDER'],
        session["usuario"]))
        return redirect(url_for('index'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/sair") #Remove "usuario" da sessão
def sair():
    del(session["usuario"])
    del(session["nome"])
    return redirect(url_for("index"))