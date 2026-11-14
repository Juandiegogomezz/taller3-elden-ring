# Taller 3: APIs públicas, MongoDB y EDA — Armas de Elden Ring

Proyecto del curso **Bases de Datos para Ciencia de Datos** (docente: Miguel Ramos García).
Autor: [Juan Diego Gómez Giraldo]

## Nota
plena confianza en que el docente conozca el videojuego, en caso de que no:
**Elden Ring** es un videojuego de rol y acción desarrollado por FromSoftware, ambientado en un mundo de fantasía conocido como las Tierras Intermedias. El juego cuenta con una amplia variedad de armas, cada una con características, atributos y propiedades particulares. Para este trabajo se utilizó una API relacionada con las armas de Elden Ring como fuente de datos, con el propósito de realizar procesos de extracción, exploración y análisis de datos a partir de la información proporcionada.

## Descripción

Flujo de ciencia de datos de punta a punta:

1. **Extracción:** descarga de las armas de Elden Ring desde una API pública.
2. **Almacenamiento RAW:** carga de los datos sin modificar en MongoDB.
3. **Análisis (EDA):** lectura desde MongoDB, limpieza con pandas, 5 insights numéricos y visualizaciones.

## API utilizada

[Elden Ring API](https://docs.eldenring.fanapis.com/docs/weapons), ruta de armas:
`https://eldenring.fanapis.com/api/weapons`

- Pública y gratuita, no requiere llave.
- Se descargaron **306 armas** (el mínimo del taller es 100).
- Cada arma incluye nombre, categoría, peso, descripción, ataque, defensa, requisitos de atributos y escalado.

## Estructura del repositorio

| Archivo | Descripción |
|---|---|
| `ingesta.py` | Descarga las armas de la API y las guarda en MongoDB |
| `analisis.ipynb` | Notebook con la limpieza, el EDA y las visualizaciones |
| `requirements.txt` | Librerías necesarias |
| `.gitignore` | Archivos excluidos del repositorio |

## Cómo ejecutarlo

### Requisitos previos
- Python 3.10 o superior (probado con Python 3.13).
- MongoDB Community Server corriendo en `localhost:27017` (se recomienda MongoDB Compass para ver los datos).

### Pasos

1. Clonar el repositorio y entrar a la carpeta:
   ```
   git clone https://github.com/[tu-usuario]/taller3-elden-ring.git
   cd taller3-elden-ring
   ```
2. Crear y activar un entorno virtual (Windows):
   ```
   py -3.13 -m venv venv
   venv\Scripts\activate
   ```
3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Cargar los datos en MongoDB (crea la base `taller3_db` y la colección `raw_data`):
   ```
   python ingesta.py
   ```
5. Abrir el notebook y ejecutarlo completo (**Kernel → Restart & Run All**):
   ```
   jupyter notebook analisis.ipynb
   ```

## Decisiones de diseño

- **Datos crudos:** los documentos se guardan tal como llegan de la API. Lo único que se agrega es el campo `_id`, que toma el valor del `id` de la API.
- **Sin duplicados:** `ingesta.py` usa `replace_one(..., upsert=True)`, así que se puede ejecutar varias veces sin duplicar documentos.
- **Limpieza en el notebook:** las listas anidadas (`attack`, `requiredAttributes`, `scalesWith`) se aplanan a columnas, y las armas sin un requisito o un tipo de ataque se tratan como 0.

## Principales hallazgos

- Las 306 armas se reparten en 31 categorías sin que ninguna domine (la mayor, Greatsword, tiene 20).
- El peso promedio es 7,09 y la mayoría de las armas es ligera.
- La Fuerza es el atributo más exigido (50,3 % de las armas), seguida de la Destreza (28,4 %).
- Exigir Fuerza no equivale a escalar con ella: solo 3 armas escalan con Fuerza en grado A o B.
- Las armas con mejor escalado total son híbridas, con tres atributos a la vez.

Las conclusiones completas están en la última sección del notebook.

## Limitaciones

La API entrega el daño y el escalado base de cada arma. No incluye el daño final con atributos, las mejoras de arma, el alcance, la velocidad ni los efectos de estado, por lo que el análisis describe el perfil del arsenal pero no determina cuál es la mejor arma del juego.