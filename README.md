## Description
Boîte de surveillance industrielle collectant des données de capteurs (température, humidité et de son) via un Raspberry Pi 4 sous Linux. 
Les données sont traitées avec ROS, stockées dans une base SQLite, et visualisées sur un tableau de bord web Flask.

## Structure du projet
- `/docs` : Documentation technique, rapports LaTeX.
- `/src/acquisition` : Scripts Python (Capteurs).
- `/src/ros_ws` : Workspace ROS (Communication & Traitement).
- `/src/database` : Schéma SQLite et scripts (Les donnees).
- `/src/web_app` : Application web Flask.
- `/tests` : les Tests.
- `/config` : Fichiers de configuration réseau/sécurité.
