import pandas as pd
from fpdf import FPDF


def sanitize_text(text):
    """
    Reemplazar caracteres problemáticos con caracteres seguros para latin-1.
    """
    if pd.isna(text):
        return ""
    replacements = {
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"',
        # Puedes añadir más reemplazos si encuentras otros caracteres problemáticos
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def csv_to_pdf(csv_file_path, pdf_file_path):
    # Leer el archivo CSV con pandas
    df = pd.read_csv('C:/Users/natal/OneDrive/Escritorio/Canadian Pr/datasets/combined_data_no_dates.csv', encoding='latin-1')

    # Crear un objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Configurar fuente
    pdf.set_font("Arial", size=8)

    # Agregar título
    pdf.cell(200, 10, txt="Datos Combinados (Mergeados)", ln=True, align="C")

    # Añadir contenido de CSV a PDF
    col_names = list(df.columns)
    pdf.set_font("Arial", size=6)
    
    # Añadir nombres de columnas
    col_width = pdf.w / len(col_names)
    for col in col_names:
        pdf.cell(col_width, 10, col, border=1)
    pdf.ln()
    
    # Añadir filas de datos
    for index, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(item), border=1)
        pdf.ln()

    # Guardar el archivo PDF
    pdf.output(pdf_file_path)
    print(f"Archivo PDF guardado en: {pdf_file_path}")

# Usar la función para convertir el CSV a PDF
csv_to_pdf('combined_data_no_dates.csv', 'combined_data_no_dates.pdf')
