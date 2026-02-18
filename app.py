from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

posts = [
    {"titulo": "Primeiro post", "conteudo": "Conteúdo do primeiro post"},
    {"titulo": "Segundo post", "conteudo": "Conteúdo do segundo post"}
]

# HOME
@app.route("/")
def home():
    return render_template("index.html", posts=posts)


# VER POST
@app.route("/post/<int:id>")
def post(id):
    return render_template("post.html", post=posts[id], id=id)


# NOVO POST
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]

        posts.append({
            "titulo": titulo,
            "conteudo": conteudo
        })

        return redirect("/")

    return render_template("novo.html")


# EDITAR POST
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        posts[id]["titulo"] = request.form["titulo"]
        posts[id]["conteudo"] = request.form["conteudo"]
        return redirect("/")

    return render_template("editar.html", post=posts[id], id=id)


# APAGAR POST
@app.route("/apagar/<int:id>")
def apagar(id):
    posts.pop(id)
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
