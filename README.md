## TripTime

TripTime est un petit script ecrit un python permettant de remonter dans home assistant via sa rest api les temps de route des trajets paramétrés.  
Il est basé sur l'API de Google Maps et permet de récupérer les temps de trajet en voiture.

### Révisions

- 26/02/2025 - V1 - ok
- 10/02/2025 - V0.1 - Création du projet

### Pré-requis

1. Une cle api pour google maps (compte gmail requis + cb)
2. Une instance home assistante ouverte sur internet
3. Un pc/serveur/vps/nas, n'importe quoi pouvant executer python3 et connecté à internet pour executer le script.

### Installation

1. Renommer le fichier travels.sample.yaml en travels.yaml et ajouter vos trajets.
2. Renommer le fichier config.sample.yaml en config.yaml et ajouter votre clé API Google Maps, votre url Home Assistant ainsi que le Bearer d'authentification pour la rest api de home assistant.
3. Créer une ou plusieurs taches cron pour lancer le script main.py. (attention à la facturation google)
4. L'intégration des entités se fait automatiquement dans home assistant.

Supplément  
 5. Ajout d'automations dans home assistant. 
 6. Ajout d'un petit flux node red pour gérer l'affichage des temps de trajets sur ma matrice led le matin avant de partir.

### Cron

```bash
crontab -e
chmod +x launcher_arrosage.sh
sudo apt install dos2unix
dos2unix launcher_arrosage.sh
```

J'ai besoin de nouvelles données entre 7/8h le matin et vers 17h40 le soir.  

```bash
# du lundi au vendredi 7h00, 7h40, 17h45 et le lundi, mardi, jeudi vendredi à 8h10
0 7 * * 1-5 sh /home/nicolas/launcher_arrosage.sh
40 7 * * 1-5 sh /home/nicolas/launcher_arrosage.sh
10 8 * * 1,2,4,5 sh /home/nicolas/launcher_arrosage.sh
45 17 * * 1-5 sh /home/nicolas/launcher_arrosage.sh
```

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
