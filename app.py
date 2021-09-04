from flask import Flask, redirect, url_for, session, request, render_template
from model import db
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = b'jhdakjrtyfuygiuhijebson145shsOhkhhujk666'
@app.route("/")
def index():
    if "usuario" in session: #Verifica se "usuario" existe na sessão
        return f"Olá, {session['usuario']}"
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


@app.route("/sair") #Remove "usuario" da sessão
def sair():
    del(session["usuario"])
    del(session["nome"])
    return redirect(url_for("index"))