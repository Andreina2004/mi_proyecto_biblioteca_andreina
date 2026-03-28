from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os

from services.usuario_service import UsuarioService
from services.libro_service import LibroService
from services.prestamo_service import PrestamoService
from forms.libro_form import LibroForm
from utils.pdf_generator import generar_pdf_libros
from inventario.inventario import leer_txt, leer_json, leer_csv

app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return UsuarioService.obtener_por_id(int(user_id))


@app.route("/")
def index():
    return render_template("general/index.html")


@app.route("/about")
def about():
    return render_template("general/about.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        mail = request.form["mail"].strip().lower()
        password = request.form["password"]

        if UsuarioService.obtener_por_mail(mail):
            flash("Ese correo ya está registrado.")
            return redirect(url_for("registro"))

        password_hash = generate_password_hash(password)
        UsuarioService.crear(nombre, mail, password_hash)

        flash("Usuario registrado correctamente. Ahora inicia sesión.")
        return redirect(url_for("login"))

    return render_template("usuarios/registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"].strip().lower()
        password = request.form["password"]

        usuario = UsuarioService.obtener_por_mail(mail)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash("Inicio de sesión correcto.")
            return redirect(url_for("libros"))
        else:
            flash("Correo o contraseña incorrectos.")

    return render_template("usuarios/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("login"))


@app.route("/libros")
@login_required
def libros():
    lista_libros = LibroService.listar()
    return render_template("libros/listar.html", libros=lista_libros)


@app.route("/libros/crear", methods=["GET", "POST"])
@login_required
def crear_libro():
    if request.method == "POST":
        form = LibroForm(
            request.form["titulo"],
            request.form["autor"],
            request.form["cantidad"],
            request.form["precio"]
        )

        if not form.is_valid():
            flash("Datos inválidos.")
            return redirect(url_for("crear_libro"))

        LibroService.agregar(
            form.titulo,
            form.autor,
            form.cantidad,
            form.precio
        )

        flash("Libro agregado correctamente.")
        return redirect(url_for("libros"))

    return render_template("libros/crear_libro.html")


@app.route("/libros/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_libro(id):
    libro = LibroService.obtener_por_id(id)

    if not libro:
        flash("Libro no encontrado.")
        return redirect(url_for("libros"))

    if request.method == "POST":
        LibroService.actualizar(
            id,
            request.form["titulo"],
            request.form["autor"],
            int(request.form["cantidad"]),
            float(request.form["precio"])
        )
        flash("Libro actualizado correctamente.")
        return redirect(url_for("libros"))

    return render_template("libros/editar_libro.html", libro=libro)


@app.route("/libros/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_libro(id):
    LibroService.eliminar(id)
    flash("Libro eliminado correctamente.")
    return redirect(url_for("libros"))


@app.route("/libros/buscar", methods=["POST"])
@login_required
def buscar_libro():
    texto = request.form["buscar"]
    resultados = LibroService.buscar(texto)
    return render_template("libros/listar.html", libros=resultados)


@app.route("/libros/pdf")
@login_required
def reporte_libros_pdf():
    lista_libros = LibroService.listar()
    ruta_pdf = os.path.join(os.getcwd(), "reporte_libros.pdf")
    generar_pdf_libros(lista_libros, ruta_pdf)

    return send_file(
        ruta_pdf,
        as_attachment=True,
        download_name="reporte_libros.pdf"
    )


@app.route("/prestamos", methods=["GET", "POST"])
@login_required
def prestamos():
    if request.method == "POST":
        id_usuario = int(request.form["id_usuario"])
        id_libro = int(request.form["id_libro"])
        fecha_prestamo = request.form["fecha_prestamo"]
        fecha_devolucion = request.form["fecha_devolucion"]
        estado = request.form["estado"]

        PrestamoService.crear(
            id_usuario,
            id_libro,
            fecha_prestamo,
            fecha_devolucion,
            estado
        )

        flash("Préstamo registrado correctamente.")
        return redirect(url_for("prestamos"))

    lista_prestamos = PrestamoService.listar_con_detalle()
    usuarios = UsuarioService.listar()
    libros = LibroService.listar()

    return render_template(
        "prestamos/listar_prestamos.html",
        prestamos=lista_prestamos,
        usuarios=usuarios,
        libros=libros
    )


@app.route("/datos")
@login_required
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()

    return render_template(
        "general/datos.html",
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv
    )


@app.route("/reset_and_seed")
@login_required
def reset_and_seed():
    LibroService.resetear_y_cargar_ejemplos()
    flash("Datos de ejemplo cargados correctamente.")
    return redirect(url_for("libros"))


if __name__ == "__main__":
    app.run(debug=True)