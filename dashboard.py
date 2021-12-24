from ctypes import string_at
import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import matplotlib.pyplot as plt
import json
import seaborn as sns
import time
import shap
import os

URL_API = 'https://projet-7-backend.herokuapp.com/'

def main():

    # Affichage du titre et du sous-titre
    st.title("Implémenter un modèle de scoring")
    st.markdown("<i>API répondant aux besoins du projet 7 pour le parcours Data Scientist OpenClassRoom</i>", unsafe_allow_html=True)

    # Affichage d'informations dans la sidebar
    st.sidebar.subheader("Informations générales")

# Chargement du logo
    logo = load_logo()
    st.sidebar.image(logo,width=200)

# Chargement de la selectbox
    lst_id = load_selectbox()
    global id_client
    id_client = st.sidebar.selectbox("ID Client", lst_id)

 # Chargement des infos générales
    nb_credits, revenu_moy, credits_moy, targets = load_infos_gen()

    # Affichage des infos dans la sidebar
    # Nombre de crédits existants
    st.sidebar.markdown("<u>Nombre crédits existants dans la base :</u>", unsafe_allow_html=True)
    st.sidebar.text(nb_credits)

    # Graphique camembert
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.sidebar.markdown("<u>Différence solvabilité / non solvabilité</u>", unsafe_allow_html=True)

    plt.pie(targets, explode=[0, 0.1], labels=["Solvable", "Non solvable"], autopct='%1.1f%%',
            shadow=True, startangle=90)
    st.sidebar.pyplot()
    

    # Revenus moyens
    st.sidebar.markdown("<u>Revenus moyens $(USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(revenu_moy)

    # Montant crédits moyen
    st.sidebar.markdown("<u>Montant crédits moyen $(USD) :</u>", unsafe_allow_html=True)
    st.sidebar.text(credits_moy)

     # Affichage de l'ID client sélectionné
    st.write("Vous avez sélectionné le client :", id_client)

    # Affichage état civil
    st.header("**Informations client**")

    if st.checkbox("Afficher les informations du client?"):
        
        infos_client = identite_client()
        st.write("Sex :**", infos_client["CODE_GENDER_M"][0], "**")
        st.markdown("<i>Sex = 0 :  Client Femelle    Sex = 1 :   Client Mâle</i>", unsafe_allow_html=True)
        st.write("Statut famille :**", infos_client['NAME_FAMILY_STATUS_Married'][0], "**")
        st.markdown("<i>Statut famille  = 0 :   Non Marié(e)     Statut famille = 1 :   Marié(e)</i>", unsafe_allow_html=True)
        st.write("Age client :", int(infos_client["DAYS_BIRTH"].values / -365), "ans.")
        st.write("Année emploi :", int(infos_client["DAYS_EMPLOYED"].values / -365), "ans.")

        data_age = load_age_population()
        # Set the style of plots
        plt.style.use('fivethirtyeight')
        fig=plt.figure(figsize=(6, 6))
        # Plot the distribution of ages in years
        h1=plt.hist(data_age, edgecolor = 'k', bins = 25)
        plt.axvline(int(infos_client["DAYS_BIRTH"].values / -365), color="red", linestyle=":")
        plt.title('Age des Clients', size=5)
        plt.xlabel('Age (Années)', size=5)
        plt.ylabel('Fréquence', size=5)
        plt.xticks(size=5)
        plt.yticks(size=5)
        st.pyplot(fig)

        st.subheader("*Revenus*")
        
        st.write("Total revenus client :", infos_client["AMT_INCOME_TOTAL"][0], "$")


        st.write('Starting a long computation...')

        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
        # Update the progress bar with each iteration.
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i + 1)
            time.sleep(0.5)

        st.write('...and now we\'re done!')
        data_revenus = load_revenus_population()
        # Set the style of plots
        plt.style.use('fivethirtyeight')
        fig=plt.figure(figsize=(6,6))
        # Plot the distribution of revenus
        sns.histplot(data_revenus)
        plt.axvline((infos_client["AMT_INCOME_TOTAL"][0]), color="red", linestyle=":")
        plt.title('Revenus des Clients', size=5)
        plt.xlabel('Revenus ($ USD)', size=5)
        plt.ylabel('Fréquence', size=5)
        plt.xlim([1e5, 8e5])
        plt.xticks(size=5)
        plt.yticks(size=5)
        st.pyplot(fig)

        st.write("Montant du crédit :", infos_client["AMT_CREDIT"][0], "$")
        st.write("Annuités crédit :", infos_client["AMT_ANNUITY"][0], "$")
        
    else:
        st.markdown("<i>Informations masquées</i>", unsafe_allow_html=True)



    # Affichage solvabilité client
        st.header("**Analyse dossier client**")
    
        st.markdown("<u>Probabilité de risque de faillite du client :</u>", unsafe_allow_html=True)
        prediction = load_prediction()
        st.write(round(prediction*100, 2), "%")
        st.markdown("<u>Données client :</u>", unsafe_allow_html=True)
        st.write(identite_client()) 

    # Affichage interprétation du modèle   
        st.markdown("<u>Interprétation du modèle - Importance des variables :</u>", unsafe_allow_html=True)
        if st.checkbox("Interpréter le modèle"):
            explained_model=load_model_interpretation()
            infos_client=identite_client()
            number = st.slider("Choisir le numéro des features...", 0, 30, 5)
            features=load_features()
            explained_model=pd.DataFrame(explained_model, columns=features)
            fig=shap.summary_plot(explained_model, np.hstack(infos_client), max_display=number, plot_type ="bar",  color_bar=False, plot_size=(5, 5))
            st.pyplot(fig)
        
        else:
            st.markdown("<i>…</i>", unsafe_allow_html=True)
    # Affichage des dossiers similaires
        chk_voisins = st.checkbox("Afficher dossiers similaires?")

        if chk_voisins:
        
            similar_id = load_voisins()
            st.markdown("<u>Liste des 10 dossiers les plus proches de ce client :</u>", unsafe_allow_html=True)
            st.write(similar_id)
            st.markdown("<i>Target 1 = Client en faillite</i>", unsafe_allow_html=True)
        else:
            st.markdown("<i>Informations masquées</i>", unsafe_allow_html=True)

@st.cache
def load_logo():
    # Construction de la sidebar
    # Chargement du logo
    logo = Image.open("logo.png") 
    return logo

@st.cache()
def load_selectbox():
    # Requête permettant de récupérer la liste des ID clients
    data_json = requests.get(URL_API + "load_data")
    data = data_json.json()
      # Récupération des valeurs sans les [] de la réponse
    lst_id = []
    for i in data:
        lst_id.append(i[0])

    return lst_id

@st.cache()
def load_infos_gen():

    # Requête permettant de récupérer :
    # Le nombre de lignes de crédits existants dans la base
    # Le revenus moyens des clients
    # Le montant moyen des crédits existants
    infos_gen = requests.get(URL_API + "infos_gen")
    infos_gen = infos_gen.json()

    nb_credits = infos_gen[0]
    revenu_moy = infos_gen[1]
    credits_moy = infos_gen[2]

    # Requête permettant de récupérer
    # Le nombre de target dans la classe 0
    # et la classe 1
    targets = requests.get(URL_API + "class_target")    
    targets = targets.json()
    return nb_credits, revenu_moy, credits_moy, targets


def identite_client():
    # Requête permettant de récupérer les informations du client sélectionné
    testurl = URL_API + "infos_client"
    infos_client = requests.get(testurl, params={ "id_client": id_client })
    #infos_client = infos_client.json()
    
    # On transforme la réponse en dictionnaire python
    infos_client = json.loads(infos_client.content)
    
    # On transforme le dictionnaire en dataframe
    infos_client = pd.DataFrame.from_dict(infos_client).T
    return infos_client
@st.cache
def load_age_population():
    
    # Requête permettant de récupérer les âges de la 
    # population pour le graphique situant le client
    data_age_json = requests.get(URL_API + "load_age_population")
    data_age = data_age_json.json()

    return data_age

@st.cache
def load_revenus_population():
    
    # Requête permettant de récupérer les revenus de la 
    # population pour le graphique situant le client
    data_revenus_json = requests.get(URL_API + "load_revenus/population")
    data_revenus = data_revenus_json.json()

    return data_revenus

@st.cache
def load_prediction():
    
    # Requête permettant de récupérer la prédiction
    # de faillite du client sélectionné
    prediction = requests.get(URL_API + "predict", params={"id_client":id_client})
    prediction = prediction.json()
    return prediction[1]


@st.cache
def load_model_interpretation():
    
    # Requête permettant de récupérer la prédiction
    # de faillite du client sélectionné
    explained_model = requests.get(URL_API + "model_interpretation", params={"id_client":id_client})
    explained_model = explained_model.json()
    
    return explained_model

@st.cache()
def load_features():
    # Requête permettant de récupérer la liste des features
    data_json = requests.get(URL_API + "load_features")
    data = data_json.json()
      # Récupération des valeurs sans les [] de la réponse
    lst_id = []
    for i in data:
        lst_id.append(i)
    return lst_id



@st.cache
def load_voisins():
    
    # Requête permettant de récupérer les 10 dossiers
    # les plus proches de l'ID client choisi
    voisins = requests.get(URL_API + "load_voisins", params={"id_client":id_client})

    # On transforme la réponse en dictionnaire python
    voisins = json.loads(voisins.content)
    
    # On transforme le dictionnaire en dataframe
    voisins = pd.DataFrame.from_dict(voisins).T

    # On déplace la colonne TARGET en premier pour plus de lisibilité
    target = voisins["TARGET"]
    voisins.drop(labels=["TARGET"], axis=1, inplace=True)
    voisins.insert(0, "TARGET", target)
    
    return voisins

if __name__ == "__main__":
    main()