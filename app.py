from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELO DA TABELA
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)


# CRIAR O BANCO (RODA UMA VEZ SÓ)
with app.app_context():
    db.create_all()


# HOME — LISTAR POSTS
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


# VER POST INDIVIDUAL
@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)


# CRIAR NOVO POST
@app.route("/novo", methods=["GET", "POST"])
def novo_post():

    if request.method == "POST":
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]

        novo = Post(titulo=titulo, conteudo=conteudo)
        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("novo_post.html")


# EDITAR POST
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_post(id):

    post = Post.query.get_or_404(id)

    if request.method == "POST":
        post.titulo = request.form["titulo"]
        post.conteudo = request.form["conteudo"]

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("editar_post.html", post=post)


# APAGAR POST
@app.route("/apagar/<int:id>")
def apagar_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
