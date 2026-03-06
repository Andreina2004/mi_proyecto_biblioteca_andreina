# Biblioteca Virtual - Sistema de Inventario

Aplicación web desarrollada con Flask para la gestión de inventario de libros.

## Tecnologías utilizadas
- Python
- Flask
- SQLite
- HTML
- CSS

## Funcionalidades
- Agregar libros
- Buscar libros por título
- Actualizar cantidad y precio
- Eliminar libros
- Visualizar inventario completo

## Programación Orientada a Objetos
Se implementó la clase **Libro** para representar cada libro y la clase **Inventario** para gestionar las operaciones.

## Colecciones utilizadas
- **Listas** para mostrar los libros.
- **Diccionarios** para acceder rápidamente por ID.

## Base de datos
Se utiliza **SQLite** con una tabla llamada `libros` que almacena:
- id
- titulo
- autor
- cantidad
- precio

## CRUD implementado
- Create: agregar libro
- Read: visualizar inventario
- Update: actualizar datos
- Delete: eliminar libro

## Ejecución del proyecto
Para ejecutar el sistema localmente:

```bash
python app.py