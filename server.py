<<<<<<< HEAD
"""
Application d'Inscription GUDLFT
Cette application Flask sert de portail d'inscription pour GUDLFT.
Elle permet aux utilisateurs de consulter et de réserver des athlètes pour des compétitions et de gérer les points du club.
Elle charge les données des clubs et des compétitions à partir de fichiers JSON et fournit diverses routes pour interagir avec l'application.
"""

=======
>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
import os
import json
import logging

from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session


class CompetitionNotFoundException(Exception):
    flash_message = 'Competition not found.'


class CompetitionPassedException(Exception):
    flash_message = 'The competition has already passed.'


class CompetitionFullException(Exception):
    flash_message = 'The competition is already full.'


class InvalidPlacesException(Exception):
    flash_message = 'Please enter a valid number for places.'


class MaximumPlacesException(Exception):
    flash_message = 'You can book a maximum of 12 athletes at once.'


class NotEnoughPointsException(Exception):
    flash_message = 'You do not have enough points to make this booking.'


<<<<<<< HEAD
# Variables globales pour stocker les messages de chargement
clubs_load_message = None
competitions_load_message = None


=======
clubs_load_message = None
competitions_load_message = None

>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
def load_mock_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]

<<<<<<< HEAD

=======
>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
def load_mock_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]

<<<<<<< HEAD

=======
>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
def loadClubs():
    global clubs_load_message
    filename = 'clubs.json'
    if os.environ.get('FLASK_ENV') == 'test':
        clubs_load_message = "Succes Mock data loaded for clubs."
        return load_mock_clubs()
    try:
        with open(filename) as c:
            listOfClubs = json.load(c)['clubs']
            clubs_load_message = f"Succes Database loaded for clubs. {len(listOfClubs)} clubs loaded from '{filename}'"
            app.logger.info(clubs_load_message)
            return listOfClubs
    except FileNotFoundError:
        clubs_load_message = f"Failed to load the clubs database. '{filename}' not found."
        app.logger.error(clubs_load_message)
        return None


def loadCompetitions():
    global competitions_load_message
    filename = 'competitions.json'
    if os.environ.get('FLASK_ENV') == 'test':
        competitions_load_message = "Succes Mock data loaded for competitions."
        return load_mock_competitions()
    try:
        with open(filename) as comps:
            listOfCompetitions = json.load(comps)['competitions']
            competitions_load_message = f"Succes Database loaded for competitions. {len(listOfCompetitions)} competitions loaded from '{filename}'"
            app.logger.info(competitions_load_message)
            return listOfCompetitions
    except FileNotFoundError:
        competitions_load_message = f"Failed to load the competitions database. '{filename}' not found."
        app.logger.error(competitions_load_message)
        return None


# Créer une instance de l'application Flask.
app = Flask(__name__)
app.secret_key = 'something_special'

<<<<<<< HEAD
# Configuration de la journalisation
app.logger.setLevel(logging.INFO)

# Chargement des données des compétitions et des clubs depuis des fichiers JSON.
# Ces variables sont globales et accessibles depuis l'ensemble de l'application.
=======
app.logger.setLevel(logging.INFO)

>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    clubs = loadClubs()
    competitions = loadCompetitions()
    return render_template('index.html', clubs_load_message=clubs_load_message, competitions_load_message=competitions_load_message)


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    clubs = loadClubs()
    competitions = loadCompetitions()

    if request.method == 'POST':
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            session['club'] = club
            return render_template('welcome.html', club=club, competitions=competitions)
        except IndexError:
            if request.form['email'] == "":
                flash("Enter your email", 'error')
                return redirect(url_for('index'))
            else:
                flash("Email invalid", 'error')
            return redirect(url_for('index'))
    else:
        club = session.get('club')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    clubs = loadClubs()
    competitions = loadCompetitions()

    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]

        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except IndexError:
        flash("The competition or club does not exist. Please try again.", 'error')
        return redirect(url_for('showSummary'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    clubs = loadClubs()
    competitions = loadCompetitions()

    try:
        competition_name = request.form['competition']
        club_name = request.form['club']
        places_input = request.form['places']

        # Recherche la compétition et le club dans la liste des compétitions et des clubs
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        # Vérifie si la compétition existe
        if competition is None:
            raise CompetitionNotFoundException()

        # Vérifie si la compétition est passée
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()

        if competition_date < current_date:
            raise CompetitionPassedException()

        # Vérifie si la compétition est complète
        if int(competition['numberOfPlaces']) <= 0:
            raise CompetitionFullException()

        # Vérifie si le champ "places" est vide, n'est pas un nombre ou est un nombre négatif
        if not places_input or not places_input.isdigit() or int(places_input) <= 0:
            raise InvalidPlacesException()

        placesRequired = int(places_input)

<<<<<<< HEAD
        # Convertie club['points'] et competition['numberOfPlaces'] en entiers
=======

        # Convertie club['points'] et competition['numberOfPlaces'] en entiers


        # Vérifier si l'utilisateur a suffisamment de points (maximum 12 athlètes)
        if placesRequired > 12:
            raise MaximumPlacesException()


        # Convertir club['points'] et competition['numberOfPlaces'] en entiers

>>>>>>> 1ff0293d6d1695bf7193cdd724dcf2332b1f5964
        club_points = int(club['points']) if club['points'] else 0
        competition_places = int(competition['numberOfPlaces']) if competition['numberOfPlaces'] else 0

        # Vérifie si l'utilisateur a suffisamment de points (1 point par inscription)
        if club_points < placesRequired:
            raise NotEnoughPointsException()

        # Vérifie si l'utilisateur tente de réserver plus de 12 athlètes
        if placesRequired > 12:
            raise MaximumPlacesException()

        # Effectue la réservation
        competition_places -= placesRequired
        club_points -= placesRequired

        # Mettre à jour les valeurs dans les dictionnaires
        competition['numberOfPlaces'] = str(competition_places)
        club['points'] = str(club_points)

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    except CompetitionNotFoundException:
        flash(CompetitionNotFoundException.flash_message, 'error')
        return redirect(url_for('index'))

    except CompetitionPassedException:
        flash(CompetitionPassedException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except CompetitionFullException:
        flash(CompetitionFullException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except InvalidPlacesException:
        flash(InvalidPlacesException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except MaximumPlacesException:
        flash(MaximumPlacesException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except NotEnoughPointsException:
        flash(NotEnoughPointsException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))


@app.route('/displayPointsClubs')
def display_points_clubs():
    clubs_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('points_table_clubs.html', clubs=clubs_list)


@app.route('/logout')
def logout():

    return redirect(url_for('index'))

    return redirect(url_for('index'))

