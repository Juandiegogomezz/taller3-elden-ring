import requests
from pymongo import MongoClient

# --- Configuración ---
API_URL = "https://eldenring.fanapis.com/api/weapons"
LIMIT = 100          # registros por página
MAX_PAGES = 50       # tope de seguridad para evitar un ciclo infinito
MONGO_URI = "mongodb://localhost:27017/"

# --- Conexión a MongoDB ---
client = MongoClient(MONGO_URI)
coleccion = client["taller3_db"]["raw_data"]

# --- Descarga y guardado ---
total = 0
for pagina in range(MAX_PAGES):
    respuesta = requests.get(API_URL, params={"limit": LIMIT, "page": pagina}, timeout=30)
    respuesta.raise_for_status()
    items = respuesta.json().get("data", [])

    if not items:
        break

    for doc in items:
        doc["_id"] = doc["id"]  # el id de la API pasa a ser el _id de Mongo
        coleccion.replace_one({"_id": doc["_id"]}, doc, upsert=True)

    total += len(items)
    print(f"Página {pagina}: {len(items)} armas procesadas")

    if len(items) < LIMIT:
        break  # última página

print(f"\nTotal procesado: {total}")
print(f"Documentos en taller3_db.raw_data: {coleccion.count_documents({})}")