class LibroForm:
    def __init__(self, titulo, autor, cantidad, precio):
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def is_valid(self):
        return (
            self.titulo != ""
            and self.autor != ""
            and self.cantidad >= 0
            and self.precio >= 0
        )

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "cantidad": self.cantidad,
            "precio": self.precio
        }