#Import de toutes les bibliothèques nécessaires au bon fonctionnement du projet
from transformers import AutoTokenizer, AutoFeatureExtractor, AutoModelForCTC
import torch
import os
import numpy as np
import faiss
import pandas as pd
import matplotlib.pyplot as plt
import time
import torchaudio
import gc
import math
import gradio as gr
import sys
#Chargement du modèle utilisé pour la vectorisation des audios
bundle= torchaudio.pipelines.HUBERT_BASE
model= bundle.get_model()


#variable contenant le chemin vers le fichier animaux.index sur votre ordinateur 
index_path="/Users/ariel/Downloads/animals.index"
#lecture du fichier animaux.index
index = faiss.read_index(index_path)

#variable contenant le chemin vers le fichier noms_animaux.txt
chemin_noms_animaux = '/Users/ariel/Downloads/noms_animaux.txt'

#Traitement du fichier noms_animaux.txt pour pouvoir lier les vecteurs contenus dans animals.index aux noms dans noms_animaux.txt
# Lire le contenu du fichier et le convertir en liste
with open(chemin_noms_animaux, 'r') as fichier:
    # Utiliser une compréhension de liste pour traiter chaque ligne
    names = [line.strip().strip("'").strip(",").strip() for line in fichier.readlines()]




def bayes_theorem(df, n_top_vectors=50):
    # Limite le DataFrame aux n_top_vectors premiers vecteurs
    df_limited = df.head(n_top_vectors)
    # Récupère les catégories uniques et initialise le dictionnaire des probabilités a posteriori
    categories = df_limited['names_normalized'].unique()
    probas_a_posteriori = {categorie: 0 for categorie in categories}
    # Calcul des probabilités a priori uniformes
    probas_a_priori = 1/3
    # Somme des similarités pour chaque catégorie limitée aux 50 premiers vecteurs
    for categorie in categories:
        somme_similarites = df_limited[df_limited['names_normalized'] == categorie]['percentage'].sum()
        probas_a_posteriori[categorie] = somme_similarites * probas_a_priori
    # Normalisation des probabilités a posteriori
    total_proba = sum(probas_a_posteriori.values())
    probas_a_posteriori_normalisees = {categorie: (proba / total_proba) for categorie, proba in probas_a_posteriori.items()}
    return probas_a_posteriori_normalisees
 

#Fonction permettant d'obtenir le nom de l'animal correspondant à chaque vecteur d'audio contenu dans animals.index
def get_name_from_index(index):
    return names[index]

#Fonction de normalisation des noms
def name_normalisation(name):
    if 'dog' in name:
        return "Chien"
    elif 'cat' in name:
        return "Chat"
    elif 'bird' in name:
        return "Oiseau"
    else:
        return "Animal non reconnu"
    

# Définition de la fonction exponentielle négative
def exp_negative(x):
    return math.exp(-x)

#Fonction de normalisation des vecteurs
#j'ai du ajouter un traitement pour les vecteurs 1D car le vecteur de requete contient une seul vecteur et ne peut etre en 2D car comme tu le sais notre processus de traitement des audios nous donne une longue liste contenant tous les caractéritiques dont on a besoin, voila pourquoi le vecteur de requeue est en 1 dimension j'ai donc améliorer la logique de mon code 
def normalization(embeddings):
    # Convertir en un tableau NumPy si ce n'est pas déjà le cas
    #embeddings = np.array(embeddings)

    # Vérifie si embeddings est un vecteur seul (1D) ou une matrice (2D)
    if embeddings.ndim == 1:
        # Normaliser un vecteur seul
        norm = np.linalg.norm(embeddings)
        if norm == 0:
            return embeddings
        return embeddings / norm
    else:
        # Normaliser chaque ligne d'une matrice
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norms
    
#Fonction pour obtenir les représentations vectorielles des audios
def get_audio_embedding(audio_path):
    waveform1, sample_rate1=torchaudio.load(audio_path)
    waveform1=torchaudio.functional.resample(waveform1, sample_rate1, bundle.sample_rate)
    with torch.inference_mode():
            emission1, _ = model(waveform1)

    # Aplatir les deux premières dimensions et garder la troisième
    flattened_features1 = emission1.view(-1, emission1.size(2))
    mean_features1 = flattened_features1.mean(dim=0)
    mean1_array=mean_features1.cpu().numpy().astype(np.float32) 
    mean1_normal=normalization(mean1_array)
    mean1_normal_2d = mean1_normal[np.newaxis, :]
    return mean1_normal_2d

#Fonction de recherche dans l'index animals.index afin de renvoyer les vecteurs d'audios les plus similaires aux vecteurs d'audios donné en entrée
def searchinIndex(index, normal_embedding):
    D,I= index.search(normal_embedding, index.ntotal)
    r=pd.DataFrame({'distance':D[0],'index':I[0]})
    return r


#Fonction qui permet la classification des espèces animales
def animal_classification(audio_path):
    query_audio = get_audio_embedding(audio_path)  # Obtention de l'embedding audio
    results = searchinIndex(index, query_audio)  # Recherche dans l'index
    results['percentage'] = results['distance'].apply(exp_negative) * 100  # Calcul du pourcentage
    results['names'] = results['index'].apply(get_name_from_index)  # Obtention des noms à partir de l'index
    results['names_normalized'] = results['names'].apply(name_normalisation)  # Normalisation des noms
    resultat = bayes_theorem(results, 25)
    formatted_result = '\n'.join([f"{animal}: {percentage:.2%}" for animal, percentage in resultat.items()])
    # Création d'une chaîne de caractères pour les 3 premiers résultats
    return formatted_result

#Fonction permettant d'ajouter un nouvel audio à l'index pour une meilleure classification
def add_in_index(audio_path):
    new_audio=get_audio_embedding(audio_path)
    index.add(new_audio)
    faiss.write_index(index, index_path)
    file_name = os.path.basename(audio_path)
    names.append(file_name)
    result="L'ajout a bien effectué"
    with open(chemin_noms_animaux, 'w') as fichier:
        # Écrire chaque nom dans le fichier, formaté comme un élément de liste Python
        for nom in names:
            fichier.write(f"'{nom}',\n")
    return result


#Création de l'interface graphique utilisé 
interface = gr.Interface(fn=animal_classification, inputs="file", outputs="text")

# Lancez l'interface
interface.launch()

