# main.py - Application principale
import streamlit as st
import pandas as pd
from io import BytesIO
from data import get_stakeholder_data, create_excel_template
from visualization import create_main_cartography, create_sphere_detail, create_comparison_chart

def main():
    st.set_page_config(
        page_title="Cartographie Interactive",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1e3a5f;
        padding: 1rem 0;
    }
    .sphere-button {
        margin: 0.2rem;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🗺️ Cartographie Interactive des Parties Prenantes</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar - Options et contrôles
    with st.sidebar:
        st.header("⚙️ Contrôles")
        
        # Bouton Présent/Futur
        period = st.radio(
            "📅 Période d'analyse",
            ["Présent", "Futur"],
            horizontal=True
        )
        
        st.divider()
        
        # Options d'affichage
        st.subheader("🎯 Vue détaillée")
        sphere_selected = st.selectbox(
            "Sélectionner une sphère",
            ["Aucune", "Publique", "Économique", "Sociale", "Professionnelle"]
        )
        
        st.divider()
        
        # Export/Import Excel
        st.subheader("📊 Données")
        
        if st.button("📥 Générer template Excel"):
            template_df = create_excel_template()
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                template_df.to_excel(writer, sheet_name='Parties_Prenantes', index=False)
            
            st.download_button(
                label="💾 Télécharger template",
                data=output.getvalue(),
                file_name="cartographie_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        uploaded_file = st.file_uploader(
            "📤 Charger vos données",
            type=['xlsx', 'xls']
        )
    
    # Données principales
    if uploaded_file:
        try:
            uploaded_df = pd.read_excel(uploaded_file)
            present_df = uploaded_df[uploaded_df['Période'] == 'Présent']
            future_df = uploaded_df[uploaded_df['Période'] == 'Futur']
        except Exception as e:
            st.error(f"Erreur lors du chargement: {e}")
            present_df, future_df = get_stakeholder_data()
    else:
        present_df, future_df = get_stakeholder_data()
    
    # Sélection des données selon la période
    current_df = present_df if period == "Présent" else future_df
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Cartographie principale
        fig_main = create_main_cartography(current_df, period)
        st.plotly_chart(fig_main, use_container_width=True)
        
        # Comparaisons si les deux périodes existent
        if not present_df.empty and not future_df.empty:
            with st.expander("📈 Comparaison Présent/Futur"):
                fig_comp = create_comparison_chart(present_df, future_df)
                st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Vue détaillée d'une sphère
        if sphere_selected != "Aucune":
            st.subheader(f"🔍 Détail - {sphere_selected}")
            fig_detail = create_sphere_detail(sphere_selected, current_df)
            st.plotly_chart(fig_detail, use_container_width=True)
        
        # Métriques rapides
        st.subheader("📊 Métriques")
        
        total_entities = len(current_df)
        avg_influence = current_df['Influence'].mean()
        active_spheres = current_df['Sphere'].nunique()
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total entités", total_entities)
            st.metric("Influence moy.", f"{avg_influence:.1f}")
        with col_m2:
            st.metric("Sphères actives", active_spheres)
            st.metric("Période", period)
        
        # Tableau des données
        with st.expander("📋 Données détaillées"):
            st.dataframe(
                current_df[['Nom', 'Sphere', 'Influence']],
                use_container_width=True,
                hide_index=True
            )
    
    # Instructions d'utilisation
    with st.expander("ℹ️ Instructions d'utilisation"):
        st.markdown("""
        **Fonctionnalités principales :**
        - 🔄 **Présent/Futur** : Basculez entre les deux périodes
        - 🎯 **Vue sphère** : Explorez chaque sphère en détail  
        - 📥 **Template Excel** : Modifiez les données dans Excel
        - 📊 **Métriques** : Suivez les évolutions
        
        **Comment personnaliser :**
        1. Téléchargez le template Excel
        2. Modifiez les données (noms, positions, influence)
        3. Rechargez le fichier via "Charger vos données"
        """)

if __name__ == "__main__":
    main()
