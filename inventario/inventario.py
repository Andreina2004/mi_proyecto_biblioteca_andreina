import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Crear carpeta data si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

TXT_FILE = os.path.join(DATA_DIR, "datos.txt")
JSON_FILE = os.path.join(DATA_DIR, "datos.json")
CSV_FILE = os.path.join(DATA_DIR, "datos.csv")


# ---------- GUARDAR EN TXT ----------
def guardar_txt(libro):

    with open(TXT_FILE, "a", encoding="utf-8") as f:
        linea = f"{libro['titulo']},{libro['autor']},{libro['cantidad']},{libro['precio']}\n"
        f.write(linea)


# ---------- LEER TXT ----------
def leer_txt():

    datos = []

    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 4:
                    datos.append({
                        "titulo": partes[0],
                        "autor": partes[1],
                        "cantidad": partes[2],
                        "precio": partes[3]
                    })

    return datos


# ---------- GUARDAR JSON ----------
def guardar_json(libro):

    datos = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
            except:
                datos = []

    datos.append(libro)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# ---------- LEER JSON ----------
def leer_json():

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []

    return []


# ---------- GUARDAR CSV ----------
def guardar_csv(libro):

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["titulo", "autor", "cantidad", "precio"])

        writer.writerow([
            libro["titulo"],
            libro["autor"],
            libro["cantidad"],
            libro["precio"]
        ])


# ---------- LEER CSV ----------
def leer_csv():

    datos = []

    if os.path.exists(CSV_FILE):

        with open(CSV_FILE, "r", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:
                datos.append(row)

    return datos