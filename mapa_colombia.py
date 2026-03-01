"""
Plantilla estándar de mapas Colombia - estilo IGAC
==================================================
Autor: Tu nombre
Proyección oficial: EPSG:9377 (MAGNA-SIRGAS / Origen Nacional)

Estructura esperada de /data:
    departamentos.shp
    municipios.shp         (opcional)
    rios_principales.shp   (opcional)
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
import contextily as ctx
import numpy as np
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL (estandarización)
# ─────────────────────────────────────────────

STYLE = {
    # Colores
    "departamentos_fill":   "#d4edda",   # verde claro (tierra)
    "departamentos_edge":   "#6c9b7d",   # borde departamental
    "municipios_edge":      "#b0c4b8",   # borde municipal (más suave)
    "rios_color":           "#a8d5e2",   # azul agua
    "borde_nacional":       "#3a5a40",   # borde exterior grueso

    # Grosores
    "lw_departamentos":     0.8,
    "lw_municipios":        0.3,
    "lw_rios":              0.6,
    "lw_borde_nacional":    1.5,

    # Tipografía
    "font_family":          "DejaVu Sans",
    "font_size_depto":      7,
    "font_size_titulo":     14,
    "font_color":           "#1a1a2e",

    # Figura
    "figsize":              (12, 14),
    "dpi":                  300,
    "fondo_figura":         "#f0f4f8",   # color de fondo del lienzo
    "fondo_agua":           "#cce5f0",   # color del océano/fondo tile
}

EPSG_COLOMBIA = 9377   # Proyección oficial IGAC
EPSG_WEB      = 3857   # Web Mercator (para contextily)

DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


# ─────────────────────────────────────────────
# FUNCIONES DE CARGA
# ─────────────────────────────────────────────

def cargar_capa(nombre_shp: str, epsg_destino: int = EPSG_COLOMBIA):
    """Carga un shapefile y lo reproyecta."""
    ruta = os.path.join(DATA_DIR, nombre_shp)
    if not os.path.exists(ruta):
        print(f"  [!] Capa no encontrada: {nombre_shp} — se omite")
        return None
    gdf = gpd.read_file(ruta)
    return gdf.to_crs(epsg=epsg_destino)


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE MAPA
# ─────────────────────────────────────────────

def crear_mapa(
    titulo: str = "Departamentos de Colombia",
    mostrar_municipios: bool = False,
    mostrar_rios: bool = True,
    mostrar_etiquetas: bool = True,
    usar_basemap: bool = True,
    columna_coro: str = None,          # columna para mapa coroplético
    cmap_coro: str = "YlGn",
    nombre_salida: str = "mapa_colombia.png",
):
    """
    Genera un mapa estandarizado de Colombia.

    Parámetros
    ----------
    titulo           : Título del mapa
    mostrar_municipios: Agregar capa de municipios
    mostrar_rios     : Agregar red hídrica
    mostrar_etiquetas: Nombres de departamentos
    usar_basemap     : Fondo contextily (requiere internet)
    columna_coro     : Si se pasa, hace mapa coroplético con esa columna
    cmap_coro        : Paleta de colores para coroplético
    nombre_salida    : Nombre del archivo PNG en /output
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Cargar capas ──────────────────────────
    deptos    = cargar_capa("departamentos.shp")
    municipios = cargar_capa("municipios.shp")   if mostrar_municipios else None
    rios      = cargar_capa("rios_principales.shp") if mostrar_rios    else None

    if deptos is None:
        raise FileNotFoundError(
            "Necesitas el archivo 'departamentos.shp' en la carpeta /data.\n"
            "Descárgalo en: https://www.igac.gov.co/es/contenido/datos-abiertos-geograficos\n"
            "o en: https://geoportal.dane.gov.co/"
        )

    # ── Figura ────────────────────────────────
    fig, ax = plt.subplots(figsize=STYLE["figsize"], facecolor=STYLE["fondo_figura"])
    ax.set_facecolor(STYLE["fondo_agua"])

    # ── Basemap (fondo geográfico) ─────────────
    if usar_basemap:
        deptos_web = deptos.to_crs(epsg=EPSG_WEB)
        ax_web = fig.add_axes(ax.get_position())   # eje auxiliar para basemap
        deptos_web.plot(ax=ax_web, alpha=0)         # solo para setear extent
        ctx.add_basemap(
            ax_web,
            source=ctx.providers.CartoDB.Positron,
            zoom="auto",
        )
        # Convertir extent del basemap a EPSG_COLOMBIA para el eje principal
        # (más sencillo: simplemente plot en EPSG_COLOMBIA sobre el fondo)
        ax_web.set_visible(False)

    # ── Municipios (fondo) ────────────────────
    if municipios is not None:
        municipios.plot(
            ax=ax,
            color="none",
            edgecolor=STYLE["municipios_edge"],
            linewidth=STYLE["lw_municipios"],
            zorder=2,
        )

    # ── Departamentos ─────────────────────────
    if columna_coro and columna_coro in deptos.columns:
        deptos.plot(
            ax=ax,
            column=columna_coro,
            cmap=cmap_coro,
            edgecolor=STYLE["departamentos_edge"],
            linewidth=STYLE["lw_departamentos"],
            legend=True,
            legend_kwds={"shrink": 0.5, "label": columna_coro},
            zorder=3,
        )
    else:
        deptos.plot(
            ax=ax,
            color=STYLE["departamentos_fill"],
            edgecolor=STYLE["departamentos_edge"],
            linewidth=STYLE["lw_departamentos"],
            zorder=3,
        )

    # ── Borde nacional (contorno exterior grueso) ──
    deptos.dissolve().plot(
        ax=ax,
        color="none",
        edgecolor=STYLE["borde_nacional"],
        linewidth=STYLE["lw_borde_nacional"],
        zorder=4,
    )

    # ── Ríos ──────────────────────────────────
    if rios is not None:
        rios.plot(
            ax=ax,
            color=STYLE["rios_color"],
            linewidth=STYLE["lw_rios"],
            zorder=5,
        )

    # ── Etiquetas de departamentos ────────────
    if mostrar_etiquetas:
        col_nombre = _detectar_columna_nombre(deptos)
        for _, row in deptos.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(
                text=row[col_nombre].upper() if col_nombre else "",
                xy=(centroid.x, centroid.y),
                ha="center", va="center",
                fontsize=STYLE["font_size_depto"],
                fontfamily=STYLE["font_family"],
                color=STYLE["font_color"],
                fontweight="bold",
                path_effects=[
                    pe.withStroke(linewidth=2, foreground="white")
                ],
                zorder=6,
            )

    # ── Elementos cartográficos ───────────────
    _agregar_norte(ax)
    _agregar_escala(ax, deptos)
    _agregar_creditos(ax)

    # ── Título y estilo general ───────────────
    ax.set_title(
        titulo,
        fontsize=STYLE["font_size_titulo"],
        fontfamily=STYLE["font_family"],
        fontweight="bold",
        color=STYLE["font_color"],
        pad=15,
    )
    ax.set_axis_off()

    plt.tight_layout()

    # ── Guardar ───────────────────────────────
    ruta_salida = os.path.join(OUTPUT_DIR, nombre_salida)
    plt.savefig(ruta_salida, dpi=STYLE["dpi"], bbox_inches="tight",
                facecolor=STYLE["fondo_figura"])
    print(f"✓ Mapa guardado en: {ruta_salida}")
    plt.show()
    return fig, ax


# ─────────────────────────────────────────────
# HELPERS CARTOGRÁFICOS
# ─────────────────────────────────────────────

def _detectar_columna_nombre(gdf):
    """Busca la columna de nombre más probable en el shapefile."""
    candidatos = ["NOMBRE_DEP", "DPTO_CNMBR", "NOM_DEP", "nombre", "NOMBRE",
                  "NAME", "name", "departamento", "DEPARTAMENTO"]
    for c in candidatos:
        if c in gdf.columns:
            return c
    # Si no encuentra, retorna la primera columna de texto
    for c in gdf.columns:
        if gdf[c].dtype == object:
            return c
    return None


def _agregar_norte(ax, x=0.97, y=0.97, size=20):
    """Agrega símbolo de norte."""
    ax.annotate(
        "N", xy=(x, y), xycoords="axes fraction",
        ha="center", va="center",
        fontsize=size, fontweight="bold",
        color=STYLE["font_color"],
        xytext=(x, y - 0.04), textcoords="axes fraction",
    )
    ax.annotate(
        "▲", xy=(x, y), xycoords="axes fraction",
        ha="center", va="center",
        fontsize=size, color=STYLE["font_color"],
    )


def _agregar_escala(ax, gdf):
    """Agrega barra de escala simple."""
    bounds = gdf.total_bounds          # [minx, miny, maxx, maxy]
    ancho  = bounds[2] - bounds[0]
    escala = round(ancho / 5 / 100000) * 100000   # aprox 1/5 del ancho

    x0 = bounds[0] + ancho * 0.05
    y0 = bounds[1] + (bounds[3] - bounds[1]) * 0.03
    x1 = x0 + escala

    ax.plot([x0, x1], [y0, y0], color=STYLE["font_color"], lw=2, zorder=10)
    ax.plot([x0, x0], [y0 - escala * 0.02, y0 + escala * 0.02],
            color=STYLE["font_color"], lw=2, zorder=10)
    ax.plot([x1, x1], [y0 - escala * 0.02, y0 + escala * 0.02],
            color=STYLE["font_color"], lw=2, zorder=10)
    ax.text(
        (x0 + x1) / 2, y0 - escala * 0.06,
        f"{int(escala/1000)} km",
        ha="center", fontsize=7,
        fontfamily=STYLE["font_family"],
        color=STYLE["font_color"],
        zorder=10,
    )


def _agregar_creditos(ax):
    """Agrega fuente y proyección en esquina inferior derecha."""
    ax.text(
        0.99, 0.01,
        "Fuente: IGAC | Proyección: MAGNA-SIRGAS EPSG:9377",
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=6, color="#555555",
        fontfamily=STYLE["font_family"],
    )


# ─────────────────────────────────────────────
# EJECUCIÓN DIRECTA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    crear_mapa(
        titulo="Departamentos de Colombia",
        mostrar_municipios=False,
        mostrar_rios=True,
        mostrar_etiquetas=True,
        usar_basemap=False,      # Cambiar a True si tienes internet
        nombre_salida="colombia_departamentos.png",
    )
