 
# Votre client est un site de partage de vélo communautaire.
#Au cours de la dernière décennie, les systèmes de partage de vélos ont gagné en nombre et en popularité dans les villes du monde entier.
#Ils permettent aux utilisateurs de louer des vélos à très court terme contre un prix.
#Les technologies d'information facilitent l'accès à ces systèmes pour débloquer ou retourner des vélos.
 
#Les données qui vont sont mis à disposition concernent 3 grandes villes au USA (New York, Chicago et Washington).
#Les données concernent les 6 premiers mois de l'année 2017 pour New York, puis Juillet, Aout et Septembre 2017 pour Chicago et enfin, Octobre, Novembre et Décembre 2017 pour Washington.
 
# Votre mission pour ce client et de lui créer une application en python, en ligne de commande qui va lui permettre les opérations suivantes :
 
# - Selectionner l'une des 3 villes (New york city, Washington ou Chicago)
# - Selectionner le mois (Janvier - Février - Mars - Avril - Juin, etc.).
 
# Une fois ces informations recoltées, vous obtenez les informations traitées suivantes :
 
#  - Le jour de la semaine avec le plus d'activité.
#  - L'heure de démarrage la plus courante.
#  - La durée de voyage moyen sur la période (mois).
#  - Le total pour chaque catégorie de User.
#  - Le nombre total de femmes et d'hommes sur la période.
#  - L'année de naissance la plus ancienne.
#  - L'année de naissance la plus récente.
#  - L'année de naissance la plus courante sur la période (avec le nombre d'occurence).


 
# En enfin, demandez s'il souhaite qu'on affiche les 10 premières données de la période selectionnée sous forme de tableau.
 
# Si l'utilisateur souhaite de nouveau faire des traitements sur d'autres villes, il n'aura pas à redémarrer l'application.



import mysql.connector, csv
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
pd.options.mode.chained_assignment = None 


def list_mois(df):
    df['month']=pd.to_datetime(df['Start Time']).dt.month
    mois_df=df['month'].unique()
    mois_df=np.sort(mois_df)
    mois_df=list(mois_df)
    return mois_df


def menu1():
    while True:
        print("""\n=== MENU VILLE ===
Selectionnez une ville:
1. New York
2. Chicago
3. Washigton
0. Quitter le programme""")
        choice = input("Votre choix : ")
        if choice in ['0','1','2','3']:
            return choice
        else:
            print("Une erreur s'est produite lors de votre saisie\nVeuillez réessayer\n")


def menu2(df):
    mois={1 : "Janvier", 2 : "Fevrier", 3 : "Mars", 4 : "Avril", 5 : "Mai", 6 : "Juin",7 : "Juillet", 8 : "Aout", 9 : "Septembre", 10 : "Octobre", 11 : "Novembre", 12 : "Decembre"}
    listo=list_mois(df)
    while True:
        print("===MENU MOIS===")
        for k in listo:
            print(f"{k}) : {mois[k]}")
        choice= int(input("Votre choix : "))
        if choice in listo:
            return choice
        else:
            print("Une erreur s'est produite lors de votre saisie\nVeuillez réessayer\n")


def df_mois(df,int):
    df_mois=df[df['month']==int]
    return df_mois


def jour_max_act(df):
    ser_date=pd.to_datetime(df['Start Time'])
    ser_date=ser_date.dt.date
    df_date=ser_date.rename('date').reset_index()
    dff=df_date.groupby('date').size().rename('count_per_day').reset_index().sort_values('count_per_day',ascending=False).head(1)
    return dff['date'].iloc[0]


def heure_max_act(df):
    ser_date=pd.to_datetime(df['Start Time'])
    ser_date=ser_date.dt.hour
    df_date=ser_date.rename('hour').reset_index()
    dff=df_date.groupby('hour').size().rename('count_per_hour').reset_index().sort_values('count_per_hour',ascending=False).head(1)
    return dff['hour'].iloc[0]


def voy_moy(df):
    moy=df['Trip Duration'].mean().round(2)
    return moy


def cat_user(df):
    df_cat_user=df.groupby('User Type').size().rename('count_usertype').reset_index()
    dico={}
    for i in range(df_cat_user['User Type'].size):
        dico[df_cat_user['User Type'].iloc[i]]=df_cat_user['count_usertype'].iloc[i]
    return dico


def count_gender(df):
    df['Gender']=df['Gender'].replace({0:"Femme",1:"Homme",2:"Autre"})
    df_gender=df.groupby('Gender').size().rename('count_gender').reset_index()
    dico={}
    for i in range(df_gender['Gender'].size):
        dico[df_gender['Gender'].iloc[i]]=df_gender['count_gender'].iloc[i]
    return dico


def year_max(df):
    age_max=df['Birth Year'].min()
    age_max=age_max.astype('int32')
    return age_max


def year_min(df):
    age_min=df['Birth Year'].max()
    age_min=age_min.astype('int32')
    return age_min


def age_courant(df):
    df_age_courant=df.groupby('Birth Year').size().rename('count_birth').reset_index().sort_values('count_birth',ascending=False).head(1)
    return df_age_courant['Birth Year'].iloc[0]




def main():
    
    file_path1="./TP2/cleaned_new_york_city.csv"
    file_path2="./TP2/cleaned_chicago_city.csv"
    file_path3="./TP2/cleaned_washington_city.csv"
    #les 3 csv filepath

    df_NY=pd.read_csv(file_path1)
    df_CH=pd.read_csv(file_path2)
    df_WA=pd.read_csv(file_path3)
    #les 3 df via les csv

    df_NY=df_NY[['Start Time','Trip Duration','User Type','Gender','Birth Year']]
    df_NY=df_NY.dropna()
    df_NY['Birth Year']=df_NY['Birth Year'].astype('int32')
    df_NY['month']=pd.to_datetime(df_NY['Start Time']).dt.month

    df_CH=df_CH[['Start Time','Trip Duration','User Type','Gender','Birth Year']]
    df_CH['month']=pd.to_datetime(df_CH['Start Time']).dt.month
    df_CH=df_CH.dropna()
    df_CH['Birth Year']=df_CH['Birth Year'].astype('int32')

    df_WA=df_WA[['Start Time','Trip Duration','User Type','Gender','Birth Year']]
    df_WA['month']=pd.to_datetime(df_WA['Start Time']).dt.month
    df_WA=df_WA.dropna()
    df_WA['Birth Year']=df_WA['Birth Year'].astype('int32')
    #pour les 3 df, on ne prend que les colonnes utiles pour le TP
    #on transforme la date pour qu'on puisse l'exploiter
    #on retire les données nulles
    #on transforme la colonne Birth Year en int pour éviter les année 1900.0

    while True:
        choice=menu1() #menu pour choisir la ville
        
        if choice=="0":
            print("Merci d'avoir utilisé nos services\nAu revoir")
            break

        elif choice=="1": 
            data=df_NY #on choisit le DF de NY

        elif choice=="2": 
            data=df_CH #on choisit le DF de Wasington

        elif choice=="3": 
            data=df_WA #on choisit le DF de Chicago

        mois=menu2(data) #on affiche les mois disponibles dans le DF de NY
        df=df_mois(data,mois) #on sélectionne le DF du mois sélectionné
        print(f"\nLe jour ayant engristré la plus grande activité est : {jour_max_act(df)}\n")
        print(f"L'heure de démarrage la plus courante est : {heure_max_act(df)}h \n")
        print(f"La durée de voyage moyen est de {voy_moy(df)} secondes\n")
        for k,v in cat_user(df).items():
            print(f"Il y a {v} users de type : {k}\n")
        for k,v in count_gender(df).items():
            print(f"Il y a {v} utilisateurs qui sont {k}\n")
        print(f"L'année de naissance la plus ancienne est :{year_max(df)}\n")
        print(f"L'année de naissance la moins ancienne est :{year_min(df)}\n")
        print(f"L'année la plus représentée est :{age_courant(df)}\n")


main()