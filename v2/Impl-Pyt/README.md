# Medha-on-Board

Project Medha is a rover that can move around for exploring the universe around it. The rover collects the information related to weather, environment and other information. The end goal of Project Medha is to make the rover fully autonomous and consider it like a team-member.

The basic idea is that when we go around for exploration(like say star-gazing), the rover will roam around get the information of the surroundings. It just not that, the rover will itself keep exploring on it's reachable places (like in home, apartment areas, parks, etc.) to collect data and information. Medha is short for Project-Medha

## MEDHA on-board processing

- The framework code for Medha on-board and modules required to start and process on-board computations like reading-sensors, controlling local-movement, etc.
- There are two implementations:
    -   **Impl-Pyt**: python implementation for the framework.
    -   **others**: in the road map. Not implemented yet.

## Config files

- v2/Imple-Pyt/Config
    -   **properties.json**: configurations related to system and connections.
    -   **values.ini**: contains values such as duration, time and other configurable properties.
    -   **SCHEMA_properties.json**: schema file to validate properties.json

## Starting the system

To start the system, make sure configurations are correct and simple run the below start command:

    python start-medha.py

**Note**:

-   make sure to check install dependencies listed in requirements.txt
-   create virtual env before proceeding with global env or shared env.