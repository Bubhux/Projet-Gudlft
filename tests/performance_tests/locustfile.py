"""
Fichier locustfile.py pour les tests de performance avec Locust.
"""

import os
import threading
import time

from server import app
from locust import HttpUser, task
from server import loadClubs, loadCompetitions


# Utilise une variable partagée pour savoir si le serveur Flask est déjà lancé
server_started = False
print(f"Le serveur Flask est inactif. server_started={server_started}")

# Pour que le démarrage du serveur Flask n'est effectué qu'une seule fois
server_lock = threading.Lock()


# Fonction pour démarrer le serveur Flask
def start_flask_server():
    global server_started
    if not server_started:
        with server_lock:
            if not server_started:
                # Activation de l'environnement de test
                os.environ['FLASK_ENV'] = 'test'

                # Démarre le serveur Flask dans un thread
                server_thread = threading.Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000})
                server_thread.daemon = True
                server_thread.start()

                # Attendre que le serveur soit prêt à recevoir des connexions
                time.sleep(5)

                # Marque le serveur comme démarré
                server_started = True
                print(f"Le serveur Flask est maintenant actif. server_started={server_started}")


# Appel de la fonction pour démarrer le serveur Flask
start_flask_server()


class LocustServerTest(HttpUser):
    """
    Classe LocustServerTest pour simuler les tests de performance avec Locust.
    """

    def on_start(self):
        # Exécutée chaque fois qu'un utilisateur virtuel démarre.
        competition = loadCompetitions()[0]
        club = loadClubs()[0]

        self.client.get("/", name=".index")
        self.client.post("/showSummary", data={"email": club['email']}, name=".showSummary")

    def on_stop(self):
        # Exécutée chaque fois qu'un utilisateur virtuel se termine.
        self.client.get("logout")

    @task
    def performance_index(self):
        # Simule l'accès à la page d'index de l'application.
        self.client.get("/")

    @task
    def performance_login(self):
        # Simule le processus de connexion à l'application.
        club = loadClubs()[0]
        self.client.post("/showSummary", data={"email": club['email']})

    @task
    def performance_logout(self):
        # Simule le processus de déconnexion de l'application.
        self.client.get("/logout")

    @task
    def performance_book(self):
        # Simule l'affichage d'une compétition.
        competition = loadCompetitions()[0]
        club = loadClubs()[0]
        self.client.get(f"/book/{competition['name']}/{club['name']}", name="book")

    @task
    def performance_purchase(self):
        # Simule le processus d'achat de places pour un club dans une compétition.
        competition = loadCompetitions()[0]
        club = loadClubs()[0]
        self.client.post(
            "/purchasePlaces", data={"club": club['name'], "competition": competition['name'], "places": 5}
        )

    @task
    def performance_display_points(self):
        # Simule l'affichage des points des clubs.
        self.client.get("/displayPointsClubs", name="display_points_clubs")
