from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 🔐 chave de segurança
app.config["SECRET_KEY"] = "univesp"

# 🗄️ banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# 📌 MODEL
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)


# 🏠 HOME — LISTAR POSTS
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


# ➕ NOVO POST
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]

        novo_post = Post(titulo=titulo, conteudo=conteudo)
        db.session.add(novo_post)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("novo.html")


# ✏️ EDITAR
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    post = Post.query.get_or_404(id)

    if request.method == "POST":
        post.titulo = request.form["titulo"]
        post.conteudo = request.form["conteudo"]
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("editar.html", post=post)


# ❌ EXCLUIR
@app.route("/excluir/<int:id>")
def excluir(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("home"))


# 🔥 CRIAR BANCO AUTOMATICAMENTE
with app.app_context():
    db.create_all()


# 🚀 RENDER (OBRIGATÓRIO)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
