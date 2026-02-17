
from flask import Flask, render_template
import os

app = Flask(__name__)

posts = [
    {"titulo": "Primeiro post", "conteudo": "Conteúdo do primeiro post"},
    {"titulo": "Segundo post", "conteudo": "Conteúdo do segundo post"}
]

@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def post(id):
    post = posts[id]
    return render_template("post.html", post=post)

# 👇 ESSA PARTE É OBRIGATÓRIA PARA O RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
