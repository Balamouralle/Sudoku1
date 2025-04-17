import tkinter as tk
from tkinter import messagebox
import random
import json
import os

#Fenetre princiaple
racine = tk.Tk()
racine.title("PROJET SUDOKU")

#variables globales
Taille=0
entrées=[]
solution=[]
cases_cachées=[]
tableau_actuel=[]
message_correspondant=None

# --- Grilles complètes (à adapter si besoin) ---
tableaux = {
    "Tableau 1": [
        [8, 1, 3, 9, 2, 5, 7, 4, 6],
        [9, 5, 6, 8, 4, 7, 3, 1, 2],
        [4, 7, 2, 3, 6, 1, 8, 9, 5],
        [6, 2, 4, 7, 1, 9, 5, 3, 8],
        [1, 9, 8, 6, 5, 3, 4, 2, 7],
        [3, 8, 5, 4, 2, 6, 9, 7, 1],
        [2, 3, 9, 1, 7, 4, 6, 5, 8],
        [5, 4, 9, 2, 8, 6, 1, 7, 3],
        [7, 6, 1, 5, 9, 8, 2, 3, 4],
    ],
    "Tableau 2": [
        [1, 2, 3, 7, 8, 9, 4, 5, 6],
        [4, 5, 6, 1, 2, 3, 7, 8, 9],
        [7, 8, 9, 4, 5, 6, 1, 2, 3],
        [2, 3, 1, 8, 9, 7, 5, 6, 4],
        [5, 6, 4, 2, 3, 1, 8, 9, 7],
        [8, 9, 7, 5, 6, 4, 2, 3, 1],
        [3, 1, 2, 9, 7, 8, 6, 4, 5],
        [6, 4, 5, 3, 1, 2, 9, 7, 8],
        [9, 7, 8, 6, 4, 5, 3, 1, 2],
    ],
    "Tableau 3": [
        [7, 2, 9, 3, 6, 4, 1, 5, 8],
        [6, 1, 5, 9, 2, 8, 7, 3, 4],
        [4, 9, 3, 2, 8, 1, 7, 6, 5],
        [8, 6, 1, 5, 7, 9, 2, 4, 3],
        [2, 5, 7, 4, 3, 6, 9, 8, 1],
        [3, 4, 8, 1, 5, 7, 6, 2, 9],
        [1, 3, 2, 6, 9, 5, 4, 7, 8],
        [9, 8, 6, 7, 4, 2, 5, 1, 3],
        [5, 7, 4, 8, 1, 3, 2, 9, 6],
    ],
    "Tableau 4": [
        [7, 6, 1, 5, 8, 3, 4, 9, 2],
        [9, 4, 3, 2, 7, 6, 8, 5, 1],
        [8, 5, 2, 4, 9, 1, 3, 6, 7],
        [6, 9, 8, 1, 2, 7, 5, 4, 3],
        [1, 2, 4, 6, 3, 5, 7, 8, 9],
        [3, 7, 5, 9, 4, 8, 6, 1, 2],
        [5, 1, 6, 3, 8, 2, 9, 7, 4],
        [4, 8, 9, 7, 6, 2, 1, 3, 5],
        [2, 3, 7, 8, 1, 9, 5, 6, 4],
    ],
    "Tableau 5": [
        [2, 8, 3, 5, 1, 9, 7, 4, 6],
        [9, 6, 4, 8, 7, 3, 5, 2, 1],
        [7, 1, 5, 6, 2, 4, 3, 9, 8],
        [1, 5, 6, 7, 4, 2, 8, 3, 9],
        [4, 2, 8, 9, 5, 6, 1, 7, 3],
        [3, 7, 9, 1, 8, 5, 2, 6, 4],
        [8, 9, 2, 3, 6, 7, 4, 1, 5],
        [7, 4, 1, 2, 9, 8, 6, 5, 3],
        [6, 3, 1, 2, 5, 8, 4, 9, 7],
    ]
}



# Variables globales
Taille = 9
entrées = []
solution = []
cases_cachées = []
tableau_actuel = []
message_correspondant = None

# Grilles complètes

# (tableaux est inchangé ici, inséré automatiquement précédemment dans ton code)

# Crée l'interface

def créer_interface():
    global entrées
    for lin in range(Taille):
        ligne = []
        for col in range(Taille):
            case = tk.Entry(racine, width=2, font=("Arial", 20), justify="center")
            case.grid(row=lin, column=col, padx=(2 if col % 3 == 0 else 1, 1), pady=(2 if lin % 3 == 0 else 1, 1))
            ligne.append(case)
        entrées.append(ligne)

def charger_tableau(tableau_x):
    global solution, cases_cachées, tableau_actuel
    tableau_actuel = tableau_x
    solution = [ligne.copy() for ligne in tableau_x]
    cases_cachées = []
    while len(cases_cachées) < 30:
        l, c = random.randint(0, Taille - 1), random.randint(0, Taille - 1)
        if (l, c) not in cases_cachées:
            cases_cachées.append((l, c))

    for l in range(Taille):
        for c in range(Taille):
            entré = entrées[l][c]
            entré.config(state="normal")
            entré.delete(0, tk.END)
            if (l, c) in cases_cachées:
                entré.config(bg="black", fg="white")
                entré.bind("<KeyRelease>", lambda e, l=l, c=c: vérifier_valeur(e, l, c))
            else:
                entré.insert(0, str(tableau_x[l][c]))
                entré.config(state="disabled", disabledforeground="black", bg="white")

def vérifier_valeur(e, lin, col):
    val = entrées[lin][col].get()
    if val == "":
        return
    if not val.isdigit() or not (1 <= int(val) <= 9):
        entrées[lin][col].config(bg="red")
        afficher_message("La valeur saisie, doit être un chiffre entre 1 et 9.")
        return
    if int(val) != solution[lin][col]:
        entrées[lin][col].config(bg="red")
        afficher_message("La valeur saisie est incorrecte.")
    else:
        entrées[lin][col].config(bg="white")
        afficher_message("")
    vérifier_si_termine()

def afficher_message(msg):
    if message_correspondant:
        message_correspondant.config(text=msg)

def bouton_pause():
    for l in range(Taille):
        for c in range(Taille):
            entrées[l][c].config(state="disabled")
    afficher_message("Jeu mis en pause.")

def bouton_reprendre():
    for (l, c) in cases_cachées:
        entrées[l][c].config(state="normal")
    afficher_message("Jeu repris.")

def bouton_aide():
    if not cases_cachées:
        afficher_message("Aide non disponible.")
        return
    l, c = random.choice(cases_cachées)
    entrées[l][c].delete(0, tk.END)
    entrées[l][c].insert(0, str(solution[l][c]))
    entrées[l][c].config(state="disabled", disabledforeground="green")
    cases_cachées.remove((l, c))
    afficher_message("Aide fournie.")

def bouton_sauvegarder():
    if not tableau_actuel:
        afficher_message("Aucune grille à sauvegarder.")
        return
    sauvegarde = {
        "tableau": tableau_actuel,
        "grille": [[e.get() if e.get().isdigit() else 0 for e in ligne] for ligne in entrées],
        "cases_cachées": cases_cachées,
    }
    with open("sauvegarde.json", "w") as f:
        json.dump(sauvegarde, f)
    afficher_message("Jeu sauvegardé.")

def bouton_charger():
    global tableau_actuel, solution, cases_cachées
    if not os.path.exists("sauvegarde.json"):
        afficher_message("Aucune sauvegarde trouvée.")
        return
    with open("sauvegarde.json", "r") as f:
        sauvegarde = json.load(f)
    tableau_actuel = sauvegarde["tableau"]
    solution = [ligne.copy() for ligne in sauvegarde["tableau"]]
    cases_cachées = [tuple(c) for c in sauvegarde["cases_cachées"]]
    for l in range(Taille):
        for c in range(Taille):
            entrée = entrées[l][c]
            entrée.config(state="normal")
            entrée.delete(0, tk.END)
            val = sauvegarde["grille"][l][c]
            if (l, c) in cases_cachées and val == 0:
                entrée.config(bg="black", fg="white")
                entrée.bind("<KeyRelease>", lambda e, l=l, c=c: vérifier_valeur(e, l, c))
            else:
                entrée.insert(0, str(val))
                entrée.config(state="disabled", disabledforeground="black", bg="white")
    afficher_message("Jeu chargé.")

def vérifier_si_termine():
    for l, c in cases_cachées:
        val = entrées[l][c].get()
        if not val.isdigit() or int(val) != solution[l][c]:
            return
    afficher_message("Félicitations, vous avez terminé le jeu !")
    for l, c in cases_cachées:
        entrées[l][c].config(state="disabled", disabledforeground="black", bg="white")

def créer_menu_droite():
    global message_correspondant
    for i, nom_tableau in enumerate(tableaux):
        tk.Button(racine, text=nom_tableau, command=lambda t=tableaux[nom_tableau]: charger_tableau(t)).grid(row=i, column=10, padx=5, pady=2)
    tk.Button(racine, text="Pause", command=bouton_pause).grid(row=6, column=10)
    tk.Button(racine, text="Reprendre", command=bouton_reprendre).grid(row=7, column=10)
    tk.Button(racine, text="Aide", command=bouton_aide).grid(row=8, column=10)
    tk.Button(racine, text="Sauvegarder", command=bouton_sauvegarder).grid(row=9, column=10)
    tk.Button(racine, text="Charger", command=bouton_charger).grid(row=10, column=10)
    message_correspondant = tk.Label(racine, text="", fg="blue", justify="left", wraplength=150)
    message_correspondant.grid(row=11, column=10, pady=10)

# Démarrage
créer_interface()
créer_menu_droite()
racine.mainloop()

