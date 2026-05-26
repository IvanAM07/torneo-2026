# PROY-2: Script de análisis estadístico - Escenario D
# Autor: P2 - Desarrollador Técnico (Paco)
# Descripción: Procesa los resultados del torneo y genera estadísticas básicas + gráficos.

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------
# 1. CARGA DE DATOS
# Usamos rutas relativas para garantizar reproducibilidad en Google Colab
# -------------------------------------------------------
datos_path = "../datos/resultados_torneo.csv"
resultados_path = "../resultados/"

# Crear carpeta de resultados si no existe
os.makedirs(resultados_path, exist_ok=True)

df = pd.read_csv(datos_path)
print("Dataset cargado correctamente.")
print(f"Total de partidos: {len(df)}\n")

# -------------------------------------------------------
# 2. CÁLCULO DE ESTADÍSTICAS POR EQUIPO
# Para cada partido calculamos puntos: victoria=3, empate=1, derrota=0
# -------------------------------------------------------
equipos = pd.unique(df[["equipo_local", "equipo_visitante"]].values.ravel())

estadisticas = []

for equipo in equipos:
    # Partidos como local
    local = df[df["equipo_local"] == equipo].copy()
    # Partidos como visitante
    visitante = df[df["equipo_visitante"] == equipo].copy()

    # Victorias, empates y derrotas como local
    victorias_local = len(local[local["goles_local"] > local["goles_visitante"]])
    empates_local = len(local[local["goles_local"] == local["goles_visitante"]])
    derrotas_local = len(local[local["goles_local"] < local["goles_visitante"]])

    # Victorias, empates y derrotas como visitante
    victorias_visita = len(visitante[visitante["goles_visitante"] > visitante["goles_local"]])
    empates_visita = len(visitante[visitante["goles_visitante"] == visitante["goles_local"]])
    derrotas_visita = len(visitante[visitante["goles_visitante"] < visitante["goles_local"]])

    # Totales
    victorias = victorias_local + victorias_visita
    empates = empates_local + empates_visita
    derrotas = derrotas_local + derrotas_visita
    puntos = victorias * 3 + empates * 1

    # Goles a favor y en contra
    goles_favor = local["goles_local"].sum() + visitante["goles_visitante"].sum()
    goles_contra = local["goles_visitante"].sum() + visitante["goles_local"].sum()
    diferencia_goles = goles_favor - goles_contra

    partidos_jugados = victorias + empates + derrotas

    estadisticas.append({
        "Equipo": equipo,
        "PJ": partidos_jugados,
        "V": victorias,
        "E": empates,
        "D": derrotas,
        "GF": int(goles_favor),
        "GC": int(goles_contra),
        "DG": int(diferencia_goles),
        "Pts": puntos
    })

# Crear DataFrame de tabla de posiciones y ordenar por puntos y diferencia de goles
tabla = pd.DataFrame(estadisticas).sort_values(
    by=["Pts", "DG", "GF"], ascending=False
).reset_index(drop=True)
tabla.index += 1  # Posición comienza en 1

print("=== TABLA DE POSICIONES ===")
print(tabla.to_string())
print()

# -------------------------------------------------------
# 3. PROMEDIO DE GOLES POR PARTIDO
# -------------------------------------------------------
total_goles = df["goles_local"].sum() + df["goles_visitante"].sum()
promedio_goles = total_goles / len(df)
print(f"Total de goles en el torneo: {total_goles}")
print(f"Promedio de goles por partido: {promedio_goles:.2f}\n")

# -------------------------------------------------------
# 4. GRÁFICO 1: Tabla de posiciones (puntos por equipo)
# Visualiza de forma clara el rendimiento relativo de cada equipo
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
colores = ["#1a6b3c", "#2e8b57", "#3cb371", "#66cdaa", "#b2dfdb"]
bars = ax.barh(tabla["Equipo"], tabla["Pts"], color=colores[:len(tabla)])
ax.set_xlabel("Puntos")
ax.set_title("Tabla de Posiciones - Torneo 2026", fontsize=13, fontweight="bold")
ax.invert_yaxis()  # El líder queda arriba
for bar, val in zip(bars, tabla["Pts"]):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=10)
plt.tight_layout()
plt.savefig(resultados_path + "tabla_posiciones.png", dpi=150)
plt.close()
print("Gráfico 'tabla_posiciones.png' guardado en /resultados.")

# -------------------------------------------------------
# 5. GRÁFICO 2: Comparativo de rendimiento (V/E/D apilados)
# Permite ver la distribución de resultados de cada equipo
# -------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
x = range(len(tabla))
ax.bar(tabla["Equipo"], tabla["V"], label="Victorias", color="#1a6b3c")
ax.bar(tabla["Equipo"], tabla["E"], bottom=tabla["V"], label="Empates", color="#f0ad4e")
ax.bar(tabla["Equipo"], tabla["D"], bottom=tabla["V"] + tabla["E"], label="Derrotas", color="#c0392b")
ax.set_ylabel("Partidos")
ax.set_title("Rendimiento por Equipo - Victorias, Empates y Derrotas", fontsize=12, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(resultados_path + "rendimiento_equipos.png", dpi=150)
plt.close()
print("Gráfico 'rendimiento_equipos.png' guardado en /resultados.")

# -------------------------------------------------------
# 6. EXPORTAR TABLA DE POSICIONES A CSV
# -------------------------------------------------------
tabla.to_csv(resultados_path + "tabla_posiciones.csv", index_label="Posicion")
print("Tabla exportada como 'tabla_posiciones.csv' en /resultados.")
