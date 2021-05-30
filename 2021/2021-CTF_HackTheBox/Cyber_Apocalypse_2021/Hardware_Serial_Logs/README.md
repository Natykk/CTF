# CTF HackTheBox 2021 Cyber Apocalypse 2021 - Serial Logs

Category: Hardware, Points: 300

We have gained physical access to the debugging interface of the Access Control System which is based on a Raspberry Pi-based IoT device. We believe that the log messages of this device contain valuable information of when our asset was abducted.

Attached file: 

# Serial Logs Solution

Premièrement on reçoit un fichier .sal avec une simple recherche google on ce rend compte les fichier .sal sont utilisé par le logiciel Logic 2 de Saleae. 

IMAGE 1_logic 


On peut voir qu un seul channel et utilisé pour faire passé des données donc on peut déjà en déduire que c'est en série et non en parallèle , si on ce renseigne sur les protocole de communication qui utilise 1-2 channel et qui son généralement utilisé par des microcontrôleur on tombe rapidement sur le protocole [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) alors analysons-le. Pour ce faire, nous devons d'abord connaître le débit en bauds, également connu sous le nom de vitesse de transfert. Sa mesure standard est le bit/s, donc pour calculer le débit en bauds de ce signal, nous faisons un zoom sur le tout premier signal et voyons la période minimale du signal.



IMAGE 2_baud



On pouvons voir que la plus petite période entre deux valeurs élevées est de 8,5us. Donc, si nous avons 1000000us (1 seconde) et qu'un bit est transféré toutes les 8.5us, nous pouvons calculer combien de bits/secondes est envoyés :

```
1 bit   1000000us
----- x --------- = 117.647,0588 bits/second
8.5us       1s
```
Maintenant si on prend la valeur standard la plus proche qui est 115200 et que l'on configure l'analyseur avec cette valeur dans le champ "baud rate" 

IMAGE 3_decode

Dans l'image suivante, on vois que Logic 2 a décodé correctement la communication et on peut voir les messages au dessus des signaux :  

IMAGE 3_message

Si l'on extract les données en CSV et que l'on range un peut le fichier on peut voir ceci 

```
...
[LOG] Connection from 316636cf0500c22f97fa261585b72a48c4625aca7868f0f6ee253937620ac15c
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[ERR] Noise detected in channel. Swithcing baud to backup value
î.ì~..ò.|`~.î|.....b..|.|....r.|...|pà|....âp..ppâp....âpp|..|..p..|..pp..|â.p..p......||.|..|..pp..|p.|àà|..pp.p...p.|..p..p.î.ì~..ò.|`~.î|.....b..|.|....r.|p.|..p|.p..|â.|p.|p.....|......|...pp..pr.p.à|p.|p.|..||pâ.|p.||.......|...|r..|â..|r.....|.î.ì~..ò.|`~.î|.....b..|.|....r.|à...âpp..pà.p|p..p......p...p|..|..................p..|.....à|â.p..|p..p.p..|p.|p
...
```
Si on regarde le dernier message lisible il est dit qu'il change le baud rate pour passer sur la valeur de backup , puis les messages ensuit sont illisible alors il nous suffit de recalculer le baud rate pour la section qui est actuellement illisible 

IMAGE 4_baud2

On peut voir que que la plus petite est de 13.48us donc 1000000 / 13.48 = 74183 bits/s , il n'y a pas de valeur standard proche donc on changer le baud rate par la valeur calculer et on re-export les données en CSV 

IMAGE 5_export

Et Voila ! 

```
[LOG] Connection from a7e6ec5bb39a554e97143d19d3bfa28a9bbef68fa6ecab3b3ef33919547278d4
[LOG] Connection from 099319f700d8d5f287387c81e6f20384c368a9de27f992f71c1de363c597afd4
[LOG] Connection from ab290d3a380f04c2f0db98f42d5b7adea2bd0723fa38e0621fb3d7c1c2808284
[LOG] Connection from CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}
[LOG] Connection from CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}
```

Flag : `CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}`

