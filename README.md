## TripTime

TripTime est un petit script ecrit un python permettant de remonter dans home assistant via sa rest api les temps de route des trajets paramétrés.  
Il est basé sur l'API de Google Maps et permet de récupérer les temps de trajet en voiture.

### Révisions

 - 10/02/2025 - V0.1 - Création du projet

### Pré-requis

1. Une cle api pour google maps
2. Une instance home assistante ouverte sur internet
3. Un pc/serveur pour executer le code python

### Installation

 1. Renommer le fichier travels.sample.yaml en travels.yaml et ajouter vos trajets.
 2. Renommer le fichier config.sample.yaml en config.yaml et ajouter votre clé API Google Maps, votre url Home Assistant ainsi que le Bearer d'authentification pour la rest api de home assistant.
 3. Créer une ou plusieurs taches cron pour lancer le script main.py. (attention à la facturation google)
 4. L'intégration des entités se fait automatiquement dans home assistant.
 5. Ajout d'automations dans home assistant. 
 6. Ajout d'un petit flux node red pour gérer l'affichage des temps de trajets sur ma matrice led le matin avant de partir.

### Automations

#### Exemple d'automation dans home assistant :

```yaml
alias: Notifier TripTime Work -> Home
description: ""
triggers:
  - trigger: time
    at: "17:50:00"
conditions:
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
  - condition: state
    entity_id: input_select.planning_nicolas
    state: Travail
actions:
  - action: notify.mobile_app_iphone_de_nicolas
    metadata: {}
    data:
      title: 🚗 Travail -> Maison @ {{now().strftime('%H:%M')}}
      message: >-
        {% set t = states('sensor.triptime_work_home') | int %} {% if t < 25
        %}🚀{% elif t <= 35 %}😐{% else %}😡{% endif %} Temps de trajet estimé
        -> {{ t }} minutes
mode: single
```


