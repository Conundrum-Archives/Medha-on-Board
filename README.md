# Medha-on-Board

Project Medha is a rover that can move around for exploring the universe around it. The rover collects the information related to weather, environment and other information. The end goal of Project Medha is to make the rover fully autonomous and consider it like a team-member.

The basic idea is that when we go around for exploration(like say star-gazing), the rover will roam around get the information of the surroundings. It just not that, the rover will itself keep exploring on it's reachable places (like in home, apartment areas, parks, etc.) to collect data and information. Medha is short for Project-Medha

## MEDHA on-board processing

- This repo consist the code-base and modules required to start and process on-board computations like reading-sensors, controlling local-movement, etc.
- The folders are classified and are self explanatory.
  * rpi (the folder where all rpi based modules go)
    - **localization**: directory containing modules for local actions like reading sensors, direction based decisions and so on.
    - **tasks**: directory containing modules for specific category of actions like healthchecks, basci checks, etc.
    - **utils**: directory containing utility modules for logging, reading configurations and other utility based modules.
    - **pins.json**: configuration file to setup pin number against pins used on board.
    - **properties.json**: configuration file to define the basic properties which includes mock settings, communication settings and Medh identity.
    - **start-medha.py**: the very first file which will be executed. The start file of the project.
  - prototypes (the folder where all prototypes, experimental scripts are placed). (Note that scripts and code in this folder may not be stable and retained longer)


## Setting up environment
* Setting up medha-on-board is very easy.
  - clone this repo using ```git clone https://github.com/Conundrum-Archives/Medha-on-Board```
  - change the branch name you want to setup using ```git checkout -b -branch-name- ; git pull origin -branch-name-```
  - run ```pip install -r requirements.txt``` to install dependencies.
  - set the relevant configuration in properties.json and pins.json file.
  - NOTE: set ```isMock: True``` in properties.json file if you want to run/work as mock ie., without actual device.
  - run the command: ```python -module-name.py``` (for main program run: ```python start-medha.py```)

* Configurations:
  - properties.json: setup relevant configuration related to **MQTT**, **NodeID**, etc
  - pins.json: assign pin numbers for **Motors**, **Sensors**, etc

* Dependencies:
  - requirements.txt: file consist of all required dependencies / libraries used within project.
  - run ```pip install -r requirements.txt``` to install dependencies.

**preferably run in a virtual environment to avoid installing all libraries globally**


### Who do I talk to? ###

* reach out to admin of the repo or handlers of repo in any confusions or anything related to this repo.
* teams and other contributors for any things related to code/code-logic.

## Happy Exploring!
