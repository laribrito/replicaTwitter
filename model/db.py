import sqlite3
from flask import g

#abre o banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("model/dados.db", \
        detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

#fecha o banco de dados
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#busca um usuário pelo login
def busca_usuario(login):
    con = get_db()
    return con.execute("SELECT * FROM usuario WHERE login = ?",[login]).fetchone()

# Cadastra um usuário no banco
def cadastra_usuario(login, senha, nome):
    con = get_db()
    con.execute("INSERT INTO usuario VALUES(NULL, ?, ?, ?)", \
    [login, senha, nome])
    con.commit()