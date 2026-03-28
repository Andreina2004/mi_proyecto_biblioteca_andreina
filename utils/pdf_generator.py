from fpdf import FPDF


def generar_pdf_libros(libros, ruta_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Reporte de Libros", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(15, 10, "ID", 1)
    pdf.cell(65, 10, "Titulo", 1)
    pdf.cell(45, 10, "Autor", 1)
    pdf.cell(25, 10, "Cantidad", 1)
    pdf.cell(40, 10, "Precio", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)

    for libro in libros:
        pdf.cell(15, 10, str(libro.id), 1)
        pdf.cell(65, 10, str(libro.titulo)[:30], 1)
        pdf.cell(45, 10, str(libro.autor)[:20], 1)
        pdf.cell(25, 10, str(libro.cantidad), 1)
        pdf.cell(40, 10, f"${libro.precio:.2f}", 1)
        pdf.ln()

    pdf.output(ruta_archivo)