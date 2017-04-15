# maTex - Die "magische" Textkorrektur

--------------------------------------

maTex ist eine Software zur Bewertung von englischen Texten.
Die Benotung der Texte basiert auf einer Naiven Bayesschen Klassifikation, 
die mit verschiedenen Messgrößen eines Textes arbeitet.
Sie können den Bayesschen Klassifikator mithilfe von maTex selbst trainieren, 
wenn sie eigene Trainingsets besitzen.

Möchten sie Texte nur Bewerten, so empfehlen wir ihnen unsere [Webseite](http://matex.pythonanywhere.com/) zu benutzen.

Vorraussetzungen
----
* Ubuntu!
* Git (siehe Installation)
* Administratorrechte (bei automatischer Installation, bei manueller unter Umständen ebenfalls)
* bei älteren Versionen als 14.04 (Trusty) funktioniert die automatische installation nur, 
wenn sie Python3 zuvor manuell installiert haben. `sudo apt-get install python3`
* Oracle JDK 8 ist von Vorteil, kann aber auch automatisch installiert werden. 
(ab Ubuntu 15.10 Wily standardmäßig in Ubuntu integriert)
* Für die Installation empfehlen wir 8GB RAM oder mehr

Installation (Internetverbindung notwendig)
------------
#### I) Allgemein auszuführen

> 1: Git installieren (Administartorrechte benötigt)

    sudo apt-get install git

> 2: Archiv rekursiv(!) klonen

    git clone --recursive https://bitbucket.org/Nikch/matex.git

#### II) Automatische Installation mithilfe der setup.py (getestet mit Ubuntu 16.04)


> 3: `setup.py` mit python3 ausführen

    cd matex
    sudo python3 setup.py

> Die `setup.py` führt sie durch die Installation. Bestätigen sie das Installieren von Paketen, 
falls sie gefragt werden. Zusätzliche Features von SyntaxNet empfehlen wir abzulehnen.

>**Achtung:** Falls sie eine ältere Version als Ubuntu 15.10 (Wily) benutzen
und Java JDK 8 noch nicht installiert haben, fügen sie folgende Option hinzu:
    
    sudo python3 setup.py -installjdk8

#### III) Manuelle Installation (für Fortgeschrittene)

> 3: Wechseln sie in den folgenden Ordner:

    cd matex/textfeatures/parsing/
    
> Folgen sie nun [diesen](https://github.com/tensorflow/models/tree/master/syntaxnet#installation) 
Schritten um Syntaxnet von Google zu installieren. Installieren sie die dort aufgeführten 
python Pakete für ihre Python 2 Distribution! Installieren sie auch bazel!
**Achtung:** Überspringen sie das erneute klonen des Syntaxnet Archivs! (Den Befehl ` git clone `...) 
Kehren sie danach in den Ordner ` /parsing/ ` zurück.

> 4: Installieren sie die für maTex benötigten Pakete: (Installieren sie pip3, falls sie es nicht bereits installiert haben)

    sudo apt-get install enchant
    sudo apt-get install python3-pip
    pip3 install numpy
    pip3 install textstat
    pip3 install pyenchant  #sudo, falls es ohne nicht funktioniert
    pip3 install flask
    pip3 install textract
    pip3 install reportlab
    
> 5: Konfigurieren sie Syntaxnet zur Verwendung mit maTex indem sie die die Datei ` setup_parser.py ` ausführen:

    python3 setup_parser.py

> 6: Nun können sie die Datei `main.py` benutzen. Gehen sie dazu zurück in den Ordner `/matex/` .

    cd ../..

Nutzung
-------

Zur Nutzung des Programms muss die `main.py` aufgerufen werden.

    python3 main.py

Es kommt eine Eingabezeile in der sie die Möglichkeit haben folgende Befehle einzugeben:

>1: `training` : Hiermit können sie Anhand ihrer eigenen Datensets den Klassifikator trainieren.
Folgen sie danach den Programm.
>2: `validaton` : Hiermit können sie ein Datenset auf seine durchschnittliche Genauigkeit testen.
>3: `run` : Klassifizieren sie Texte mithilfe eines Profils ihrer Wahl.
>4: `profileinfo` : Damit können sie die Features und besten Features eines Profils ausgeben,
sowie die Genauigkeit des Profils.
>5: `script` : Damit können sie ein von ihnen erstelltes Script aus dem Ordner `Scripts` ausführen.
>6: `exit` : Zum Verlassen des Programmes.

Alternativ können sie auch die Funktion `-gui` benutzen:

    python3 main.py -gui
    
Damit wird die maTex Webseite auf ihrem Server gestartet.

Kontakt
-------

[Hier](http://matex.pythonanywhere.com/contact) kommen sie zu unserem Kontanktformular auf unserer Webseite

Entwickler
----------

**Julian Behringer** [*mailto*](mailto:behringer@phaenovum.de)

**Nikodem Kernbach** [*mailto*](mailto:kernbach@phaenovum.de)

**Raphael Kreft** [*mailto*](mailto:kreft@phaenovum.de)
