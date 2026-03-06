class LibroForm:

    def __init__(self, titulo, autor, cantidad, precio):
        self.titulo = titulo
        self.autor = autor
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "cantidad": self.cantidad,
            "precio": self.precio
        }