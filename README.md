# UFOs sighting reports worldwide

## Table of Contents

* [About the Project](#about_the_project)
  * [Built With](#built_with)
* [Web Application](#web_app)
  * [Installation](#installation)
  * [Lauching the app](#launch_app)
* [Notebook](#nootebook)
* [Usage](#usage)
* [Contact](#contact)

<br>

## About the Project
This repository contains our final work for the 2nd year Computer Science Project class at ENSAE (Institut Polytechnique de Paris).

In this repository, you will find:
* A notebook (.ipynb), explaining in more depth our data cleaning/wrangling and modeling approaches. This notebook contains some of our results, but the results will also be found in our webapp (please see below).
* Some modules (.py), containing the functions we created and used during our data analysis, modeling, and visualization.

The underlying data comes from a [public website](https://www.mavenanalytics.io/data-playground).

We would also like to thank our Python class teachers, C.Laroche and L.Galiana, for the support and knowledge they gave us.

Please feel free to contact us if you would like to share your opinions/comments on our work.

### Built with

* [Python](https://python.org)
* [Streamlit](https://streamlit.io)
* [Bootstrap](https://getbootstrap.com)
* [GeoPy](https://geopy.readthedocs.io)
* [Folium](https://folium.readthedocs.io)
* [Wordcloud](https://pypi.org/project/wordcloud/)

<br>

<!-- WEB APPLICATION -->
## Web Application

### Installation

1. Clone the repository
```sh
git clone https://github.com/JulesBrable/UFO.git
```
2. Install required libraries
```sh
pip install -r requirements.txt
```

### Launching the app

Once the installation is complete, you can start the application either:

* Using the command line:
```sh
streamlit run ./UFOs_cartography.py
```

* Directly on Streamlit Cloud: https://julesbrable-ufo-ufos-cartography-b7h718.streamlit.app

### Usage

We chose to developp a web application using [Streamlit](https://streamlit.io), which is open-source and user-friendly Python framework. We made the app interface as simple as possible, while keeping a certain level of personalization. Indeed, the main idea of this application is to allow flexibility and scalability for anyone interested in discovering the origin of UFO sightings and finding resources to reflect on the causes of these reports. We deployed our app on [Streamlit Cloud](https://streamlit.io/cloud), which is free access.
When the application is launched, the user must make choices from a number of filters. Then, he will submit his entries and can observe the corresponding results. He can freely navigate between the different panels of the application, according to his interest.

<br>

## Notebook


<br>

## Contact

* [Jules Brablé⛑](https://github.com/JulesBrable) - jules.brable@ensae.fr
* [Antonio Sasaki👑](https://github.com/antoniosasaki) - antonio.sasaki@ensae.fr
* [Oumar Dione🎩](https://github.com/Oumar-DIONE) - oumar.dione@ensae.fr
