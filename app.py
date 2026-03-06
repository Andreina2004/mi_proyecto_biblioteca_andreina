from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

from form import LibroForm
from inventario.inventario import guardar_txt, guardar_json, guardar_csv, leer_txt, leer_json, leer_csv

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "biblioteca.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
        """)
        conn.commit()


class Libro:
    def __init__(self, id, titulo, autor, cantidad, precio):
        self._id = id
        self._titulo = titulo
        self._autor = autor
        self._cantidad = cantidad
        self._precio = precio

    def get_id(self):
        return self._id

    def get_titulo(self):
        return self._titulo

    def get_autor(self):
        return self._autor

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio


class Inventario:
    def __init__(self):
        self.libros = {}
        self.lista = []

    def cargar(self):
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM libros ORDER BY id ASC").fetchall()

        self.lista = [Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], r["precio"]) for r in rows]
        self.libros = {l.get_id(): l for l in self.lista}

    def agregar(self, titulo, autor, cantidad, precio):
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO libros(titulo, autor, cantidad, precio) VALUES (?, ?, ?, ?)",
                (titulo, autor, cantidad, precio)
            )
            conn.commit()

    def eliminar(self, id):
        with get_conn() as conn:
            conn.execute("DELETE FROM libros WHERE id = ?", (id,))
            conn.commit()

    def actualizar(self, id, cantidad, precio):
        with get_conn() as conn:
            conn.execute(
                "UPDATE libros SET cantidad = ?, precio = ? WHERE id = ?",
                (cantidad, precio, id)
            )
            conn.commit()

    def buscar(self, texto):
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM libros WHERE titulo LIKE ? ORDER BY id ASC",
                (f"%{texto}%",)
            ).fetchall()

        return [Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], r["precio"]) for r in rows]


inventario = Inventario()
init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/libros", methods=["GET", "POST"])
def libros():
    resultados = None

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar":
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])

            inventario.agregar(titulo, autor, cantidad, precio)

            libro_form = LibroForm(titulo, autor, cantidad, precio)
            libro_dict = libro_form.to_dict()

            guardar_txt(libro_dict)
            guardar_json(libro_dict)
            guardar_csv(libro_dict)

            return redirect(url_for("libros"))

        elif accion == "buscar":
            texto = request.form["buscar"]
            inventario.cargar()
            resultados = inventario.buscar(texto)
            return render_template("libros.html", libros=inventario.lista, resultados=resultados)

        elif accion == "actualizar":
            id_libro = int(request.form["id"])
            cantidad = int(request.form["nueva_cantidad"])
            precio = float(request.form["nuevo_precio"])
            inventario.actualizar(id_libro, cantidad, precio)
            return redirect(url_for("libros"))

    inventario.cargar()
    return render_template("libros.html", libros=inventario.lista, resultados=resultados)


@app.route("/libros/eliminar/<int:id>", methods=["POST"])
def eliminar_libro(id):
    inventario.eliminar(id)
    return redirect(url_for("libros"))


@app.route("/datos")
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()

    return render_template(
        "datos.html",
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv
    )


@app.route("/reset_and_seed")
def reset_and_seed():
    ejemplos = [
        ("Cien años de soledad", "Gabriel García Márquez", 8, 12.50),
        ("Don Quijote de la Mancha", "Miguel de Cervantes", 6, 15.00),
        ("La Odisea", "Homero", 10, 9.99),
        ("El amor en los tiempos del cólera", "Gabriel García Márquez", 7, 11.25),
        ("1984", "George Orwell", 12, 10.00),
        ("Rebelión en la granja", "George Orwell", 9, 7.50),
        ("El Principito", "Antoine de Saint-Exupéry", 5, 10.00),
        ("Harry Potter y la piedra filosofal", "J.K. Rowling", 15, 14.99),
        ("Harry Potter y la cámara secreta", "J.K. Rowling", 13, 14.99),
        ("Harry Potter y el prisionero de Azkaban", "J.K. Rowling", 11, 14.99),
        ("El señor de los anillos", "J.R.R. Tolkien", 4, 19.99),
        ("El Hobbit", "J.R.R. Tolkien", 9, 13.99),
        ("Crónica de una muerte anunciada", "Gabriel García Márquez", 10, 8.75),
        ("Rayuela", "Julio Cortázar", 6, 12.00),
        ("Ficciones", "Jorge Luis Borges", 8, 9.50),
        ("La ciudad y los perros", "Mario Vargas Llosa", 5, 10.50),
        ("Pedro Páramo", "Juan Rulfo", 7, 8.25),
        ("La sombra del viento", "Carlos Ruiz Zafón", 9, 13.50),
        ("Orgullo y prejuicio", "Jane Austen", 10, 9.99),
        ("Frankenstein", "Mary Shelley", 6, 8.99),
    ]

    with get_conn() as conn:
        conn.execute("DELETE FROM libros")
        for titulo, autor, cantidad, precio in ejemplos:
            conn.execute(
                "INSERT INTO libros(titulo, autor, cantidad, precio) VALUES (?, ?, ?, ?)",
                (titulo, autor, cantidad, precio)
            )
        conn.commit()

    return redirect(url_for("libros"))


if __name__ == "__main__":
    app.run(debug=True)