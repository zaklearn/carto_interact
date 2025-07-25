# data.py - Données des parties prenantes
import pandas as pd

def get_stakeholder_data():
    """Données actuelles des parties prenantes"""
    present_data = {
        'Nom': [
            'Lagardère', 'Réseaux sociaux', 'Société civile', 'Pouvoirs publics', 
            'Public', 'Organisations professionnelles', 'Investisseurs',
            'Actionnaires', 'Éditeurs', 'Télédiffuseurs', 'Partenaires sociaux', 'Auteurs'
        ],
        'Sphere': [
            'Central', 'Publique', 'Publique', 'Publique', 'Publique', 
            'Économique', 'Économique', 'Professionnelle', 'Économique', 
            'Économique', 'Sociale', 'Sociale'
        ],
        'X_Position': [0, -6, -4, 0, 6, 8, 6, 0, 8, 4, -8, -6],
        'Y_Position': [0, 6, 8, 8, 6, 2, -2, -6, 0, -4, -2, -6],
        'Influence': [10, 7, 6, 9, 6, 7, 8, 9, 6, 7, 6, 5],
        'Taille': [30, 20, 18, 25, 18, 20, 22, 25, 18, 20, 18, 16]
    }
    
    future_data = {
        'Nom': [
            'Lagardère', 'Réseaux sociaux', 'IA & Digital', 'Pouvoirs publics', 
            'Communautés en ligne', 'Organisations ESG', 'Investisseurs durables',
            'Actionnaires activistes', 'Plateformes numériques', 'Créateurs de contenu', 
            'Syndicats 2.0', 'Influenceurs'
        ],
        'Sphere': [
            'Central', 'Publique', 'Publique', 'Publique', 'Publique',
            'Économique', 'Économique', 'Professionnelle', 'Économique',
            'Économique', 'Sociale', 'Sociale'
        ],
        'X_Position': [0, -7, -2, 0, 7, 9, 5, 0, 9, 3, -9, -5],
        'Y_Position': [0, 7, 9, 8, 5, 1, -3, -7, -1, -5, -1, -7],
        'Influence': [10, 9, 8, 8, 7, 8, 9, 8, 9, 6, 5, 7],
        'Taille': [30, 25, 22, 24, 20, 22, 25, 24, 25, 18, 16, 20]
    }
    
    return pd.DataFrame(present_data), pd.DataFrame(future_data)

def get_sphere_details():
    """Détails par sphère pour vue approfondie"""
    sphere_data = {
        'Publique': {
            'entities': ['Réseaux sociaux', 'Société civile', 'Pouvoirs publics', 'Public'],
            'description': 'Sphère de l\'opinion et régulation publique',
            'color': '#FF6B6B'
        },
        'Économique': {
            'entities': ['Organisations professionnelles', 'Investisseurs', 'Éditeurs', 'Télédiffuseurs'],
            'description': 'Acteurs économiques et financiers',
            'color': '#4ECDC4'
        },
        'Sociale': {
            'entities': ['Partenaires sociaux', 'Auteurs', 'Collaborateurs'],
            'description': 'Relations humaines et sociales',
            'color': '#45B7D1'
        },
        'Professionnelle': {
            'entities': ['Actionnaires', 'Conseil de surveillance', 'Direction'],
            'description': 'Gouvernance et management',
            'color': '#96CEB4'
        }
    }
    return sphere_data

def create_excel_template():
    """Crée un template Excel pour modification"""
    present_df, future_df = get_stakeholder_data()
    
    # Ajouter une colonne période
    present_df['Période'] = 'Présent'
    future_df['Période'] = 'Futur'
    
    # Combiner les données
    combined_df = pd.concat([present_df, future_df], ignore_index=True)
    
    return combined_df
