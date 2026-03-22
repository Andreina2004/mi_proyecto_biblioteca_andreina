from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_conn
from form import LibroForm
from inventario.inventario import guardar_txt, guardar_json, guardar_csv, leer_txt, leer_json, leer_csv

app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def init_db():
    try:
        conn = get_conn()
        cursor = conn.cursor()

        print("Conectado a MySQL, creando tablas...")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10,2) NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            mail VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """)

        conn.commit()
        print("Tablas creadas correctamente en MySQL")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error al crear las tablas:", e)


class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, mail, password):
        self.id = id_usuario
        self.nombre = nombre
        self.mail = mail
        self.password = password

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            return Usuario(
                usuario["id_usuario"],
                usuario["nombre"],
                usuario["mail"],
                usuario["password"]
            )
        return None

    @staticmethod
    def obtener_por_mail(mail):
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            return Usuario(
                usuario["id_usuario"],
                usuario["nombre"],
                usuario["mail"],
                usuario["password"]
            )
        return None

    @staticmethod
    def crear(nombre, mail, password):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nombre, mail, password)
        )
        conn.commit()
        cursor.close()
        conn.close()


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))


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
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        self.lista = [
            Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], float(r["precio"]))
            for r in rows
        ]
        self.libros = {l.get_id(): l for l in self.lista}

    def agregar(self, titulo, autor, cantidad, precio):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, cantidad, precio) VALUES (%s, %s, %s, %s)",
            (titulo, autor, cantidad, precio)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar(self, id):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    def actualizar(self, id, cantidad, precio):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE libros SET cantidad = %s, precio = %s WHERE id = %s",
            (cantidad, precio, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def buscar(self, texto):
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM libros WHERE titulo LIKE %s ORDER BY id ASC",
            (f"%{texto}%",)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], float(r["precio"]))
            for r in rows
        ]


inventario = Inventario()
init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        mail = request.form["mail"].strip().lower()
        password = request.form["password"]

        usuario_existente = Usuario.obtener_por_mail(mail)
        if usuario_existente:
            flash("Ese correo ya está registrado.")
            return redirect(url_for("registro"))

        password_hash = generate_password_hash(password)
        Usuario.crear(nombre, mail, password_hash)

        flash("Usuario registrado correctamente. Ahora inicia sesión.")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"].strip().lower()
        password = request.form["password"]

        usuario = Usuario.obtener_por_mail(mail)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash("Inicio de sesión correcto.")
            return redirect(url_for("libros"))
        else:
            flash("Correo o contraseña incorrectos.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("login"))


@app.route("/libros", methods=["GET", "POST"])
@login_required
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
@login_required
def eliminar_libro(id):
    inventario.eliminar(id)
    return redirect(url_for("libros"))


@app.route("/datos")
@login_required
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
@login_required
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

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros")

    for titulo, autor, cantidad, precio in ejemplos:
        cursor.execute(
            "INSERT INTO libros (titulo, autor, cantidad, precio) VALUES (%s, %s, %s, %s)",
            (titulo, autor, cantidad, precio)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("libros"))


if __name__ == "__main__":
    app.run(debug=True)