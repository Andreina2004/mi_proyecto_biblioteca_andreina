class Prestamo:
    def __init__(self, id_prestamo, id_usuario, id_libro, fecha_prestamo, fecha_devolucion, estado):
        self.id_prestamo = id_prestamo
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado