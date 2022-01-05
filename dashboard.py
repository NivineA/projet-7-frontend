from ctypes import string_at
from matplotlib.figure import Figure
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
import plotly.graph_objects as go
from traitlets.traitlets import default


URL_API = 'http://127.0.0.1:5000//'

def main():

    # Affichage du titre et du sous-titre
    st.title("Dashboard de Prêt à Dépenser")
    st.markdown("<i>Implémentez un modèle de scoring</i>", unsafe_allow_html=True)

    #Chargement du logo
    logo = load_logo()
    st.sidebar.image(logo,width=200)

    # Affichage d'informations dans la sidebar
    st.sidebar.header(":memo:Informations du client")
    # Chargement de la selectbox
    lst_id = load_selectbox()
    global id_client
    id_client = st.sidebar.selectbox("ID Client", lst_id)

     # Affichage de l'ID client sélectionné
    st.write("Vous avez sélectionné le client :", id_client)

    #Afficher les informations du client":
        
    infos_client = identite_client()
    st.sidebar.write("**Age client :**", int(infos_client['DAYS_BIRTH'].values /-365), "ans")
    st.sidebar.write("**Sex :**", infos_client['CODE_GENDER'][0])
    st.sidebar.write("**Statut famille :**", infos_client['NAME_FAMILY_STATUS'][0]) 
    st.sidebar.write("**Education :**", infos_client["NAME_EDUCATION_TYPE"][0])
    if int(infos_client["DAYS_EMPLOYED"].values /-365)<0 or int(infos_client["DAYS_EMPLOYED"].values /-365)>100:
        st.sidebar("**Année d'emploi :**",  "inconnu")
    else:
        st.sidebar.write("**Année d'emploi :**", int(infos_client["DAYS_EMPLOYED"].values /-365), "ans")
    st.sidebar.write("**Type de revenu :**", infos_client["NAME_INCOME_TYPE"][0])
    st.sidebar.write("**Revenu :**", int(infos_client["AMT_INCOME_TOTAL"].values ), "euros")
    st.sidebar.write("**Type du contrat :**", infos_client["NAME_CONTRACT_TYPE"][0])
    st.sidebar.write("**Montant crédit :**", int(infos_client["AMT_CREDIT"].values ), "euros")
    st.sidebar.write("**Montant annuité :**", int(infos_client["AMT_ANNUITY"].values ), "euros")

    # Afficher les graphiques des variables:

    st.sidebar.header(":bar_chart:Plus d'informations")
    st.sidebar.subheader("Visualisations univariées")
    variables=['DAYS_BIRTH','CODE_GENDER', 'NAME_FAMILY_STATUS', "NAME_EDUCATION_TYPE", "DAYS_EMPLOYED","NAME_INCOME_TYPE", 
    "AMT_INCOME_TOTAL", "NAME_CONTRACT_TYPE", "AMT_CREDIT", "AMT_ANNUITY"]
    features=st.sidebar.multiselect("les variables à illustrer:", variables)

    for feature in features:
        # Set the style of plots
        plt.style.use('fivethirtyeight')
        fig=plt.figure(figsize=(6, 6))
        if feature=='DAYS_BIRTH':
        # Plot the distribution of feature
            st.write( feature)
            h1=plt.hist(load_age_population(), edgecolor = 'k', bins = 25)
            plt.axvline(int(infos_client["DAYS_BIRTH"].values / -365), color="red", linestyle=":")
            plt.title('Age des Clients', size=5)
            plt.xlabel('Age (Années)', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='DAYS_EMPLOYED':
            st.write( feature)
            h1=plt.hist(load_days_employed_population(), edgecolor = 'k', bins = 25)
            plt.axvline(int(infos_client["DAYS_EMPLOYED"].values / -365), color="red", linestyle=":")
            plt.title('Années emplois des Clients', size=5)
            plt.xlabel('Années emplois (Années)', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='CODE_GENDER':
            st.write(feature)
            h1=plt.hist(load_sex_population(), edgecolor = 'k', bins = 25)
            plt.axvline(infos_client["CODE_GENDER"].item(), color="red", linestyle=":")
            plt.title('Genre des Clients', size=5)
            plt.xlabel('Genre', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='NAME_FAMILY_STATUS':
            st.write(feature)
            h1=plt.hist(load_family_status_population(), edgecolor = 'k', bins = 25)
            plt.axvline(infos_client["NAME_FAMILY_STATUS"].item(), color="red", linestyle=":")
            plt.title('Statut de famille des Clients', size=5)
            plt.xlabel('Statut de famille', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='NAME_EDUCATION_TYPE':
            st.write(feature)
            h1=plt.hist(load_education_population(), edgecolor = 'k', bins = 25)
            plt.axvline(infos_client["NAME_EDUCATION_TYPE"].item(), color="red", linestyle=":")
            plt.title('Niveau éducation des Clients', size=5)
            plt.xlabel('Niveau éducation', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='NAME_INCOME_TYPE':    
            st.write(feature)
            h1=plt.hist(load_income_type_population(), edgecolor = 'k', bins = 25)
            plt.axvline(infos_client["NAME_INCOME_TYPE"].item(), color="red", linestyle=":")
            plt.title('Type de revenus des Clients', size=5)
            plt.xlabel('Type revenus', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            st.pyplot(fig)

        elif feature=='AMT_INCOME_TOTAL':    
            st.write(feature)
            sns.histplot(load_revenus_population())
            plt.axvline(infos_client["AMT_INCOME_TOTAL"][0], color="red", linestyle=":")
            plt.title('Revenus des Clients', size=5)
            plt.xlabel('Revenus en euros', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            plt.xlim([1e5, 8e5])
            st.pyplot(fig)

        elif feature=='AMT_CREDIT':    
            st.write(feature)
            h1=plt.hist(load_credit_population(), edgecolor = 'k', bins = 25)
            plt.axvline(infos_client["AMT_CREDIT"][0], color="red", linestyle=":")
            plt.title('Montant crédit des Clients', size=5)
            plt.xlabel('Montant crédit en euros', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            plt.xlim([1e4, 3e6])
            st.pyplot(fig)

        elif feature=="AMT_ANNUITY":   
            st.write(feature)
            sns.histplot(load_annuity_population())
            plt.axvline(infos_client["AMT_ANNUITY"][0], color="red", linestyle=":")
            plt.title('Montant annuités des Clients', size=5)
            plt.xlabel('Montant annuités en euros', size=5)
            plt.ylabel('Fréquence', size=5)
            plt.xticks(size=5)
            plt.yticks(size=5)
            plt.xlim([1e3, 1e5])
            st.pyplot(fig)

    # graphe analyse bivariée:

    if st.sidebar.checkbox("Visualisez l'analyse bivarié des revenus et montant du crédit des clients"):
        st.write( 'Revenus et montant crédit')
        data_score=load_data_predict()
        fig=plt.figure(figsize=(8,8))
        ax=plt.scatter(x=data_score['AMT_INCOME_TOTAL_y'], y=data_score['AMT_CREDIT_y'], c=data_score['score']*100, cmap='viridis')
        plt.axvline(infos_client["AMT_INCOME_TOTAL"][0], color="red", linestyle=":")
        plt.axhline(infos_client["AMT_CREDIT"][0], color="red", linestyle=":")
        norm = plt.Normalize(data_score['score'].min()*100, data_score['score'] .max()*100)
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
        sm.set_array([])
        ax.figure.colorbar(sm)
        plt.title('Montant crédit en fonction des revenus des Clients', size=5)
        plt.xlabel('Revenu en euros', size=5)
        plt.ylabel('Montant crédit en euros', size=5)
        plt.xticks(size=5)
        plt.yticks(size=5)
        plt.ylim([1e4, 3e6])
        plt.xlim([1e5, 8e5])
        st.pyplot(fig)

    if st.sidebar.checkbox("Visualisez l'analyse bivarié des revenus et âge des clients"):
        st.write( 'Revenus et âge')
        data_score=load_data_predict()
        fig=plt.figure(figsize=(8,8))
        ax=plt.scatter(x=data_score['DAYS_BIRTH_y']/-365, y=data_score['AMT_INCOME_TOTAL_y'], c=data_score['score']*100, cmap='viridis')
        plt.axvline(infos_client["DAYS_BIRTH"][0]/-365, color="red", linestyle=":")
        plt.axhline(infos_client["AMT_INCOME_TOTAL"][0], color="red", linestyle=":")
        norm = plt.Normalize(data_score['score'].min()*100, data_score['score'] .max()*100)
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
        sm.set_array([])
        ax.figure.colorbar(sm)
        plt.title('Revenu en fonction de lâge des clients', size=5)
        plt.xlabel('Age en ans', size=5)
        plt.ylabel('Revenu en euros', size=5)
        plt.xticks(size=5)
        plt.yticks(size=5)
        plt.ylim([1e5, 8e5])
        st.pyplot(fig)

    if st.sidebar.checkbox("Visualisez l'analyse bivarié des années emploi et âge des clients"):
        st.write( 'Age et années emploi')
        data_score=load_data_predict()
        fig=plt.figure(figsize=(8,8))
        ax=plt.scatter(x=data_score['DAYS_BIRTH_y']/-365, y=data_score['DAYS_EMPLOYED_y']/-365, c=data_score['score']*100, cmap='viridis')
        plt.axvline(infos_client["DAYS_BIRTH"][0]/-365, color="red", linestyle=":")
        plt.axhline(infos_client["DAYS_EMPLOYED"][0]/-365, color="red", linestyle=":")
        norm = plt.Normalize(data_score['score'].min()*100, data_score['score'] .max()*100)
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
        sm.set_array([])
        ax.figure.colorbar(sm)
        plt.title('Années emploi en fonction de lâge  des clients', size=5)
        plt.xlabel('Age en ans', size=5)
        plt.ylabel('Années emploi en ans', size=5)
        plt.xticks(size=5)
        plt.yticks(size=5)
        plt.ylim([0,30])
        st.pyplot(fig)
    
# Affichage solvabilité client

    st.header("**Analyse dossier client**")
    st.markdown("<u>Probabilité de risque de faillite du client :</u>", unsafe_allow_html=True)
    prediction = load_prediction()
    risque=round(prediction*100, 2)
    st.write(risque, "%")
    st.markdown("<u>Données client :</u>", unsafe_allow_html=True)
    st.write(identite_client()) 
    threshold= st.slider("Choisir le seuil",  0, 100, 50)
    fig=plt.figure(figsize=(6, 6))
    fig=go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]},
    value = risque,
    mode = "gauge+number",
    title = {'text': "Probabilité de faillite"},
    gauge = {'axis': {'range': [None, 100]},
            'bar': {'color': "black", "thickness":0.1},
             'steps' : [
                 {'range': [0, 20], 'color': "green"},
                 {'range': [20, 40], 'color': "blue"},
                 {'range': [40, 60], 'color': "yellow"},
                 {'range': [60, 80], 'color': "purple"},
                 {'range': [80, 100], 'color': "red"}],

             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': threshold}}))
    
    st.plotly_chart(fig)
    if risque<=20:
        st.success('Risque de faillite qualifiée faible : crédit acceptée')
    elif risque<=40:
       st.success('Risque de faillite qualifiée bas : crédit acceptée') 
    elif risque<=60:
       st.success('Risque de faillite qualifiée moyen : crédit non acceptée') 
    elif risque<=80:
       st.success('Risque de faillite qualifiée bon : crédit non acceptée') 
    else:
      st.success('Risque de faillite qualifiée grand : crédit non acceptée')    


 # Affichage interprétation du modèle 
 #   
    st.markdown("<u>Interprétation du modèle - Importance des variables locale :</u>", unsafe_allow_html=True)
    if st.checkbox("Interpréter le modèle"):
        features=load_features()
        explained_model=load_model_interpretation_shap()[0]
        infos_client=load_data_shap()
        number = st.slider("Choisir le numéro des features...", 0, 30, 15)
        explained_models=pd.DataFrame(explained_model, columns=features)
        fig=plt.figure(figsize=(8,8))
        shap.summary_plot(explained_models, np.hstack(infos_client), max_display=number, plot_type ="bar",  color_bar=False, plot_size=(5, 5))
        st.pyplot(fig)
        st.markdown("<u>Interprétation du modèle - Importance des variables globale :</u>", unsafe_allow_html=True) 
        feature_importance=load_feature_importance()
        df = pd.DataFrame({'feature': features,
                                    'importance': feature_importance}).sort_values('importance', ascending = False)
        df = df.sort_values('importance', ascending = False).reset_index()
    
        # Normalize the feature importances to add up to one
        df['importance_normalized'] = df['importance'] / df['importance'].sum()
       # Make a horizontal bar chart of feature importances
        fig=plt.figure(figsize = (15, 10))
        ax = plt.subplot()
        # Need to reverse the index to plot most important on top
        ax.barh(list(reversed(list(df.index[:30]))), 
            df['importance_normalized'].head(30), 
            align = 'center', edgecolor = 'k')
    
        # Set the yticks and labels
        ax.set_yticks(list(reversed(list(df.index[:30]))))
        ax.set_yticklabels(df['feature'].head(30))
    
        # Plot labeling
        plt.xlabel('Normalized Importance'); plt.title('Feature Importances')
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
    # Chargement du logo
    logo = Image.open("logo.png") 
    return logo

@st.cache
def load_selectbox():
    # Requête permettant de récupérer la liste des ID clients
    data_json = requests.get(URL_API + "load_data")
    data = data_json.json()
      # Récupération des valeurs sans les [] de la réponse
    lst_id = []
    for i in data:
        lst_id.append(i[0])

    return lst_id


def identite_client():
    # Requête permettant de récupérer les informations du client sélectionné
    testurl = URL_API + "infos_client"
    infos_client = requests.get(testurl, params={ "id_client": id_client })
    infos_client = json.loads(infos_client.content)
    # On transforme le dictionnaire en dataframe
    infos_client = pd.DataFrame.from_dict(infos_client).T
    return infos_client

def load_data_test():
    # Requête permettant de récupérer les informations des clients
    testurl = URL_API + "load_data_test"
    data_test = requests.get(testurl)
    data_test = json.loads(data_test.content)
    data_test = pd.DataFrame.from_dict(data_test).T
    return data_test

@st.cache
def load_age_population():
    
    # Requête permettant de récupérer les âges de la 
    # population pour le graphique situant le client
    data_age_json = requests.get(URL_API + "load_age_population")
    data_age = data_age_json.json()

    return data_age

@st.cache
def load_days_employed_population():
    
    # Requête permettant de récupérer les années d'emploi de la 
    # population pour le graphique situant le client
    data_days_json = requests.get(URL_API + "load_days_employed_population")
    data_days = data_days_json.json()

    return data_days

@st.cache
def load_sex_population():
    
    # Requête permettant de récupérer les sexes de la 
    # population pour le graphique situant le client
    data_genre_json = requests.get(URL_API + "load_sex_population")
    data_genre = data_genre_json.json()

    return data_genre

@st.cache
def load_family_status_population():
    
    # Requête permettant de récupérer les statuts familles de la 
    # population pour le graphique situant le client
    data_famille_json = requests.get(URL_API + "load_family_status_population")
    data_famille = data_famille_json.json()

    return data_famille

@st.cache
def load_education_population():
    
    # Requête permettant de récupérer le niveau d'éducation de la 
    # population pour le graphique situant le client
    data_education_json = requests.get(URL_API + "load_education_population")
    data_education = data_education_json.json()

    return data_education

@st.cache
def load_income_type_population():
    
    # Requête permettant de récupérer le type des revenus de la 
    # population pour le graphique situant le client
    data_income_json = requests.get(URL_API + "load_income_type_population")
    data_income = data_income_json.json()

    return data_income

    
@st.cache
def load_contract_type_population():
    
    # Requête permettant de récupérer le type de contract de la 
    # population pour le graphique situant le client
    data_contract_json = requests.get(URL_API + "load_contract_type_population")
    data_contract = data_contract_json.json()

    return data_contract


@st.cache
def load_revenus_population():
    
    # Requête permettant de récupérer les revenus de la 
    # population pour le graphique situant le client
    data_revenus_json = requests.get(URL_API + "load_revenus_population")
    data_revenus = data_revenus_json.json()

    return data_revenus

@st.cache
def load_credit_population():
    
    # Requête permettant de récupérer le montant des crédits de la 
    # population pour le graphique situant le client
    data_credit_json = requests.get(URL_API + "load_credit_population")
    data_credit = data_credit_json.json()

    return data_credit

@st.cache
def load_annuity_population():
    
    # Requête permettant de récupérer le montant des annuités de la 
    # population pour le graphique situant le client
    data_annuity_json = requests.get(URL_API + "load_annuity_population")
    data_annuity = data_annuity_json.json()

    return data_annuity

@st.cache
def load_prediction():
    
    # Requête permettant de récupérer la prédiction
    # de faillite du client sélectionné
    prediction = requests.get(URL_API + "predict", params={"id_client":id_client})
    prediction = prediction.json()
    return prediction[1]

@st.cache
def load_data_predict():
    # Requête permettant de récupérer les informations du client sélectionné avec le score calculé
    testurl = URL_API + "load_data_predict"
    infos_clients = requests.get(testurl)
    infos_clients = json.loads(infos_clients.content)
    # On transforme le dictionnaire en dataframe
    infos_clients = pd.DataFrame.from_dict(infos_clients).T
    return infos_clients

@st.cache
def load_model_interpretation_shap():
    
    # Requête permettant de récupérer les valeurs shap pour un client séléctionné pour les deux classes
    explained_model = requests.get(URL_API + "model_interpretation_shap", params={"id_client":id_client})
    explained_model = explained_model.json()
    lst_id = []
    for i in  explained_model:
        lst_id.append(i)
    return lst_id
    

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

@st.cache()
def load_feature_importance():
    # Requête permettant de récupérer la liste des features importance
    data_json = requests.get(URL_API + "load_feature_importance")
    data = data_json.json()
      # Récupération des valeurs sans les [] de la réponse
    lst_id = []
    for i in data:
        lst_id.append(i)
    return lst_id

@st.cache()
def load_data_shap():
    # Requête permettant de récupérer la données utilisés pour l'interprétation du modèle
    testurl = URL_API + "load_data_shap"
    infos_client = requests.get(testurl, params={ "id_client": id_client })
    infos_client = json.loads(infos_client.content)
    # On transforme le dictionnaire en dataframe
    infos_client = pd.DataFrame.from_dict(infos_client).T
    return infos_client 

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