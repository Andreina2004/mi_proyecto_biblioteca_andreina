from conexion.conexion import get_conn


class PrestamoService:

    @staticmethod
    def crear(id_usuario, id_libro, fecha_prestamo, fecha_devolucion, estado):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion, estado)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_usuario, id_libro, fecha_prestamo, fecha_devolucion, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def listar_con_detalle():
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                p.id_prestamo,
                u.nombre AS usuario,
                l.titulo AS libro,
                p.fecha_prestamo,
                p.fecha_devolucion,
                p.estado
            FROM prestamos p
            INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
            INNER JOIN libros l ON p.id_libro = l.id
            ORDER BY p.id_prestamo ASC
            """
        )
        prestamos = cursor.fetchall()
        cursor.close()
        conn.close()
        return prestamos