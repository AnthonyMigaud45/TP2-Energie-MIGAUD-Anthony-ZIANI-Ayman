import csv
import matplotlib.pyplot as plt
from datetime import datetime

def charger_donnees(fichier_csv):
    donnees = []
    with open(fichier_csv, mode='r', encoding='utf-8') as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            # Filtre les valeurs vide et les convertis si nécessaires
            try:
                donnees.append({
                    "Date": ligne["Date"],
                    "Heures": ligne["Heures"],
                    "Consommation": float(ligne["Consommation"]) if ligne["Consommation"] else 0,
                    "Nucleaire": float(ligne["Nucleaire"]) if ligne["Nucleaire"] else 0,
                    "Fioul": float(ligne["Fioul"]) if ligne["Fioul"] else 0,
                    "Charbon": float(ligne["Charbon"]) if ligne["Charbon"] else 0,
                    "Gaz": float(ligne["Gaz"]) if ligne["Gaz"] else 0,
                    "Eolien": float(ligne["Eolien"]) if ligne["Eolien"] else 0,
                    "Solaire": float(ligne["Solaire"]) if ligne["Solaire"] else 0,
                    "Hydraulique": float(ligne["Hydraulique"]) if ligne["Hydraulique"] else 0
                })
            except ValueError:
                continue  # Ignore les erreurs de conversion
    return donnees

def calculer_statistiques(donnees):
    stats = {
        "total_consommation": 0,
        "nucleaire": 0,
        "fioul": 0,
        "charbon": 0,
        "gaz": 0,
        "eolien": 0,
        "solaire": 0,
        "hydraulique": 0
    }
    for ligne in donnees:
        stats["total_consommation"] += ligne["Consommation"]
        stats["nucleaire"] += ligne["Nucleaire"]
        stats["fioul"] += ligne["Fioul"]
        stats["charbon"] += ligne["Charbon"]
        stats["gaz"] += ligne["Gaz"]
        stats["eolien"] += ligne["Eolien"]
        stats["solaire"] += ligne["Solaire"]
        stats["hydraulique"] += ligne["Hydraulique"]

    # Calcul des pourcentages
    total_production = stats["nucleaire"] + stats["fioul"] + stats["charbon"] + stats["gaz"] + stats["eolien"] + stats["solaire"] + stats["hydraulique"]
    for cle in ["nucleaire", "fioul", "charbon", "gaz", "eolien", "solaire", "hydraulique"]:
        stats[f"part_{cle}"] = stats[cle] / total_production * 100 if total_production > 0 else 0

    return stats

def consommation_par_mois(donnees):
    consommation_mensuelle = [0] * 12
    compteurs = [0] * 12

    for ligne in donnees:
        if ligne["Date"]:
            try:
                mois = datetime.strptime(ligne["Date"], "%Y-%m-%d").month - 1
                consommation_mensuelle[mois] += ligne["Consommation"]
                compteurs[mois] += 1
            except ValueError:
                continue

    # Calcule de la moyenne
    return [consommation_mensuelle[i] / compteurs[i] if compteurs[i] > 0 else 0 for i in range(12)]

def afficher_graphiques(stats, consommation_moyenne):

    labels = ["Nucléaire", "Fioul", "Charbon", "Gaz", "Éolien", "Solaire", "Hydraulique"]
    keys = ["nucleaire", "fioul", "charbon", "gaz", "eolien", "solaire", "hydraulique"]
    
    # Récupération des parts associées
    parts = [stats[f"part_{key}"] for key in keys]

    # Affichage des graphiques dans une figure unique
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Camembert
    axs[0].pie(parts, labels=labels, autopct='%1.1f%%', startangle=140)
    axs[0].set_title("Répartition de la production d'énergie")

    # Barres
    mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
    axs[1].bar(mois, consommation_moyenne, color='#56A5F0') #56A5F0 est le code couleur de la couleur de notre graphique
    axs[1].set_title("Consommation moyenne mensuelle en 2022")
    axs[1].set_xlabel("Mois")
    axs[1].set_ylabel("Consommation (MW)")

    # Affichage de la figure
    plt.show()

def final():
    fichier_csv = "RTE_2022.csv"  
    donnees = charger_donnees(fichier_csv)
    
    # Calcul des statistiques globales
    stats = calculer_statistiques(donnees)
    print("Statistiques globales :")
    for cle, valeur in stats.items():
        print(f"{cle} : {valeur}")
    
    # Analyse de la variabilité saisonnière
    consommation_moyenne = consommation_par_mois(donnees)

    # Affichage des graphiques
    afficher_graphiques(stats, consommation_moyenne)

final()