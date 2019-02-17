############################## IDEA ##############################
Simulation of Casimir (cognitive model to describe human spatial knowledge processing),
which was described by Schultheis, H. & Barkowsky, T. in 2011 in the paper:
Casimir: An Architecture for Mental Spatial Knowledge Processing

##################### Background Information #####################
In project-paper.pdf the background to that project is described.

##################### Preparations #####################
- python3 is needed
- install numpy
- install flask
- install flask_restplus

- install node js
- run npm install in casimir-web folder in order to download needed npm modules

##################### Starting the Simulation #####################
In order to let the simulation run:
- navigate to Casimir folder
- python CasimirSimulation.py
- navigate to casimir-web folder
- npm start
- open localhost:3000 in browser

######################## Important Notes ########################
If the error "No 'Access-Control-Allow-Origin' header is present on the requested resource.
Origin 'http://localhost:3000' is therefore not allowed access" comes up:
Make sure to turn off CORS in the browser

######################## Not needed files ########################
The Model*.py files, were implemented to let the simulation run with different settings.
They are not needed for the actual implementation

######################### Important Links #########################
URL to Github: https://github.com/montezuma93/Casimir

URL to Travis: https://travis-ci.org/montezuma93/Casimir

URL to SonarCloud https://sonarcloud.io/dashboard?id=montezuma93_Casimir
