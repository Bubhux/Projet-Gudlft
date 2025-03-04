"""
Fichier test_server_functional.py pour effectuer des tests de fonctionnalités avec Selenium.
"""

import os
import time
import threading

from server import app, load_mock_clubs, load_mock_competitions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestServerFunctional:
    """
        Cette classe contient des tests fonctionnels pour l'application Flask de GUDLFT Registration.
        Les tests vérifient le fonctionnement du serveur, la navigation sur les pages, la saisie de données,
        et la validation de l'affichage. Chaque méthode de test est conçue pour tester un aspect spécifique
        de l'application. Les tests sont les suivants :

        - test_home_page: Vérifie que la page d'accueil s'affiche correctement et contient le titre attendu.

        - test_display_points_table_clubs: Vérifie que la page "View clubs points" s'affiche correctement et
          affiche le message "Points available by clubs".

        - test_login_user: Teste le processus de connexion de l'utilisateur et vérifie que la page de bienvenue
          affiche l'adresse e-mail de l'utilisateur connecté.

        - test_book_places_reservation_success: Teste le processus de réservation de places pour une compétition.
          Il simule la sélection de places, la réservation et vérifie le message de confirmation. Ensuite, le test
          vérifie que les points disponibles sont mis à jour conformément à la réservation effectuée et que le nombre
          de places disponibles pour cette compétition est correctement réduit.

        - test_logout: Teste le processus de déconnexion de l'utilisateur et vérifie que l'utilisateur est redirigé
          vers la page de connexion.

        :param mocker: Utilisé pour simuler les données de clubs et de compétitions via les
         fonctions `load_mock_clubs` et `load_mock_competitions`.

        Les tests utilisent le framework Pytest et le navigateur Web Selenium pour automatiser les interactions avec
        l'application. Ils assurent que l'application fonctionne correctement du point de vue de l'utilisateur.
    """

    def setup_method(self, method):
        # Activation de l'environnement de test
        os.environ['FLASK_ENV'] = 'test'

        # Démarre le serveur Flask dans un thread
        self.server_thread = threading.Thread(target=self.start_flask_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        # Attend que le serveur soit prêt à recevoir des connexions
        time.sleep(2)

        # Initialisation du pilote WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/")

    def teardown_method(self, method):
        # Reviens à l'environnement de production
        self.driver.quit()
        os.environ['FLASK_ENV'] = 'production'

    def start_flask_server(self):
        # Démarre le serveur Flask en mode test
        app.run(host='127.0.0.1', port=5000)

    def test_home_page(self, mocker):
        mocker.patch('server.saveClubs')  # Mock de la fonction saveClubs
        mocker.patch('server.saveCompetitions')  # Mock de la fonction saveCompetitions

        # Ouvre la page d'accueil
        self.driver.get("http://127.0.0.1:5000/")

        print("Page title:", self.driver.title)

        # Vérifie les éléments de la page
        assert "GUDLFT | Registration" in self.driver.title

        time.sleep(3)

    def test_display_points_table_clubs(self, mocker):
        mocker.patch('server.saveClubs')  # Mock de la fonction saveClubs
        mocker.patch('server.saveCompetitions')  # Mock de la fonction saveCompetitions

        # Ouvre la page d'accueil
        self.driver.get("http://127.0.0.1:5000/")

        # Trouve le lien "View clubs points" par son texte
        view_clubs_link = self.driver.find_element(By.LINK_TEXT, "View clubs points")

        time.sleep(3)

        # Clique sur le lien "View clubs points"
        view_clubs_link.click()

        # Selenium attend 5 secondes que la page soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

        # Trouve l'élément h2 avec le texte "Points available by clubs"
        h2_element = self.driver.find_element(By.XPATH, "//h2[text()='Points available by clubs']")

        # Imprime des vérifications dans le terminal
        page_title = self.driver.title
        points_table_clubs_message = h2_element.text

        print("Page title:", page_title)
        print("Points available by clubs message:", points_table_clubs_message)

        # Vérifie les éléments de la page
        assert "Clubs Points | GUDLFT Registration" in page_title
        assert "Points available by clubs" in points_table_clubs_message

        time.sleep(3)

    def test_login_user(self, mocker):
        mocker.patch('server.saveClubs')  # Mock de la fonction saveClubs
        mocker.patch('server.saveCompetitions')  # Mock de la fonction saveCompetitions

        # Ouvre la page d'accueil
        self.driver.get("http://127.0.0.1:5000/")

        time.sleep(3)

        # Remplis le champ d'adresse e-mail et se connecte
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("john@simplylift.co")

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Selenium attend 5 secondes que la page soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

        # Imprime des vérifications dans le terminal
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h2").text

        print("Welcome message:", welcome_message)

        # Vérifie les éléments de la page
        assert "Welcome, john@simplylift.co - Simply Lift" in welcome_message

        time.sleep(3)

    def test_book_places_reservation_success(self, mocker):
        mocker.patch('server.saveClubs')  # Mock de la fonction saveClubs
        mocker.patch('server.saveCompetitions')  # Mock de la fonction saveCompetitions

        load_mock_clubs()
        load_mock_competitions()

        # Ouvre la page d'accueil
        self.driver.get("http://127.0.0.1:5000/")

        time.sleep(3)

        # Remplis le champ d'adresse e-mail et se connecter
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("john@simplylift.co")

        time.sleep(3)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Attends que la page http://127.0.0.1:5000/showSummary soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be("http://127.0.0.1:5000/showSummary")
        )

        # Vérifie que vous êtes sur la page de résumé
        assert "http://127.0.0.1:5000/showSummary" in self.driver.current_url

        time.sleep(3)

        # Selenium attend 5 secondes que la page soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

        # Clique sur le premier lien "Book Places"
        book_places_link = self.driver.find_element(By.LINK_TEXT, "Book Places")
        book_places_link.click()

        # Assure que les données de la compétition "Spring Festival" sont chargées
        competition_name = self.driver.find_element(By.CSS_SELECTOR, "h2").text
        assert competition_name == "Competition Spring Festival"

        time.sleep(3)

        # Selenium attend 5 secondes que la page de réservation soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[action='/purchasePlaces']"))
        )

        # Sélectionne 5 places dans le formulaire de réservation
        places_input = self.driver.find_element(By.NAME, "places")
        places_input.send_keys("5")

        time.sleep(3)

        # Clique sur le bouton "Book"
        book_button = self.driver.find_element(By.CSS_SELECTOR, "form[action='/purchasePlaces'] button[type='submit']")
        book_button.click()

        # Selenium attend 5 secondes pour que la réservation soit traitée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

        # Vérifie si le message "Great-booking complete!" est présent
        messages = self.driver.find_elements(By.CSS_SELECTOR, "ul li")
        message_text = "Great-booking complete!"

        message_found = False
        for message in messages:
            if message_text in message.text:
                message_found = True
                break

        assert message_found

        # Vérifie les points, le nombre de places et la date après la mise à jour des données
        points_element = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Points available:')]")
        assert "Points available: 8" in points_element.text

        date_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul li")
        date_found = False

        for element in date_elements:
            if "Date: 2028-03-27 10:00:00" in element.text:
                date_found = True
                break

        assert date_found
        #print(element.text)

        place_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul li")
        place_found = False

        for place in place_elements:
            if "Number of Places: 20" in place.text:
                place_found = True
                break

        assert place_found
        #print(place.text)

        time.sleep(3)

    def test_logout(self, mocker):
        mocker.patch('server.saveClubs')  # Mock de la fonction saveClubs
        mocker.patch('server.saveCompetitions')  # Mock de la fonction saveCompetitions

        # Ouvre la page d'accueil
        self.driver.get("http://127.0.0.1:5000/")

        time.sleep(3)

        # Remplis le champ d'adresse e-mail et se connecter
        email_input = self.driver.find_element(By.NAME, "email")
        email_input.send_keys("john@simplylift.co")

        time.sleep(3)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Attends que la page http://127.0.0.1:5000/showSummary soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be("http://127.0.0.1:5000/showSummary")
        )

        # Imprime des vérifications dans le terminal
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, "h2").text

        # Vérifie que vous êtes sur la page de résumé
        assert "http://127.0.0.1:5000/showSummary" in self.driver.current_url

        # Vérifie les éléments de la page
        assert "Welcome, john@simplylift.co - Simply Lift" in welcome_message

        print("Welcome message:", welcome_message)

        # Selenium attend 5 secondes que la page soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

        time.sleep(3)

        # Clique sur le lien "Logout"
        logout_link = self.driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()

        # Selenium attend 5 secondes que la page de déconnexion soit chargée
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )

        # Vérifie si l'utilisateur est redirigé vers la page de connexion
        email_input = self.driver.find_element(By.NAME, "email")

        assert email_input is not None

        time.sleep(3)
