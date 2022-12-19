# Studies of UFOs sighting reports worldwide

## Table of Contents

* [About the Project](#about_the_project)
* [Problematic](#prob)
* [Web Application](#web_app)
  * [Installation](#installation)
  * [Lauching the app](#launch_app)
  * [Usage](#usage)
* [Contact](#contact)

<br>

## About the Project
This repository contains our final work for the 2nd year Computer Science Project class at ENSAE (Institut Polytechnique de Paris).

In this repository, you will find the following files:
* A notebook (.ipynb), explaining in more depth our data cleaning/wrangling and modeling approaches. This notebook contains some of our results, but the results will also be found in our webapp (please see below), especially with regards to the data visualization.
* Some modules (.py), containing the functions we created and used during our data analysis, modeling, and visualization; and the scripts used for building our web application.

If you want to run the notebook from your computer, you will need to clone this repository (see below for the corresponding command line instruction).

The underlying data comes from a [public website](https://www.mavenanalytics.io/data-playground). We also used webscrapping to obtain additional components that were missing from the original dataset.

We would also like to thank our Python class teachers, C.Laroche and L.Galiana, for the support and knowledge they gave us.

<br>

## Problematic
UFOs have been the source of many stories and legends for hundreds of years. They make us wonder if we humans are alone in the universe. This question is inherent to humans, because by nature, human beings can be curious and fascinated by the unknown.

Furthermore, when a person thinks he or she sees something unknown in the sky, there are two options: either it is explainable (on scientific or logical grounds), or it is not (in which case it is a UFO (?)). However, a person's judgment to recognize and identify whether what he or she has seen is or is not unknown can be altered by many factors, for example: cognitive bias, geographic context, or temporal context. The main issue for us has been to identify some explanations for the reports of UFO sightings around the world from the begining of the 20th century to 2014, and to identify some clusters between the US states.

Finally, we also aimed at creating a visualization tool for these reports, by coding a Web Application.

<br>

<!-- WEB APP -->
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

## Contact

* [Jules Brablé⛑](https://github.com/JulesBrable) - jules.brable@ensae.fr
* [Antonio Sasaki👑](https://github.com/antoniosasaki) - antonio.sasaki@ensae.fr
* [Oumar Dione🎩](https://github.com/Oumar-DIONE) - oumar.dione@ensae.fr
