from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Biblioteca Virtual – Consulta de libros y disponibilidad"

# Ruta dinámica
@app.route('/libro/<titulo>')
def libro(titulo):
    return f"Libro: {titulo} – consulta exitosa."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)