# colombian-map-template

## Descripción

Proyecto de análisis exploratorio de datos.

## Estructura del Proyecto

```
colombian-map-template/
├── LICENSE                 # Licencia MIT
├── README.md              # Este archivo
├── requirements.txt       # Dependencias de Python
├── .gitignore            # Archivos ignorados por Git
│
├── data/                 # Datos del proyecto
│   ├── raw/             # Datos originales sin procesar
│   ├── temp/            # Datos temporales
│   └── processed/       # Datos procesados y limpios
│
├── notebooks/           # Notebooks de Jupyter organizados por fase
│   ├── 0_exploracion/  # Análisis exploratorio inicial
│   ├── 1_limpieza/     # Limpieza y preparación de datos
│   ├── 2_stats/        # Análisis estadístico
│   ├── 3_modelacion/   # Modelado y algoritmos
│   └── 9_reportes/     # Reportes finales
│
├── src/                # Código fuente
│   └── python/        # Scripts de Python
│       ├── cleaning/  # Funciones de limpieza
│       ├── models/    # Modelos y algoritmos
│       └── evaluation/ # Evaluación de resultados
│
├── outputs/           # Resultados generados
│   ├── other/        # Otros archivos de salida
│   ├── figures/      # Gráficos y visualizaciones
│   ├── tables/       # Tablas generadas
│   ├── bib/          # Referencias bibliográficas (BibTeX)
│   ├── lit/          # Literatura y documentos de referencia
│   ├── slides/       # Presentaciones
│   └── docs/         # Documentación generada
│
├── tools/            # Herramientas y scripts auxiliares
│
└── docs/             # Documentación del proyecto
    ├── methodology.md   # Metodología utilizada
    ├── pseudocode.md    # Pseudocódigo y planificación
    ├── document/        # Documentos formales
    └── slides/          # Presentaciones del proyecto
```

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd colombian-map-template
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de Rutas (paths.yml)

Este proyecto utiliza archivos `paths.yml` para gestionar las rutas de manera flexible entre diferentes entornos.

### ⚠️ Importante

Los archivos `paths.yml` están excluidos del control de versiones (`.gitignore`) porque contienen rutas absolutas específicas de cada máquina.

### Cómo Configurar

1. **Ubicaciones donde crear `paths.yml`:**
   - `notebooks/0_exploracion/paths.yml`
   - `notebooks/1_limpieza/paths.yml`
   - `notebooks/2_stats/paths.yml`
   - `notebooks/3_modelacion/paths.yml`
   - `notebooks/9_reportes/paths.yml`
   - `src/python/cleaning/paths.yml`
   - `src/python/models/paths.yml`
   - `src/python/evaluation/paths.yml`

2. **Estructura de cada archivo `paths.yml`:**

```yaml
project:
  root: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template"

data:
  raw: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/data/raw"
  temp: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/data/temp"
  processed: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/data/processed"

outputs:
  figures: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/outputs/figures"
  tables: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/outputs/tables"
  slides: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/outputs/slides"
  docs: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/outputs/docs"
  model: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/outputs/model"

logs:
  root: "<RUTA_ABSOLUTA_A_TU_PROYECTO>/colombian-map-template/logs"
```

3. **Reemplaza** `<RUTA_ABSOLUTA_A_TU_PROYECTO>` con la ruta real donde clonaste el proyecto.

### Ejemplo en diferentes sistemas operativos:

**Linux/macOS:**
```yaml
project:
  root: "/home/usuario/proyectos/colombian-map-template"
```

**Windows:**
```yaml
project:
  root: "C:/Users/usuario/proyectos/colombian-map-template"
```

### Uso en código

```python
import yaml

# Cargar configuración de rutas
with open('paths.yml', 'r') as f:
    paths = yaml.safe_load(f)

# Usar rutas
data_raw = paths['data']['raw']
output_figures = paths['outputs']['figures']
```

## Uso

1. Coloca tus datos crudos en `data/raw/`
2. Ejecuta los notebooks en orden numérico según la fase del análisis
3. Los resultados se guardarán automáticamente en `outputs/`

## Metodología

Consulta [docs/methodology.md](docs/methodology.md) para detalles sobre la metodología empleada.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para preguntas o colaboraciones, por favor contacta al equipo del proyecto.
