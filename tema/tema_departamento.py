"""
Tema para mapas a escala de departamento. Un departamento.

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
grosor = 0.15              # ancho de linea para esta escala

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
base = 11

tema_departamento = theme_void(base_size=base, base_family=fuente) + theme(
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
    figure_size=(8, 7.5),
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
# from tema_departamento import (tema_departamento, paletas, borde,
#                                grosor, vecino, vecino_borde)
#
# # EPSG:9377 es la proyeccion oficial de Colombia.
# df_mpio = gpd.read_file("datos/municipio.geojson").to_crs(9377)
# df_mpio = df_mpio.merge(df_indicador, left_on="mpio_cdpmp",
#                         right_on="codigo_dane")
# df_vecinos = gpd.read_file("datos/vecinos.geojson").to_crs(9377)
#
# # 05 = Antioquia. Los codigos de departamento son de 2 digitos.
# df_dpto = df_mpio.query("dpto_ccdgo == '05'").copy()
#
# cortador = mapclassify.Quantiles(df_dpto["mi_variable"], k=5)
# cortes = np.concatenate([[df_dpto["mi_variable"].min()], cortador.bins])
# etiquetas = [f"{cortes[i]:,.1f} – {cortes[i+1]:,.1f}"
#              .replace(",", "@").replace(".", ",").replace("@", ".")
#              for i in range(5)]
# posicion = np.digitize(df_dpto["mi_variable"], cortador.bins[:-1],
#                        right=True)
# df_dpto["clase"] = pd.Categorical(
#     [etiquetas[i] for i in posicion], categories=etiquetas, ordered=True)
#
# # Los vecinos de fondo dan contexto en departamentos de frontera.
# limites = df_dpto.total_bounds
# p = (ggplot()
#      + geom_map(df_vecinos, fill=vecino, color=vecino_borde, size=0.3)
#      + geom_map(df_dpto, aes(fill="clase"), color=borde, size=grosor)
#      + scale_fill_manual(values=paletas["verdes"][::2], name="%")
#      + coord_fixed(xlim=(limites[0], limites[2]),
#                    ylim=(limites[1], limites[3]), expand=False)
#      + labs(title="Antioquia", subtitle="Municipios, 2024",
#             caption="Fuente: DANE, MGN 2025.")
#      + tema_departamento)
#
# p.save("mapa.png", dpi=300, verbose=False)
