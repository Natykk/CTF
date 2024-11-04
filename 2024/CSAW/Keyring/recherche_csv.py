import numpy as np
import pandas as pd

# Dictionnaire contenant les statistiques de référence pour chaque clé connue.
# Les statistiques incluent les moyennes (mean_x, mean_y, mean_z) et les écarts-types (std_x, std_y, std_z)
# pour les coordonnées X, Y et Z.
keys_stats = {
    'Key A': {'mean_x': 0.084, 'mean_y': 0.065, 'mean_z': 10.02, 'std_x': 0.46, 'std_y': 0.36, 'std_z': 0.18},
    'Key B': {'mean_x': -0.084, 'mean_y': 0.059, 'mean_z': 9.99, 'std_x': 0.42, 'std_y': 0.34, 'std_z': 0.16},
    'Key C': {'mean_x': -0.072, 'mean_y': 0.082, 'mean_z': 10.05, 'std_x': 0.45, 'std_y': 0.38, 'std_z': 0.17},
    'Key D': {'mean_x': 0.101, 'mean_y': 0.053, 'mean_z': 9.988, 'std_x': 0.43, 'std_y': 0.34, 'std_z': 0.16}
}

# Fonction pour calculer les statistiques d'un DataFrame donné.
# Les statistiques calculées incluent la moyenne et l'écart-type pour chaque axe (X, Y, Z).
def calculate_statistics(df):
    # Calcul de la moyenne et de l'écart-type pour chaque axe
    stats = {
        'mean_x': df['X'].mean(),
        'mean_y': df['Y'].mean(),
        'mean_z': df['Z'].mean(),
        'std_x': df['X'].std(),
        'std_y': df['Y'].std(),
        'std_z': df['Z'].std()
    }
    return stats  # Retourne un dictionnaire contenant les statistiques calculées

# Fonction pour calculer la distance euclidienne entre les statistiques d'un échantillon et celles d'une clé connue.
# Cette distance mesure la similarité globale entre l'échantillon et la clé en comparant les moyennes et écarts-types.
def calculate_euclidean_distance(sample, key_stats):
    # Calcul des différences de moyenne entre l'échantillon et les statistiques de la clé
    mean_diff = np.array([
        sample['mean_x'] - key_stats['mean_x'],
        sample['mean_y'] - key_stats['mean_y'],
        sample['mean_z'] - key_stats['mean_z']
    ])
    
    # Calcul des différences d'écart-type entre l'échantillon et les statistiques de la clé
    std_diff = np.array([
        sample['std_x'] - key_stats['std_x'],
        sample['std_y'] - key_stats['std_y'],
        sample['std_z'] - key_stats['std_z']
    ])
    
    # Calcul de la distance euclidienne totale en sommant les carrés des différences de moyennes et d'écarts-types
    total_diff = np.sqrt(np.sum(mean_diff ** 2) + np.sum(std_diff ** 2))
    return total_diff  # Retourne la distance euclidienne totale

# Liste des fichiers d'échantillons CSV à analyser
list_sample_final = [
    'sample1.csv', 'sample2.csv', 'sample9.csv', 'sample11.csv', 'sample12.csv', 
    'sample15.csv', 'sample16.csv', 'sample18.csv', 'sample21.csv', 'sample22.csv', 
    'sample23.csv', 'sample27.csv', 'sample28.csv', 'sample30.csv', 'sample31.csv', 
    'sample32.csv', 'sample33.csv', 'sample34.csv', 'sample38.csv', 'sample39.csv'
]

# Boucle sur chaque fichier d'échantillon pour calculer ses statistiques et trouver la clé correspondante
for i in list_sample_final:
    # Chargement des données du fichier CSV dans un DataFrame
    df = pd.read_csv('samples/' + i)
    
    # Suppression de la colonne 'TimeStamp' car elle n'est pas nécessaire pour le calcul des statistiques
    df = df.drop(columns=['TimeStamp'])
    
    # Calcul des statistiques de l'échantillon
    sample_stats = calculate_statistics(df)
    print(f"Stats pour {i}: {sample_stats}")
    
    # Enregistrement des statistiques dans un fichier texte pour chaque échantillon
    with open('stats.txt', 'a') as f:
        f.write(f"{i}: {sample_stats}\n")
    
    # Calcul de la distance entre l'échantillon et chaque clé connue
    differences = {key: calculate_euclidean_distance(sample_stats, stats) for key, stats in keys_stats.items()}

    # Identification de la clé la plus proche (celle avec la plus petite différence)
    closest_key = min(differences, key=differences.get)

    # Enregistrement de la clé la plus proche dans un fichier texte et affichage dans la console
    with open('closest_key.txt', 'a') as f:
        f.write(f"Le sample est le plus proche de la {closest_key}.\n")
    print(f"Le sample est le plus proche de la {closest_key}.")

