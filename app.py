"""
Application Dash — Tableau de bord Décisionnel : Ateliers de Couture (Sénégal)
Projet 06 — Pilotage des Délais de Confection & Analyse des Retards

Consignes d'exécution :
1. Assurez-vous que les dépendances sont installées :
   pip install dash plotly pandas
2. Lancez l'application dans votre terminal depuis le dossier du projet :
   python app.py
3. Ouvrez votre navigateur web à l'adresse suivante :
   http://127.0.0.1:8050/
"""

from pathlib import Path
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Chemins des données nettoyées
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DATA_PATH = BASE_DIR / "resultats" / "operations_nettoyees.csv"
REF_SITES_PATH = BASE_DIR / "donnees" / "referentiel_sites.csv"

# Chargement des données
df_ops = pd.read_csv(CLEAN_DATA_PATH)
df_ref = pd.read_csv(REF_SITES_PATH, sep=";")

# Fusion avec le référentiel des sites
df_full = df_ops.merge(df_ref, on="id_site", how="left")

# Filtrage du périmètre d'analyse métier valide
# Statut = Valide, site autorisé, mesures exploitables et catégories documentées
df_valide = df_full[
    (df_full["statut"] == "Valide")
    & (df_full["id_site"].isin(df_ref["id_site"]))
    & (df_full["categorie"].isin(["Boubou", "Chemise", "Robe", "Uniforme"]))
    & (df_full["delai_promis_jours"].notna())
    & (df_full["delai_reel_jours"].notna())
].copy()

# Métriques centrales : écart de confection (réel - promis) et indicateur binaire de retard
df_valide["ecart_retard_jours"] = df_valide["delai_reel_jours"] - df_valide["delai_promis_jours"]
df_valide["en_retard"] = (df_valide["ecart_retard_jours"] > 0).astype(int)

# Traitement des dates pour le filtrage
df_valide["date_dt"] = pd.to_datetime(df_valide["date_operation"], errors="coerce")
min_date = df_valide["date_dt"].dropna().min()
max_date = df_valide["date_dt"].dropna().max()

# Initialisation de l'application Dash
app = dash.Dash(
    __name__,
    title="Ateliers de Couture — Pilotage des Délais",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Palette de couleurs "Haute Couture & Atelier"
COLOR_PRIMARY = "#0f2b48"     # Bleu nuit profond
COLOR_ACCENT = "#c29352"      # Or couture
COLOR_SUCCESS = "#2a9d8f"     # Émeraude / Ponctualité
COLOR_WARNING = "#e76f51"     # Corail vif / Retard
COLOR_CARD = "#ffffff"
COLOR_BG = "#f4f7f9"
COLOR_TEXT = "#1c2833"

# Options pour les menus déroulants
site_options = [
    {"label": f"{r.nom_site} ({r.ville})", "value": r.id_site}
    for _, r in df_ref.iterrows()
]
cat_options = [
    {"label": cat, "value": cat}
    for cat in sorted(df_valide["categorie"].unique())
]

# Structure HTML & composants (Vanilla CSS moderne)
app.layout = html.Div(
    style={
        "backgroundColor": COLOR_BG,
        "fontFamily": "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif",
        "color": COLOR_TEXT,
        "minHeight": "100vh",
        "padding": "24px 32px",
    },
    children=[
        # En-tête (Header)
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "backgroundColor": COLOR_PRIMARY,
                "color": "#ffffff",
                "padding": "20px 30px",
                "borderRadius": "12px",
                "marginBottom": "24px",
                "boxShadow": "0 8px 24px rgba(15, 43, 72, 0.15)",
            },
            children=[
                html.Div([
                    html.H1(
                        "Ateliers de Couture — Observatoire des Délais de Confection",
                        style={"fontSize": "24px", "fontWeight": "700", "margin": "0 0 6px 0", "letterSpacing": "-0.5px"},
                    ),
                    html.P(
                        "Outil décisionnel d'audit et de pilotage des engagements clients (Données consolidées 2025)",
                        style={"fontSize": "14px", "opacity": "0.85", "margin": 0},
                    ),
                ]),
                html.Div(
                    style={"textAlign": "right"},
                    children=[
                        html.Span(
                            "Projet 06 • Direction des Opérations",
                            style={"fontSize": "12px", "fontWeight": "600", "backgroundColor": "rgba(255,255,255,0.15)", "padding": "6px 12px", "borderRadius": "20px"},
                        ),
                    ]
                )
            ],
        ),

        # Panneau des Filtres
        html.Div(
            style={
                "backgroundColor": COLOR_CARD,
                "padding": "20px 24px",
                "borderRadius": "12px",
                "marginBottom": "24px",
                "boxShadow": "0 2px 12px rgba(0,0,0,0.05)",
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(260px, 1fr))",
                "gap": "20px",
                "alignItems": "center",
            },
            children=[
                # Filtre Dates
                html.Div([
                    html.Label("Période d'opération :", style={"fontWeight": "600", "fontSize": "13px", "marginBottom": "6px", "display": "block", "color": COLOR_PRIMARY}),
                    dcc.DatePickerRange(
                        id="date-filter",
                        start_date=min_date.date() if pd.notna(min_date) else None,
                        end_date=max_date.date() if pd.notna(max_date) else None,
                        min_date_allowed=min_date.date() if pd.notna(min_date) else None,
                        max_date_allowed=max_date.date() if pd.notna(max_date) else None,
                        display_format="DD/MM/YYYY",
                        style={"width": "100%", "borderRadius": "6px"},
                    ),
                ]),
                # Filtre Sites
                html.Div([
                    html.Label("Sites de confection :", style={"fontWeight": "600", "fontSize": "13px", "marginBottom": "6px", "display": "block", "color": COLOR_PRIMARY}),
                    dcc.Dropdown(
                        id="site-filter",
                        options=site_options,
                        value=[opt["value"] for opt in site_options],
                        multi=True,
                        placeholder="Sélectionnez les sites...",
                        style={"borderRadius": "6px"},
                    ),
                ]),
                # Filtre Catégories
                html.Div([
                    html.Label("Types de vêtements :", style={"fontWeight": "600", "fontSize": "13px", "marginBottom": "6px", "display": "block", "color": COLOR_PRIMARY}),
                    dcc.Dropdown(
                        id="category-filter",
                        options=cat_options,
                        value=[opt["value"] for opt in cat_options],
                        multi=True,
                        placeholder="Sélectionnez les vêtements...",
                        style={"borderRadius": "6px"},
                    ),
                ]),
            ],
        ),

        # Cartes Indicateurs Clés (KPI Cards)
        html.Div(
            id="kpi-container",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
                "gap": "18px",
                "marginBottom": "24px",
            },
        ),

        # Zone d'alerte si aucune donnée
        html.Div(id="alert-container"),

        # Graphiques interactifs (Grille 2x2)
        html.Div(
            id="charts-container",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(480px, 1fr))",
                "gap": "20px",
            },
            children=[
                html.Div(
                    style={"backgroundColor": COLOR_CARD, "padding": "16px", "borderRadius": "12px", "boxShadow": "0 2px 12px rgba(0,0,0,0.05)"},
                    children=[dcc.Graph(id="chart-category", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": COLOR_CARD, "padding": "16px", "borderRadius": "12px", "boxShadow": "0 2px 12px rgba(0,0,0,0.05)"},
                    children=[dcc.Graph(id="chart-monthly", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": COLOR_CARD, "padding": "16px", "borderRadius": "12px", "boxShadow": "0 2px 12px rgba(0,0,0,0.05)"},
                    children=[dcc.Graph(id="chart-sites", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": COLOR_CARD, "padding": "16px", "borderRadius": "12px", "boxShadow": "0 2px 12px rgba(0,0,0,0.05)"},
                    children=[dcc.Graph(id="chart-scatter", config={"displayModeBar": False})],
                ),
            ],
        ),

        # Pied de page (Footer)
        html.Div(
            style={
                "marginTop": "36px",
                "paddingTop": "16px",
                "borderTop": "1px solid #dce4ec",
                "display": "flex",
                "justifyContent": "space-between",
                "fontSize": "13px",
                "color": "#7f8c8d",
            },
            children=[
                html.Span("Ateliers de couture — Registre 2025 synthétique • Source prioritaire JSON nettoyée"),
                html.Span("Métrique centrale : delai_reel_jours − delai_promis_jours"),
            ],
        ),
    ],
)


# Callback réactif pour filtrer les données et mettre à jour l'ensemble du tableau de bord
@app.callback(
    [
        Output("kpi-container", "children"),
        Output("alert-container", "children"),
        Output("charts-container", "style"),
        Output("chart-category", "figure"),
        Output("chart-monthly", "figure"),
        Output("chart-sites", "figure"),
        Output("chart-scatter", "figure"),
    ],
    [
        Input("date-filter", "start_date"),
        Input("date-filter", "end_date"),
        Input("site-filter", "value"),
        Input("category-filter", "value"),
    ],
)
def update_dashboard(start_date, end_date, selected_sites, selected_cats):
    # Filtrage sécurisé
    filtered = df_valide.copy()

    if selected_sites:
        filtered = filtered[filtered["id_site"].isin(selected_sites)]
    else:
        filtered = filtered.iloc[0:0]

    if selected_cats:
        filtered = filtered[filtered["categorie"].isin(selected_cats)]
    else:
        filtered = filtered.iloc[0:0]

    if start_date:
        s_date = pd.to_datetime(start_date)
        filtered = filtered[filtered["date_dt"].isna() | (filtered["date_dt"] >= s_date)]
    if end_date:
        e_date = pd.to_datetime(end_date)
        filtered = filtered[filtered["date_dt"].isna() | (filtered["date_dt"] <= e_date)]

    total_ops = len(filtered)

    # Gestion de l'absence de données (Division par zéro évitée)
    if total_ops == 0:
        alert = html.Div(
            style={
                "backgroundColor": "#fff3cd",
                "color": "#856404",
                "padding": "18px 24px",
                "borderRadius": "10px",
                "border": "1px solid #ffeeba",
                "marginBottom": "20px",
                "fontWeight": "500",
                "textAlign": "center",
            },
            children="⚠️ Aucune commande de confection ne correspond aux filtres sélectionnés. Veuillez élargir votre sélection.",
        )
        empty_fig = go.Figure()
        empty_fig.update_layout(
            annotations=[{
                "text": "Aucune donnée disponible",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16, "color": "#7f8c8d"}
            }],
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        kpis_empty = [
            build_kpi_card("Commandes analysées", "0", "Effectif sélectionné", "#7f8c8d"),
            build_kpi_card("Taux de dépassement", "N/A", "Commandes en retard", "#7f8c8d"),
            build_kpi_card("Retard médian", "N/A", "Écart réel - promis", "#7f8c8d"),
            build_kpi_card("Retard moyen", "N/A", "Sur commandes exploitables", "#7f8c8d"),
        ]
        return kpis_empty, alert, {"display": "none"}, empty_fig, empty_fig, empty_fig, empty_fig

    # Calculs métriques sur données filtrées
    nb_en_retard = int((filtered["en_retard"] == 1).sum())
    taux_retard = (nb_en_retard / total_ops) * 100 if total_ops > 0 else 0.0
    retard_median = filtered["ecart_retard_jours"].median()
    retard_moyen = filtered["ecart_retard_jours"].mean()

    kpi_cards = [
        build_kpi_card("Commandes analysées", f"{total_ops:,}", "Périmètre valide filtré", COLOR_PRIMARY),
        build_kpi_card("Taux de dépassement", f"{taux_retard:.1f} %", f"{nb_en_retard} commandes en retard", COLOR_WARNING if taux_retard > 65 else COLOR_SUCCESS),
        build_kpi_card("Retard médian", f"{retard_median:+.0f} j", "Médiane delai_reel − promis", COLOR_ACCENT),
        build_kpi_card("Retard moyen", f"{retard_moyen:+.1f} j", "Sensible aux valeurs atypiques", COLOR_PRIMARY),
    ]

    # Graphique 1 : Taux de dépassement par catégorie
    cat_summary = filtered.groupby("categorie").agg(
        total=("id_operation", "count"),
        retard_pct=("en_retard", lambda s: round(s.mean() * 100, 1)),
        retard_med=("ecart_retard_jours", "median"),
    ).reset_index().sort_values(by="retard_pct", ascending=False)

    fig1 = px.bar(
        cat_summary,
        x="categorie",
        y="retard_pct",
        text="retard_pct",
        color="retard_pct",
        color_continuous_scale=["#2a9d8f", "#e76f51"],
        labels={"categorie": "Vêtement", "retard_pct": "Taux de retard (%)"},
        title="<b>1. Dépassement du délai promis par vêtement</b>",
    )
    fig1.update_traces(texttemplate="%{text:.1f} %", textposition="outside")
    fig1.update_layout(
        plot_bgcolor="white",
        yaxis=dict(range=[0, 100], title="Taux de dépassement (%)"),
        xaxis=dict(title=""),
        coloraxis_showscale=False,
        margin=dict(t=50, b=40, l=40, r=20),
    )

    # Graphique 2 : Évolution temporelle (Mois)
    dated_filtered = filtered[filtered["date_dt"].notna()].copy()
    if len(dated_filtered) > 0:
        dated_filtered["mois"] = dated_filtered["date_dt"].dt.strftime("%Y-%m")
        monthly_summary = dated_filtered.groupby("mois").agg(
            promis_med=("delai_promis_jours", "median"),
            reel_med=("delai_reel_jours", "median"),
        ).reset_index().sort_values("mois")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=monthly_summary["mois"], y=monthly_summary["promis_med"],
            mode="lines+markers", name="Délai promis médian",
            line=dict(color=COLOR_SUCCESS, width=2.5),
        ))
        fig2.add_trace(go.Scatter(
            x=monthly_summary["mois"], y=monthly_summary["reel_med"],
            mode="lines+markers", name="Délai réel médian",
            line=dict(color=COLOR_WARNING, width=2.5),
        ))
        fig2.update_layout(
            title="<b>2. Évolution temporelle des délais médians (2025)</b>",
            plot_bgcolor="white",
            xaxis=dict(title="Mois de l'opération"),
            yaxis=dict(title="Jours"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=50, b=40, l=40, r=20),
        )
    else:
        fig2 = go.Figure().add_annotation(text="Dates non renseignées sur cette sélection", showarrow=False)

    # Graphique 3 : Classement des sites par retard médian
    site_summary = filtered.groupby("nom_site").agg(
        retard_med=("ecart_retard_jours", "median"),
        retard_pct=("en_retard", lambda s: round(s.mean() * 100, 1)),
        total=("id_operation", "count"),
    ).reset_index().sort_values(by="retard_med", ascending=True)

    fig3 = px.bar(
        site_summary,
        y="nom_site",
        x="retard_med",
        orientation="h",
        text="retard_med",
        labels={"nom_site": "Atelier", "retard_med": "Retard médian (jours)"},
        title="<b>3. Retard médian par atelier de couture</b>",
        color="retard_med",
        color_continuous_scale="Reds",
    )
    fig3.update_traces(texttemplate="%{text:+.1f} j", textposition="outside")
    fig3.update_layout(
        plot_bgcolor="white",
        xaxis=dict(title="Écart médian (delai_reel − delai_promis) en jours"),
        yaxis=dict(title=""),
        coloraxis_showscale=False,
        margin=dict(t=50, b=40, l=120, r=30),
    )

    # Graphique 4 : Nuage de points Promis vs Réel (plafonné à 60j pour lisibilité)
    sub_visu = filtered[filtered["delai_reel_jours"] <= 60]
    fig4 = px.scatter(
        sub_visu,
        x="delai_promis_jours",
        y="delai_reel_jours",
        color="categorie",
        opacity=0.7,
        labels={"delai_promis_jours": "Délai promis (jours)", "delai_reel_jours": "Délai réel (jours)"},
        title="<b>4. Confrontation Délai Promis vs Réel (Zoom ≤ 60 jours)</b>",
    )
    max_axis = max(sub_visu["delai_promis_jours"].max() if len(sub_visu) > 0 else 30, 45)
    fig4.add_shape(
        type="line", x0=0, y0=0, x1=max_axis, y1=max_axis,
        line=dict(color="#7f8c8d", width=1.5, dash="dash"),
    )
    fig4.add_annotation(
        x=max_axis * 0.7, y=max_axis * 0.75,
        text="Zone de retard (Réel > Promis)",
        showarrow=False,
        font=dict(color=COLOR_WARNING, size=11, family="Segoe UI"),
    )
    fig4.update_layout(
        plot_bgcolor="white",
        margin=dict(t=50, b=40, l=40, r=20),
        legend=dict(title="Catégorie"),
    )

    return (
        kpi_cards,
        html.Div(),
        {"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(480px, 1fr))", "gap": "20px"},
        fig1,
        fig2,
        fig3,
        fig4,
    )


def build_kpi_card(title, value, subtitle, accent_color):
    return html.Div(
        style={
            "backgroundColor": COLOR_CARD,
            "padding": "18px 20px",
            "borderRadius": "12px",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.04)",
            "borderLeft": f"5px solid {accent_color}",
        },
        children=[
            html.Div(title, style={"fontSize": "13px", "fontWeight": "600", "color": "#7f8c8d", "marginBottom": "6px"}),
            html.Div(value, style={"fontSize": "26px", "fontWeight": "700", "color": COLOR_TEXT, "marginBottom": "4px"}),
            html.Div(subtitle, style={"fontSize": "12px", "color": "#95a5a6"}),
        ],
    )


if __name__ == "__main__":
    print("Démarrage du serveur Dash pour les Ateliers de Couture...")
    print("Application accessible sur : http://127.0.0.1:8050/")
    app.run(debug=False, port=8050)
