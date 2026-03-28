from conexion.conexion import get_conn
from models.usuario import Usuario


class UsuarioService:

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

    @staticmethod
    def listar():
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios ORDER BY nombre ASC")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios