import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsbombpy import sb

# Función para abreviar nombres de jugadores
def abreviar_nombre(nombre):
    if pd.isna(nombre):
        return "Desconocido"
    partes = nombre.split()
    if len(partes) > 1:
        return f"{partes[-1]}, {partes[0][0]}."
    return nombre

# Página de análisis de jugadores
def main():
    st.title("Análisis Avanzado de Jugadores")

    # Cargar datos de partidos
    try:
        C_Am = sb.matches(competition_id=223, season_id=282)
        matches_df = C_Am[["home_team", "away_team", "match_id"]].copy()
        matches_df["Plays"] = matches_df["home_team"] + " vs " + matches_df["away_team"]
    except Exception as e:
        st.error(f"No se pudieron cargar los datos de partidos: {e}")
        return

    # Selección de partido
    selected_play = st.sidebar.selectbox("Selecciona un partido:", matches_df["Plays"])
    match_id = matches_df[matches_df["Plays"] == selected_play]["match_id"].values[0]
    home_team = matches_df[matches_df["match_id"] == match_id]["home_team"].values[0]
    away_team = matches_df[matches_df["match_id"] == match_id]["away_team"].values[0]

    # Cargar eventos del partido seleccionado
    try:
        events = sb.events(match_id=match_id)
    except Exception as e:
        st.error(f"No se pudieron cargar los eventos del partido: {e}")
        return

    # Filtrar eventos relevantes
    tipos_incluidos = ["Pass", "Shot", "Carry", "Duel", "Ball Recovery"]
    filtered_events = events[events["type"].isin(tipos_incluidos)].copy()

    # Clasificar jugadores por equipo
    filtered_events["team_type"] = filtered_events["team"].apply(
        lambda x: "Local" if x == home_team else "Visitante"
    )

    # Agrupar datos por jugador, tipo de acción y equipo
    grouped_events = (
        filtered_events.groupby(["player", "type", "team_type"])
        .size()
        .reset_index(name="count")
    )
    grouped_events["player_abbr"] = grouped_events["player"].apply(abreviar_nombre)

    # Mostrar estadísticas generales
    st.subheader("Distribución de Acciones por Tipo")
    if not grouped_events.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        grouped_events.groupby("type")["count"].sum().plot(kind="bar", ax=ax, color="#1f77b4")
        ax.set_title("Distribución de Acciones por Tipo")
        ax.set_xlabel("Tipo de Acción")
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)

    # Tabla de acciones por jugadores
    st.subheader("Tabla Comparativa de Jugadores")
    player_table = grouped_events.pivot_table(
        index=["player_abbr", "team_type"],
        columns="type",
        values="count",
        fill_value=0,
    ).astype(int)
    st.dataframe(player_table)

    # Selección de jugadores para comparación
    jugadores = grouped_events["player_abbr"].unique()
    jugador_1 = st.sidebar.selectbox("Selecciona el Jugador 1:", jugadores)
    jugador_2 = st.sidebar.selectbox("Selecciona el Jugador 2:", jugadores)

    # Función para crear gráficos comparativos
    def crear_grafico_comparativo(jugador_1, jugador_2, tipo_accion):
        datos_1 = grouped_events[(grouped_events["player_abbr"] == jugador_1) & (grouped_events["type"] == tipo_accion)]
        datos_2 = grouped_events[(grouped_events["player_abbr"] == jugador_2) & (grouped_events["type"] == tipo_accion)]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(
            [jugador_1, jugador_2],
            [datos_1["count"].sum() if not datos_1.empty else 0,
             datos_2["count"].sum() if not datos_2.empty else 0],
            color=["#1f77b4", "#ff7f0e"],
        )
        ax.set_title(f"Comparación: {tipo_accion}")
        ax.set_xlabel("Jugador")
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)

    # Gráficos comparativos por tipo de acción
    st.subheader("Comparación de Acciones entre Jugadores")
    for tipo_accion in tipos_incluidos:
        crear_grafico_comparativo(jugador_1, jugador_2, tipo_accion)

if __name__ == "__main__":
    main()
