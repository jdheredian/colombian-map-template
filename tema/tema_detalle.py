"""
Tema para mapas a escala de detalle. Sectores, secciones y manzanas.

Autocontenido: copia este archivo a otro proyecto y funciona solo.
Al final del archivo esta el ejemplo de uso completo.
"""
from plotnine import (
    element_blank, element_rect, element_text, theme, theme_void,
)

# ── colores ───────────────────────────────────────────────────
tinta = "#1b1b1b"         # texto principal
tinta_suave = "#6b6b6b"   # subtitulo y notas
papel = "#ffffff"         # fondo de la figura
mar = "#dceaf2"           # fondo del panel: el azul queda para el agua
vecino = "#ffffff"        # relleno de los paises colindantes
vecino_borde = "#b9b9b9"  # borde de los colindantes
borde = "#ffffff"         # linea entre poligonos de Colombia
sin_dato = "#e8e8e8"

fuente = "Helvetica Neue"   # cambiar por una instalada si no existe
grosor = 0.40              # ancho de linea para esta escala

# ── paletas ───────────────────────────────────────────────────
# Rampas ColorBrewer de 9 pasos. Para 5 clases: paletas["azules"][::2]
paletas = {
    "azules":  ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6",
                "#4292c6", "#2171b5", "#08519c", "#08306b"],
    "verdes":  ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476",
                "#41ab5d", "#238b45", "#006d2c", "#00441b"],
    "calidos": ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c",
                "#fc4e2a", "#e31a1c", "#bd0026", "#800026"],
    "morados": ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8",
                "#807dba", "#6a51a3", "#54278f", "#3f007d"],
    "grises":  ["#ffffff", "#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696",
                "#737373", "#525252", "#252525", "#000000"],
    # Divergentes: para variables con un punto medio con significado
    "rojo_azul":  ["#67001f", "#b2182b", "#d6604d", "#f4a582", "#f7f7f7",
                   "#92c5de", "#4393c3", "#2166ac", "#053061"],
    "cafe_verde": ["#543005", "#8c510a", "#bf812d", "#dfc27d", "#f5f5f5",
                   "#80cdc1", "#35978f", "#01665e", "#003c30"],
}

# ── tema ──────────────────────────────────────────────────────
base = 10

tema_detalle = theme_void(base_size=base, base_family=fuente) + theme(
    text=element_text(family=fuente, color=tinta),

    # theme_void deja de apagar los ejes en cuanto se define text=,
    # porque axis_text lo hereda. Hay que apagarlos uno por uno.
    axis_text=element_blank(),
    axis_title=element_blank(),
    axis_ticks=element_blank(),
    axis_ticks_length=0,
    panel_grid=element_blank(),

    plot_background=element_rect(fill=papel, color=papel),
    panel_background=element_rect(fill=mar, color=None),

    plot_title=element_text(size=base * 1.45, weight="bold", ha="left",
                            margin={"b": 3, "units": "pt"}),
    plot_subtitle=element_text(size=base, color=tinta_suave, ha="left",
                               margin={"b": 10, "units": "pt"}),
    plot_caption=element_text(size=base * 0.72, color=tinta_suave,
                              ha="right", margin={"t": 10, "units": "pt"}),

    legend_title=element_text(size=base * 0.86, weight="bold", ha="left"),
    legend_text=element_text(size=base * 0.82),
    legend_key_size=base * 1.18,
    legend_background=element_blank(),

    plot_margin=0.015,
    figure_size=(8, 6),
    dpi=300,
)

# ─────────────────────────────────────────────────────────────
# CÓMO SE USA
#
# Necesita: pip install geopandas plotnine mapclassify
#
# import geopandas as gpd
# import mapclassify
# import numpy as np
# import pandas as pd
# from plotnine import *
# from tema_detalle import tema_detalle, paletas, borde, grosor, sin_dato
#
# # Sirve para sector_urbano, seccion_urbana, sector_rural y
# # seccion_rural. Son archivos grandes: filtra el municipio
# # antes de hacer nada mas.
# df_seccion = gpd.read_file("datos/seccion_urbana.geojson").to_crs(9377)
# df_zona = df_seccion.query("mpio_cdpmp == '05001'").copy()
# df_zona = df_zona.merge(df_indicador, on="secu_ccnct")
#
# cortador = mapclassify.NaturalBreaks(df_zona["mi_variable"], k=5)
# cortes = np.concatenate([[df_zona["mi_variable"].min()], cortador.bins])
# etiquetas = [f"{cortes[i]:,.1f} – {cortes[i+1]:,.1f}"
#              .replace(",", "@").replace(".", ",").replace("@", ".")
#              for i in range(5)]
# posicion = np.digitize(df_zona["mi_variable"], cortador.bins[:-1],
#                        right=True)
# df_zona["clase"] = pd.Categorical(
#     [etiquetas[i] for i in posicion], categories=etiquetas, ordered=True)
#
# p = (ggplot(df_zona)
#      + geom_map(aes(fill="clase"), color=borde, size=grosor)
#      + scale_fill_manual(values=paletas["azules"][::2], name="%",
#                          na_value=sin_dato)
#      + coord_fixed(expand=False)
#      + labs(title="Secciones urbanas de Medellín",
#             caption="Fuente: DANE, MGN 2025.")
#      + tema_detalle)
#
# p.save("mapa.png", dpi=300, verbose=False)
