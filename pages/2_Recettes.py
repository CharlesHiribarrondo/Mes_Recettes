# Import packages
import streamlit as st
import pandas as pd
import numpy as np

# Import data
df_recettes = pd.read_csv('data/Data_Recettes_Cuisine_Recettes.csv', index_col=None)
df_ingredients = pd.read_csv('data/Data_Recettes_Cuisine_Ingredients.csv', index_col=None)

#st.write("Jeu de données des recettes :", df_recettes)
#st.write("Jeu de données des ingrédients :", df_ingredients)

# Sélection des recettes
st.header("Sélection de vos recettes :male-cook: :")
choix_recettes = st.multiselect(
    'Sélectionner vos recettes :',
    df_recettes['Nom_recette']  # On affiche les noms des recettes pour le choix
)

# Slider pour choisir le nombre de personnes
nombre_personnes = st.slider("Nombre de personnes par recette : ", min_value=1, max_value=16, value=4)

# Calcul du coefficient
coefficient = nombre_personnes / 4

# Filtrer le DataFrame pour récupérer les lignes correspondantes aux recettes sélectionnées
if choix_recettes:
    # Filtrer le DataFrame des recettes en fonction des choix de l'utilisateur
    df_selectionnees = df_recettes[df_recettes['Nom_recette'].isin(choix_recettes)]

    # Afficher les recettes sélectionnées
    #st.write("Recettes sélectionnées :", df_selectionnees)

    # Récupérer les "n°" des recettes sélectionnées
    numeros_selectionnes = df_selectionnees['Numero']

    # Filtrer le DataFrame des ingrédients en fonction des "n°" des recettes sélectionnées
    ingredients_selectionnes = df_ingredients[df_ingredients['Numero'].isin(numeros_selectionnes)]
    #st.write(ingredients_selectionnes[['Nom_recette',"Ingredient",'Quantite','Unite','Rayon_magasin']])

    # Regrouper les ingrédients identiques par "Ingrédient", "Unité" et "Rayon_magasin" et sommer les quantités
    ingredients_groupes = ingredients_selectionnes.groupby(['Ingredient', 'Unite', 'Rayon_magasin'], as_index=False).agg({
        'Quantite': 'sum'
    })

    # Ajuster les quantités en fonction du coefficient
    #ingredients_groupes['Quantité'] = (ingredients_groupes['Quantité'] * coefficient).round()  # Arrondir les quantités
    ingredients_groupes['Quantite'] = np.ceil(ingredients_groupes['Quantite'] * coefficient).astype(int)

    # Afficher les ingrédients correspondants
    st.write("Ingrédients des recettes sélectionnées :", ingredients_groupes[['Ingredient', 'Quantite', 'Unite', 'Rayon_magasin']])

    # Grouper les ingrédients par rayon
    ingredients_par_rayon = ingredients_groupes.groupby('Rayon_magasin')
    #st.write(ingredients_par_rayon)

# Résultat : Liste de courses
    st.header("	:tada: Votre Liste de courses :clipboard: :tada::")

    # Afficher chaque rayon et ses ingrédients sous forme de checkboxes
    for rayon, ingredients_rayon in ingredients_par_rayon:  # Correctement renommer pour éviter la confusion
        st.subheader(f"Rayon : {rayon}")

        # Pour chaque ingrédient dans ce rayon
        for index, row in ingredients_rayon.iterrows():
            # Créer la chaîne de texte avec l'ingrédient, quantité et unité
            # Supprimer les décimales inutiles dans l'unité
            quantity_str = f"{int(row['Quantite'])} {row['Unite']}".replace('.0 ', ' ')
            ingredient_info = f"{row['Ingredient']} : {quantity_str}"

            # Afficher dans une case à cocher
            st.checkbox(f"  {ingredient_info}", key=f"{rayon}_{index}")

else:
    st.write("Aucune recette sélectionnée.")
