# SDFScrap

![Interface console](https://media.discordapp.net/attachments/345949387769249793/1087022462904045629/consolev2.png?width=2910&height=1692)

## Description
Script de scrapping permettant d'accéder aux billets disponibles d'un événement depuis la bourse du Stade de France avec la possibilité de recevoir des notifications sur son téléphone, par e-mail ou via Discord.

## Prérequis 

- Python 3
- Pip
-- pushbullet.py
-- pywebio
-- selenium
- PushBullet
- Chromium

## Mise en route 

Afin de faire fonctionner le script python veuillez suivre les étapes suivantes :

### Variables

Le script comporte plusieurs variables à modifier dont voici les détails :

| Variable  | Description          |
| :--------------- |:---------------|
| VOTRE_ADRESSE_EMAIL  | Adresse e-mail pour recevoir les notifications       |
| VOTRE_MOT_DE_PASSE_EMAIL  | Mot de passe de votre compte de messagerie. Si vous utilisez Gmail, assurez-vous de créer un mot de passe d'application pour que cela fonctionne correctement.             |
| URL_DU_WEBHOOK_DISCORD  | URL de votre WebHook Discord.          |
| PUSHBULLET_TOKEN  | Token  de votre compte PushBullet        |

### Modules

Afin de pouvoir installer les différents modules Python du programme, veuillez exécuter la commande suivante le terminal de votre machine :

```console
pip install -r requirements.txt
```

### Lancer le programme

Une fois les précédentes étapes effectuées, veuillez exécuter la commande depuis votre terminal :

```console
python3 scraping.py
```

Désormais, vous devriez être en capacité de recevoir des notifications depuis votre téléphone, par e-mail ou via Discord dès le moment ou un nouveau billet est disponible sur le site de la bourse du Stade de France !

## Screens

![Interface console](https://media.discordapp.net/attachments/345949387769249793/1087022462904045629/consolev2.png?width=2910&height=1692)

![Notif Discord](https://media.discordapp.net/attachments/345949387769249793/1087022886277107813/Capture_decran_2023-03-19_a_15.39.50.png?width=3840&height=1554)

![Notifs PushBullet](https://media.discordapp.net/attachments/345949387769249793/1087022796519002152/Screenshot_20230319-154015_Pushbullet.jpg?width=822&height=1689)
