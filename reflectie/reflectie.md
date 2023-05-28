# Reflectie Python project

Voor het vak Python Development heb ik een Trojan application gemaakt. Deze Trojan werkt via Github. De Trojan zal gebruikt worden voor verschillende doeleinden. Zijnde het verkrijgen van systeeminformatie, het maken va nscreenshots, het verzamelen van keystrokes met behulp van een keylogger, het afspelen van een geluidje en het binnenkrijgen van WiFi passwords.

## Werking

Het project werkt via Github. Via Github worden dus commando's in een bestand (config.txt) geplaatst. het main.py script zal altijd blijven draaien en om de 120 seconden kijken of er een commando in de file staat. Als in dit bestand bijvoorbeeld het woord 'sysinfo' geplaatst wordt, zal main.py de gehele repo pullen en de 'sysinfo' module vervolgens uitvoeren. Na het uitvoeren van de gevraagde modules zal het programma de resultaten pushen naar Github. We zien deze resultaten vervolgens op Github verschijnen.

## Features

Het programma heeft verschillende features. De belangrijkste zijn dat het programma aanstuurbaar is via Github, dat er meerdere modules beschikbaar zijn en dat nieuwe modules makkelijk toegevoegd kunnen worden. Encryptie heb ik proberen toevoegen maar dit is uiteindelijk niet gelukt.

## Keuzes

Binnen dit project heb ik ook regelmatig gebruik gemaakt van bepaalde libraries. De externe libraries die ik gebruikt heb zijn pynput voor de keylogger, playsound voor de play_sound module, pyautogui voor de screenshot module en psutil voor de sysinfo module.

## Moeilijkheden en problemen

In het project heb ik logischerwijs ook enkel moeilijkheden gehad. Ik had bijvoorbeeld een probleem bij het werken met Github. Als eerste had ik een implementatie waarbij ik via requests de inhoud van de raw view van een script ging opvragen en deze dan in een nieuw bestandje plaatsen. Dit werkte en zo kon ik 1 enkel bestand binnenhalen, alleen werd het dan wel heel lastig om de repo terug te pushen met de resultaten.

Ook heb ik last gehad met de encryptie van de modules. Ik heb hier de Fernet library voor gebruikt maar dit was helaas zonder resultaat.