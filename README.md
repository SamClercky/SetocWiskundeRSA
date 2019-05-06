# Setoc Wiskunde
Al deze code is onderdeel van een onderzoeksopdracht voor het vak Wiskunde.
De code is ter ondersteuning van het onderzoek en de complete code kan hier
dus worden gevonden en is gebaseerd op de code van [deze repo]("https://github.com/sybrenstuvel/python-rsa")
## Installatie
Om de code ten volle te kunnen gebruiken, is het aangeraden om
[python 3]("https://www.python.org/downloads/") te hebben
geïnstalleerd samen met [python-rsa]("https://github.com/sybrenstuvel/python-rsa").

Met pip3: `$ pip3 install rsa`

## Gebruik
Deze code is geschreven met python 3 en verwacht dit ook op de hostcomputer.
Het bestand `functions.py` bevat alle code omtrend de brute force techniek.
Het bestand `algo2.py` bevat alle code omtrend de tweede oplossing.

Om `algo2.py` het best via een terminal te kunnen uittesten, heb je het bestand
`setup_vars.py`.
``` python3
>>> import setup_vars as sv
>>> sv.reset(32)  # Maak een sleutel aan met python-rsa
>>> sv.start_all(4)  # Start met zoeken met 4 threads
...
[*] Gevonden resultaat 197 # Voorbeeld uitkomst
...
```

## Disclaimer
Ik heb niets te maken met `python-rsa`, noch heb ik hier financiële voordelen
bij. Dit is project heeft puur een educatief doeleind als eindproject
voor het vak Wiskunde.