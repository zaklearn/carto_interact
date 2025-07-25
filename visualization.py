# visualization.py - Fonctions de visualisation
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from data import get_sphere_details

def create_main_cartography(df, period="Présent"):
    """Crée la cartographie principale 2D avec 4 pôles"""
    
    # Configuration des couleurs par sphère
    color_map = {
        'Central': '#FFFFFF',
        'Publique': '#FF6B6B',
        'Économique': '#4ECDC4', 
        'Sociale': '#45B7D1',
        'Professionnelle': '#96CEB4'
    }
    
    fig = go.Figure()
    
    # Ajouter les axes des 4 pôles
    fig.add_shape(type="line", x0=-10, y0=0, x1=10, y1=0,
                  line=dict(color="lightgray", width=2, dash="dot"))
    fig.add_shape(type="line", x0=0, y0=-10, x1=0, y1=10,
                  line=dict(color="lightgray", width=2, dash="dot"))
    
    # Labels des 4 pôles
    fig.add_annotation(x=0, y=9.5, text="SPHÈRE PUBLIQUE", 
                      font=dict(size=14, color="white", family="Arial Black"),
                      showarrow=False)
    fig.add_annotation(x=9.5, y=0, text="SPHÈRE<br>ÉCONOMIQUE", 
                      font=dict(size=14, color="white", family="Arial Black"),
                      showarrow=False)
    fig.add_annotation(x=0, y=-9.5, text="SPHÈRE PROFESSIONNELLE", 
                      font=dict(size=14, color="white", family="Arial Black"),
                      showarrow=False)
    fig.add_annotation(x=-9.5, y=0, text="SPHÈRE<br>SOCIALE", 
                      font=dict(size=14, color="white", family="Arial Black"),
                      showarrow=False)
    
    # Ajouter les parties prenantes
    for sphere in df['Sphere'].unique():
        sphere_data = df[df['Sphere'] == sphere]
        
        fig.add_trace(go.Scatter(
            x=sphere_data['X_Position'],
            y=sphere_data['Y_Position'],
            mode='markers+text',
            marker=dict(
                size=sphere_data['Taille'],
                color=color_map.get(sphere, '#999999'),
                line=dict(color='black' if sphere != 'Central' else 'navy', width=2),
                opacity=0.9
            ),
            text=sphere_data['Nom'],
            textposition='middle center',
            textfont=dict(
                size=8 if sphere != 'Central' else 12, 
                color='black' if sphere != 'Central' else 'navy',
                family="Arial"
            ),
            name=f'{sphere}',
            hovertemplate='<b>%{text}</b><br>' +
                         f'Sphère: {sphere}<br>' +
                         'Influence: %{marker.size}<br>' +
                         f'Période: {period}' +
                         '<extra></extra>'
        ))
    
    # Configuration du layout
    fig.update_layout(
        title={
            'text': f'Cartographie des Parties Prenantes - {period}',
            'x': 0.5,
            'font': {'size': 18, 'color': 'white'}
        },
        showlegend=True,
        legend=dict(
            yanchor="top", y=0.99, xanchor="left", x=0.01,
            bgcolor="rgba(255,255,255,0.8)", font=dict(size=10)
        ),
        plot_bgcolor='#1e3a5f',
        paper_bgcolor='#1e3a5f',
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-11, 11]
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-11, 11]
        ),
        width=800,
        height=600
    )
    
    return fig

def create_sphere_detail(sphere_name, df):
    """Crée une vue détaillée d'une sphère spécifique"""
    sphere_details = get_sphere_details()
    sphere_info = sphere_details.get(sphere_name, {})
    
    # Filtrer les données pour cette sphère
    sphere_data = df[df['Sphere'] == sphere_name]
    
    if sphere_data.empty:
        return go.Figure().add_annotation(
            text=f"Aucune donnée pour {sphere_name}",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=16)
        )
    
    # Créer un layout circulaire pour cette sphère
    n_entities = len(sphere_data)
    angles = np.linspace(0, 2*np.pi, n_entities, endpoint=False)
    radius = 3
    
    x_pos = radius * np.cos(angles)
    y_pos = radius * np.sin(angles)
    
    fig = go.Figure()
    
    # Cercle de la sphère
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    
    fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        line=dict(color=sphere_info.get('color', '#999999'), width=3),
        showlegend=False, hoverinfo='skip'
    ))
    
    # Entités de la sphère
    fig.add_trace(go.Scatter(
        x=x_pos,
        y=y_pos,
        mode='markers+text',
        marker=dict(
            size=sphere_data['Taille'].values,
            color=sphere_info.get('color', '#999999'),
            line=dict(color='white', width=2),
            opacity=0.8
        ),
        text=sphere_data['Nom'].values,
        textposition='middle center',
        textfont=dict(size=10, color='white'),
        name=sphere_name,
        hovertemplate='<b>%{text}</b><br>' +
                     f'Sphère: {sphere_name}<br>' +
                     'Influence: %{marker.size}<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': f'Détail - {sphere_name}',
            'x': 0.5,
            'font': {'size': 16, 'color': 'white'}
        },
        annotations=[
            dict(
                text=sphere_info.get('description', ''),
                xref="paper", yref="paper",
                x=0.5, y=0.1,
                showarrow=False,
                font=dict(size=12, color='white')
            )
        ],
        showlegend=False,
        plot_bgcolor='#2c3e50',
        paper_bgcolor='#2c3e50',
        xaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-5, 5]
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showticklabels=False,
            range=[-5, 5]
        ),
        width=400,
        height=400
    )
    
    return fig

def create_comparison_chart(present_df, future_df):
    """Crée un graphique de comparaison présent/futur"""
    
    # Calculer les métriques par sphère
    present_metrics = present_df.groupby('Sphere')['Influence'].agg(['count', 'mean']).reset_index()
    future_metrics = future_df.groupby('Sphere')['Influence'].agg(['count', 'mean']).reset_index()
    
    present_metrics['Période'] = 'Présent'
    future_metrics['Période'] = 'Futur'
    
    comparison_df = pd.concat([present_metrics, future_metrics])
    
    fig = go.Figure()
    
    # Graphique en barres groupées
    for period in ['Présent', 'Futur']:
        period_data = comparison_df[comparison_df['Période'] == period]
        fig.add_trace(go.Bar(
            name=period,
            x=period_data['Sphere'],
            y=period_data['mean'],
            text=period_data['count'],
            texttemplate='Nb: %{text}',
            textposition='outside'
        ))
    
    fig.update_layout(
        title='Évolution de l\'influence par sphère',
        xaxis_title='Sphères',
        yaxis_title='Influence moyenne',
        barmode='group',
        plot_bgcolor='white'
    )
    
    return fig