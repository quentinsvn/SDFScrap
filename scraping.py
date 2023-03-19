from pushbullet import PushBullet
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from selenium import webdriver
import time
import re
import smtplib
from email.message import EmailMessage
import sys
import subprocess
import requests
import json

VOTRE_ADRESSE_EMAIL = "" # Remplacer VOTRE_ADRESSE_EMAIL par votre adresse email
VOTRE_MOT_DE_PASSE_EMAIL = "" # Remplacer VOTRE_MOT_DE_PASSE_EMAIL par votre mot de passe email (attention, vous devez créer un mot de passe d'application pour votre compte Gmail)
URL_EVENEMENT = "" # Remplacer URL_EVENEMENT par l'URL de votre événement (par exemple https://exchange.stadefrance.com/selection/resale/item?performanceId=xxxxxxxxxxxxxx)
URL_DU_WEBHOOK_DISCORD = "" # Remplacer LIEN DU WEBHOOK DISCORD par votre URL de webhook Discord
PUSHBULLET_TOKEN = "" # Remplacer PUSHBULLET_TOKEN par votre token Pushbullet

# Connexion au serveur SMTP de Gmail pour envoyer des emails (ou un autre service SMTP)
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to  
    user = VOTRE_ADRESSE_EMAIL
    msg['from'] = user
    password = VOTRE_MOT_DE_PASSE_EMAIL
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def send_notification(file_content):

    # URL du webhook Discord
    DISCORD_WEBHOOK_URL = URL_DU_WEBHOOK_DISCORD

    # Créer le message à envoyer
    message = 'Nouveau billet(s) disponible(s) :\n\n{}'.format(file_content)

    # Créer un dictionnaire avec les données à envoyer dans la requête POST
    data = {
        "embeds": [
            {
                "title": "Nouveau(x) billet(s) disponible(s)",
                "description": message,
                "url": URL_EVENEMENT,
                "color": 5814783,
                "author": {
                    "name": "Stade de France"
                }
            }
        ],
        "attachments": []
    }

    json_message = json.dumps(data) # Convertir le dictionnaire en JSON

    # Envoie la requête POST au webhook Discord
    requests.post(DISCORD_WEBHOOK_URL, json=data)

    # Vérifie que la requête a été effectuée avec succès
    # if response.status_code != 204:
    #     print('Erreur lors de l\'envoi de la notification Discord')

# Configure le navigateur pour qu'il ouvre la page que vous souhaitez scrapper
url = URL_EVENEMENT 

# Configure le navigateur pour qu'il se lance dans le mode "headless" (sans interface graphique)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Si vous êtes sous Mac OS X, exécutez la commande "caffeinate" pour empêcher l'ordinateur de se mettre en veille
if 'darwin' in sys.platform:
    print('Mac OS X détecté, activation de caffeinate...')
    subprocess.Popen('caffeinate')


# Boucle infinie pour du scrapping continu
while True:
    # Ouvrir la page web dans le navigateur
    driver.get(url)

    # Attendre quelques secondes que la page se charge complètement
    time.sleep(5)

    # Éxécution du code JavaScript pour extraire les éléments chargés en JS
    js_code = """
        var categories = document.querySelectorAll("table tr td:nth-child(1)");
        var places = document.querySelectorAll("table tr td:nth-child(3)");
        var results = [];

        for (var i = 0; i < categories.length; i++) {
            results.push("Catégorie : " + categories[i].innerText);
        }

        for (var i = 0; i < places.length; i++) {
            results.push("Place : " + places[i].innerText);
        }

        results = results.filter(function(item) {
            return item !== "Catégorie : " && item !== "Place : ";
        });


        return results;
    """
    js_results = driver.execute_script(js_code)

    # Écriture des résultats dans un fichier texte
    with open("tickets/tickets.txt", "w") as js_file:
        js_file.write("\n".join(js_results))

    # Lire le contenu du fichier et vérifier si le mot clé est présent
    with open('tickets/tickets.txt', 'r') as f:
        content = f.read()

    # Lire le contenu du fichier et vérifier si le mot clé est présent par rapport à la dernière vérification
    with open('tickets/tickets_old.txt', 'r') as f:
        backup = f.read()

    # Lire le contenu du fichier et vérifier si le mot clé est présent (par exemple ici nous recherchons un billet en catégorie "OR")
    # Si le mot clé est présent, on envoie une notification PushBullet et un email
    if re.search(r'\bOR\b', content):
        email_alert("Nouveau(s) billet(s) disponible(s)", "Voici la liste du ou des nouveau(x) billet(s) disponible(s) :\n\n{}".format(content), VOTRE_ADRESSE_EMAIL) # Remplacer VOTRE_ADRESSE_EMAIL par votre adresse email
        send_notification(content)

    if content != backup:
        access_token = PUSHBULLET_TOKEN

        print("Nouveau(x) billet(s) disponible(s) !")

        # Connexion à l'API PushBullet
        pb = PushBullet(access_token)
        
        # Envoi d'une notification PushBullet
        push = pb.push_note("Nouveau(x) billet(s) disponible(s)", "Voici la liste du ou des nouveau(x) billet(s) disponible(s) :\n\n{}".format(content))

        send_notification(content) # Envoi d'une notification Discord
        email_alert("Nouveau(x) billet(s) disponible(s)", "Voici la liste du ou des nouveau(x) billet(s) disponible(s) :\n\n{}".format(content), VOTRE_ADRESSE_EMAIL) # Envoi d'un email
        with open('tickets/tickets_old.txt', 'w') as f:
            f.write(content) # Écriture du nouveau contenu dans le fichier de sauvegarde
    else:
        print("Pas de nouveau(x) billet(s) disponible(s) pour le moment...") # Affichage dans la console si aucun nouveau billet n'est disponible

    # Temps de rafraîchissement avant de scrapper à nouveau la page
    time.sleep(300) # 300 secondes = 5 minutes

# Fermer le navigateur à la fin du programme
driver.quit()
