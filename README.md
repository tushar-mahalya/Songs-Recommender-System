# Songs Recommender System

[![Repo Size](https://img.shields.io/github/repo-size/tushar-mahalya/Songs-Recommender-System?style=flat-square)](https://github.com/tushar-mahalya/Songs-Recommender-System)  ![License](https://img.shields.io/badge/license-MIT-red.svg)  ![Project Status](https://img.shields.io/badge/status-Completed-brightgreen.svg)  [![streamlit-ext-demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://songs-recommendation-system.streamlit.app/)

## Getting started
To use the application, you can visit the live version hosted on the following URL:

   `https://songs-recommendation-system.streamlit.app/`
    
Alternatively, you can run the application on your local machine by following the steps below:

1. Clone the repository to your local machine by running the following command:  

		git clone https://github.com/tushar-mahalya/Songs-Recommender-System.git
    
2. Install the necessary dependencies by running the following command:

		pip install -r requirements.txt

3. Start the Streamlit application by running the following command:

		streamlit run app.py
    
4. Open your web browser and navigate to the following URL:

		http://localhost:8501/

## Introduction
In immersive exploration into the evolving landscape of music preferences, our objective is to build a robust system that encompasses a wide range of functionalities, using a combination of data acquisition, exploratory data analysis, content-based recommendation algorithms, and user interface development.

* ### Data Acquisition and Processing
To kickstart our project, we leverage web scraping techniques and the Spotify API to gather metadata, audio features data, and lyrics of Billboard Hot 100 (BBHOT100) tracks spanning 77 years, from 1946 to 2022. This meticulous data collection process ensures a comprehensive and rich dataset for our analysis and recommendation system.
* ### Exploratory Data Analysis
Harnessing the power of business intelligence tools, specifically Tableau, we conduct extensive exploratory data analysis on the processed BBHOT100 dataset. This analysis aims to derive valuable insights into the evolution of music preferences over time. By examining trends, patterns, and correlations within the data, we uncover the shifting dynamics of musical tastes and understand the factors that influence popularity.
* ### Content-Based Recommendation System
Building upon the insights gained from our exploratory analysis, we develop a content-based music recommendation system. By extracting audio features from each song in the dataset, we employ sophisticated algorithms to identify similarities and patterns. This enables us to offer personalized song recommendations to users based on their individual preferences. Our system empowers users to discover new music that aligns with their taste, similar to the acclaimed Spotify recommendation engine.
* ### Advanced Analytics
In addition to our recommendation system, we have developed an analytical engine that further enhances the understanding of music and artists. Our engine utilizes PizzaPlot, a specialized visualization tool, to present the audio features of user selected songs in an easily digestible format. We also analyze the popularity of specific artists, providing insights into their reach and influence with respect to time. Furthermore, we visualize the mean percentile rank of artists and genres, allowing users to gauge the relative standing of certain attributes.
* ### User Interface Development
Delivering a seamless user experience is paramount to our project. With a focus on user-centric design, we craft an intuitive and visually appealing user interface (UI) that emulates the familiar aesthetics of the Spotify platform. Utilizing Streamlit, a powerful web application framework, we build an interactive frontend that seamlessly integrates with our recommendation system. The result is a user-friendly and engaging interface that facilitates effortless music exploration and discovery.
* ### Deployment on Streamlit Cloud
To ensure widespread accessibility, we deploy our song recommender system on Streamlit Cloud. Leveraging the scalability and availability of cloud computing, our system becomes easily accessible to users worldwide via a web browser. This deployment allows music enthusiasts to enjoy personalized recommendations and explore the evolution of music preferences at their convenience.

## Features
* ### Recommender Engine
![Recommneder Engine Demo video](resources/Gifs/recommendations.gif)
Our application utilizes a comprehensive algorithm to provide users with tailored music recommendations based on their selected 5-10 songs. By analyzing the audio features, key, time signature, subjectivity, and polarity of the song titles (measured using TextBlob), as well as the genre of the artist, we generate a list of 20 songs that closely align with the user's preferences. To further enhance the user experience, we present a PizzaPlot visualization, showcasing the distribution of audio features of the selected songs. This visual representation helps users understand the characteristics of their chosen songs and how they relate to the recommended tracks. To ensure a seamless listening experience, each recommended song is accompanied by a Spotify link, allowing users to effortlessly explore and enjoy the suggested music.  
* ### Analytical Engine
 <div style="display: flex; justify-content: center;">
  <div style="flex: 1; padding: 10px; text-align: center;">
    <p>Artist Profile</p>
    <img src="resources/Gifs/artist_profile.gif" alt="Analytical Engine demo for Artist" style="max-width: 100%; height: auto;" />
  </div>
  <div style="flex: 1; padding: 10px; text-align: center;">
    <p>Genre Profile</p>
    <img src="resources/Gifs/genre_profile.gif" alt="Analytical Engine demo for Genre" style="max-width: 100%; height: auto;" />
  </div>
</div>


* ### Themed Playlists
![Playlisting Demo video](resources/Gifs/playlist.gif)
In addition to the personalized song recommendations, our application goes a step further by curating five themed playlists based on the user's mood. Each playlist is meticulously crafted to cater to the user's preferences, leveraging the characteristics of their selected songs. These playlists exhibit specific audio features that are dominant within them, ensuring a cohesive and immersive musical experience. Let's delve into the details of each playlist:

  1. <u>Trending Songs</u> : By prioritizing the 'popularity' factor, we ensure that users stay up-to-date with the latest music trends and discover the hottest hits in real-time.

  2. <u>Dance Party</u> : Designed for those looking to groove and let loose, this playlist emphasizes the highest 'Danceability' factor.

  3. <u>Monday Blues</u> : Intended to counteract the notorious Monday blues, this playlist is curated with songs that possess the lowest 'Valence' factor.

  4. <u>Energizing</u> : Perfect for workouts or moments when an extra boost of energy is needed, this playlist highlights songs with the highest 'Energy' factor.

  5. <u>Positive Vibes</u> : For those seeking an uplifting and optimistic musical experience, this playlist focuses on songs with the highest 'Valence' factor.

## Hardware Specification

For this project I've used [Amazon Sagemaker Studio Lab](https://studiolab.sagemaker.aws/) EC2-Instance which have the following specs -

| Component | Specification |
| --- | --- |
| CPU | Intel® Xeon® Platinum 8259CL |
| Architecture | x86_64 |
| RAM | 16GB |
| Storage | 15GB (AWS S3 Bucket) |
| GPU | NVIDIA® Tesla T4 |
| CUDA Version | 11.4 |
| V-RAM | 15GB |


## Contributing

If you would like to contribute to the project, you can follow the steps below:

1. Fork the repository to your GitHub account.
2. Clone the repository to your local machine.
3. Create a new branch for your changes.
4. Make your changes to the codebase.
5. Push your changes to your forked repository.
6. Create a pull request from your forked repository to the original repository.

## License

This project is licensed under the MIT License. You are free to use, modify and distribute the code as per the license terms.
