# 🗺️ Plantilla de Mapas Colombia — Estilo IGAC

Repositorio para generar mapas estandarizados de Colombia en Python,
replicando el estilo del visor oficial del IGAC.

---

## 📁 Estructura del repositorio

```
colombia_mapas/
├── data/                    ← Shapefiles van aquí (no se suben a git)
│   ├── departamentos.shp    ← REQUERIDO
│   ├── municipios.shp       ← opcional
│   └── rios_principales.shp ← opcional
├── output/                  ← PNGs generados (no se suben a git)
├── scripts/
│   └── mapa_colombia.py     ← Script principal
├── requirements.txt
└── README.md
```

---

## 📥 Descarga de Shapefiles

### 1. Departamentos (REQUERIDO)
**IGAC — Datos Abiertos Geográficos**
- URL: https://www.igac.gov.co/es/contenido/datos-abiertos-geograficos
- Buscar: "Departamentos de Colombia"
- O directamente: https://geoportal.dane.gov.co/
  → Catálogo → División político-administrativa → Departamentos

### 2. Municipios (opcional, para detalle)
- Misma fuente DANE/IGAC
- Buscar: "Municipios de Colombia"

### 3. Ríos principales (opcional)
**IDEAM — Sistema de Información Ambiental**
- URL: http://www.ideam.gov.co/web/agua/visor-geografico
- Buscar: "Red hídrica escala 1:500.000"
- O desde: https://www.datos.gov.co → buscar "ríos Colombia shapefile"

### 4. Alternativa rápida con Python (sin descargar manualmente)
```python
# Puedes usar naturalearthdata para datos base globales
import geopandas as gpd
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
colombia = world[world.name == "Colombia"]
# Nota: baja resolución, solo para pruebas
```

---

## ⚙️ Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```
---

## 🚀 Uso básico

```python
from scripts.mapa_colombia import crear_mapa

# Mapa básico
crear_mapa(titulo="Departamentos de Colombia")

# Mapa con municipios y ríos
crear_mapa(
    titulo="División político-administrativa",
    mostrar_municipios=True,
    mostrar_rios=True,
    nombre_salida="mapa_completo.png"
)

# Mapa coroplético (con datos propios)
import geopandas as gpd
deptos = gpd.read_file("data/departamentos.shp")
deptos["poblacion"] = [...]   # tu columna de datos

crear_mapa(
    titulo="Población por departamento",
    columna_coro="poblacion",
    cmap_coro="YlOrRd",
    nombre_salida="mapa_poblacion.png"
)
```

---

## 🎨 Personalización del estilo

Todos los parámetros visuales están centralizados en el diccionario `STYLE`
al inicio del script. Cambia ahí los colores, grosores y fuentes para
que todos tus mapas queden consistentes automáticamente:

```python
STYLE = {
    "departamentos_fill":  "#d4edda",   # color de relleno
    "departamentos_edge":  "#6c9b7d",   # color de bordes
    "rios_color":          "#a8d5e2",   # color de ríos
    "dpi":                  300,        # resolución de exportación
    # ...
}
```

---

## 📐 Proyección

Este repositorio usa **EPSG:9377** (MAGNA-SIRGAS / Origen Nacional),
que es la proyección oficial adoptada por Colombia desde 2020 según
el IGAC. Esto garantiza que las distancias y áreas sean correctas
para el territorio colombiano.

---

## 📌 .gitignore recomendado

```
data/
output/
venv/
__pycache__/
*.pyc
```

---

## 📚 Fuentes oficiales

| Entidad | Portal | Datos |
|--------|--------|-------|
| IGAC | igac.gov.co | Cartografía oficial |
| DANE | geoportal.dane.gov.co | División político-admin |
| IDEAM | ideam.gov.co | Hidrografía, clima |
| datos.gov.co | datos.gov.co | Datos abiertos del Estado |
