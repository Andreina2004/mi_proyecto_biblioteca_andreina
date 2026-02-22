from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/libros")
def libros():
    lista_libros = [
        {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez"},
        {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes"},
        {"titulo": "Harry Potter y la piedra filosofal", "autor": "J.K. Rowling"}
    ]
    return render_template("libros.html", libros=lista_libros)

if __name__ == "__main__":
    app.run(debug=True)