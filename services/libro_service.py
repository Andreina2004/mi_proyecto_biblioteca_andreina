from conexion.conexion import get_conn
from models.libro import Libro


class LibroService:

    @staticmethod
    def listar():
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], float(r["precio"]))
            for r in rows
        ]

    @staticmethod
    def obtener_por_id(id_libro):
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libros WHERE id = %s", (id_libro,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Libro(row["id"], row["titulo"], row["autor"], row["cantidad"], float(row["precio"]))
        return None

    @staticmethod
    def agregar(titulo, autor, cantidad, precio):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, cantidad, precio) VALUES (%s, %s, %s, %s)",
            (titulo, autor, cantidad, precio)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def actualizar(id_libro, titulo, autor, cantidad, precio):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE libros
            SET titulo = %s, autor = %s, cantidad = %s, precio = %s
            WHERE id = %s
            """,
            (titulo, autor, cantidad, precio, id_libro)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def eliminar(id_libro):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = %s", (id_libro,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar(texto):
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM libros
            WHERE titulo LIKE %s OR autor LIKE %s
            ORDER BY id ASC
            """,
            (f"%{texto}%", f"%{texto}%")
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            Libro(r["id"], r["titulo"], r["autor"], r["cantidad"], float(r["precio"]))
            for r in rows
        ]

    @staticmethod
    def resetear_y_cargar_ejemplos():
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