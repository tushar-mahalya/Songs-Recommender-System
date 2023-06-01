# --- IMPORTING DEPENDENCIES ---

import json
import pandas as pd
import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, FontManager
import streamlit.components.v1 as components
from src.plotUtils import getFeaturePercentiles, getMoodPlaylist
from src.plotUtils import format_song_name, format_artist_name

# ---------------------------------------------------------------------------------------------- #
# --- DEFINING PLOTTING FUNCTIONS ---

spotifyGreen = '#1dda63'
bg_color_cas = "#000000"
grey = "#979797"
lightgrey = "#bdbdbd"

robotoBold = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamBold.ttf')
robotoMed = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamMedium.ttf')


def plotPizza(values):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']
    slice_colors = [spotifyGreen] * 9
    text_colors = ["w"] * 9

    # Instantiate PyPizza class
    baker = PyPizza(
        params=featColumns,
        background_color='#000000',
        straight_line_color=grey,
        straight_line_lw=2,
        straight_line_ls='-',
        last_circle_color=grey,
        last_circle_lw=7,
        last_circle_ls='-',
        other_circle_lw=2,
        other_circle_color=lightgrey,
        other_circle_ls='--',
        inner_circle_size=20
    )

    # Plot pizza
    fig, ax = baker.make_pizza(
        values,
        figsize=(8, 8),
        color_blank_space=["k"] * 9,
        slice_colors=slice_colors,
        value_bck_colors=slice_colors,
        param_location=115,
        blank_alpha=1,
        kwargs_slices=dict(edgecolor="w", zorder=2, linewidth=2, alpha=.8, linestyle='-'),
        kwargs_params=dict(color="w", fontsize=22, fontweight='bold',
                           va="center", fontproperties=robotoMed.prop),
        kwargs_values=dict(color="k", fontsize=18, va='center',
                           zorder=3, fontproperties=robotoMed.prop,
                           bbox=dict(edgecolor="k", boxstyle="round,pad=0.2", lw=1.5))
    )

    ax.patch.set_facecolor('None')
    fig.set_alpha = 0.0
    fig.patch.set_visible(False)

    return fig


def plotHitProfile(feat_dict):
    mpl.rc('axes', edgecolor=grey)
    mpl.rc('axes', linewidth='2')

    fig, ax = plt.subplots(figsize=(8, 6))

    # Adding bg color and setting the grid
    fig.set_facecolor(bg_color_cas)
    ax.set_facecolor('k')
    ax.set_axisbelow(True)
    ax.grid(color=lightgrey, which='major', linestyle='--', alpha=1)

    years = list(map(int, list(feat_dict.keys())))
    hit_quality = list(map(float, list(feat_dict.values())))

    # Plotting
    ax.plot(years, hit_quality, '-', color=spotifyGreen, lw=4)

    # Setting the limits for x and y axes
    minYear = int(list(year for year in feat_dict if feat_dict[year] > 0)[0])
    maxYear = max(years) + 1  # Add a buffer of 1 to the maximum year
    ax.set_xlim([minYear, maxYear])

    # Setting the x-axis ticks
    num_ticks = 10  # Number of ticks on the x-axis
    tick_step = (maxYear - minYear) / (num_ticks - 1)  # Calculate the tick step
    x_ticks = [int(minYear + i * tick_step) for i in range(num_ticks)]  # Generate the ticks
    ax.set_xticks(x_ticks)

    ax.set_xlabel('Year', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='w')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='w')
    # Customizing the x and y ticklabels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    ax.tick_params(axis='both', which='major', labelcolor='w', length=0, color='#2b2b2b')

    return fig

# ---------------------------------------------------------------------------------------------- #
# --- PAGE CONFIGURATION ---

st.set_page_config(page_title="Music Recommender System", page_icon=":notes:", layout="wide")


# ---------------------------------------------------------------------------------------------- #
# --- LOADING REQUIRED DATAFRAMES ---
@st.cache_data
def load_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df


@st.cache_data
def load_json(json_file_path):
    with open(json_file_path, "r") as file:
        dict_file = json.load(file)
    return dict_file

def upload_data(df, name):
    df.to_csv(f'artifacts/{name}.csv', index=False)


main_data_path = "artifacts/[Songs]_Preprocessed_Data.csv"
ohe_data_path = 'artifacts/[OHE]_Artist_Genre.csv'
hit_profile_path = 'artifacts/Artists_&_Genres_Hit_Profile.json'

df = load_csv(main_data_path)
artist_genre_ohe_df = load_csv(ohe_data_path)
hit_profile = load_json(hit_profile_path)
artists = hit_profile['Artist'].keys()
genres = hit_profile['Genre'].keys()

# ---------------------------------------------------------------------------------------------- #
# --- Initializing Recommender System ---

from src.pipeline.recommender_engine import RecommenderEngine

rec_sys = RecommenderEngine()

# ---------------------------------------------------------------------------------------------- #
# --- LINKS FOR REQUIRED ANIMATION AND IMAGES ---

# animation html scripts
spotify_animation_html = """
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<lottie-player src="https://assets10.lottiefiles.com/packages/lf20_a6hjf7nd.json"  background="transparent"  speed="1"  style="width: 105px; height: 105px;"  loop  autoplay></lottie-player> """
astro_animation_html = """
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<lottie-player src="https://assets4.lottiefiles.com/packages/lf20_euaveaxu.json"  background="transparent"  speed="1"  style="width: 170px; height: 160px;"  loop  autoplay></lottie-player> """

# static images
spotify_logo = "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"
casette = 'https://www.scdn.co/i/500/cassette.svg'

# ---------------------------------------------------------------------------------------------- #
# --- WEBPAGE LAYOUT & WIDGET CODE ---

# Removing the Hamberger menu
hide_menu_style = """<style> #MainMenu {visibility: hidden;}
header {visibility: hidden;}</style>"""

st.markdown(hide_menu_style, unsafe_allow_html=True)

# Removing whitespace from the top of the page
st.markdown("""
<style>
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
    }
</style>""", unsafe_allow_html=True)

# Button config
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ffffff;
    color:#000000;
    }
div.stButton > button:hover {
    background-color: #1DDA63;
    color:#FFFFFF;
    }
</style>""", unsafe_allow_html=True)

# Select widget config
s_box = st.markdown("""
<style>
div[data-baseweb="select"] > div {
	background-color: #000000;
    color:#ffffff;
    }
</style>""", unsafe_allow_html=True)


# Setting background
page_bg = """
<style>
[data-testid="stAppViewContainer"]{
    background-color: #000000;
    color: #ffffff;
    background-repeat: no-repeat;
    background-position: left;
	}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title and intro Heading
heading_animation = "<p style = 'font-size: 60px;'><b>Spotify Music Recommendation System</b></p>"

# ---------------------------------------------------------------------------------------------- #
# --- GITHUB CORNER WIDGET ---

st.markdown("""
<a href="https://github.com/tushar-mahalya/Songs-Recommender-System" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#fff; color:#151513; position: absolute; top: -85; border: 0; right: -80;" aria-hidden="false"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a>""", unsafe_allow_html=True)

st.markdown("""
<style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------- #
# --- HEADING SECTION ---

with st.container():
    left_col, right_col = st.columns([1, 9])
    with left_col:
        components.html(spotify_animation_html)
    with right_col:
        st.markdown(heading_animation, unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------- #
# --- RECCOMMENDER SYSTEM ---

user_df = None

with st.container():
    st.title("Pick your favourite songs  :musical_note:")
    st.subheader("Search for the song's title")
    user_songs = st.multiselect(label="Search", options=df["Song-Artist"],
                                label_visibility='collapsed')
    if st.button("Confirm Selection"):

        if len(user_songs) < 5 or len(user_songs) > 10:
            st.error("Please select only 5-10 songs", icon="⚠️")

        else:
            user_df = df[df["Song-Artist"].isin(user_songs)]
            recs_df = rec_sys.Recommend_Songs(user_songs)
            upload_data(recs_df, 'recommendations')
            user_df_len = user_df.shape[0]
            extra = user_df_len - 5

            st.subheader("Below are the profiles of your chosen songs, using which we'll analyse your preferences..")
			
            if user_df_len > 5:
                with st.container():
                    cols = st.columns(5)
                    for i in range(0, 5):
                        with cols[i]:
                            st.pyplot(plotPizza(getFeaturePercentiles(df, user_df['Song-Artist'].values[i], 'song')))
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {format_song_name(user_df['Song'].values[i])} <br>
                            			<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                        <b> Artist: </b> {format_artist_name(user_df['Artist Names'].values[i])} <br>
                                        <a href = {user_df['Spotify Link'].values[i]}>
                                        <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                        </p>""",
                                        unsafe_allow_html=True)
                with st.container():
                    cols = st.columns(5)
                    for i in range(0, extra):
                        with cols[i]:
                            st.pyplot(plotPizza(getFeaturePercentiles(df, user_df['Song-Artist'].values[i+extra], 'song')))
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {format_song_name(user_df['Song'].values[i+extra])} <br>
                            			<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                        <b> Artist: </b> {format_artist_name(user_df['Artist Names'].values[i+extra])} <br>
                                        <a href = {user_df['Spotify Link'].values[i+extra]}>
                                        <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                        </p>""",
                                        unsafe_allow_html=True)
            else:
                with st.container():
                    cols = st.columns(5)
                    for i in range(0, 5):
                        with cols[i]:
                            st.pyplot(plotPizza(getFeaturePercentiles(df, user_df['Song-Artist'].values[i], 'song')))
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {format_song_name(user_df['Song'].values[i])} <br>
                            			<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                        <b> Artist: </b> {format_artist_name(user_df['Artist Names'].values[i])} <br>
                                        <a href = {user_df['Spotify Link'].values[i]}>
                                        <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                        </p>""",
                                        unsafe_allow_html=True)

            st.write("<br>", unsafe_allow_html=True)

            st.subheader("Based on your music taste, you might also like:")

            with st.container():
                cols = st.columns(5)
                for i in range(0, 5):
                    with cols[i]:
                        st.image(recs_df['Song Image'].values[i], use_column_width=True)
                        st.markdown(
                            f"""<p align = 'center'> <b> Song: </b> {format_song_name(recs_df['Song'].values[i])} <br>
                            		<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                    <b> Artist: </b> {format_artist_name(recs_df['Artist Names'].values[i])} <br>
                                    <a href = {recs_df['Spotify Link'].values[i]}>
                                    <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                    </p>""",
                            unsafe_allow_html=True)
            with st.container():
                cols = st.columns(5)
                for i in range(0, 5):
                    with cols[i]:
                        st.image(recs_df['Song Image'].values[5 + i], use_column_width=True)
                        st.markdown(
                            f"""<p align = 'center'> <b> Song: </b> {format_song_name(recs_df['Song'].values[5 + i])} <br>
                            	<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                <b> Artist: </b> {format_artist_name(recs_df['Artist Names'].values[5 + i])} <br>
                                <a href = {recs_df['Spotify Link'].values[5 + i]}>
                                <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                </p>""",
                            unsafe_allow_html=True)
            with st.container():
                cols = st.columns(5)
                for i in range(0, 5):
                    with cols[i]:
                        st.image(recs_df['Song Image'].values[10 + i], use_column_width=True)
                        st.markdown(
                            f"""<p align = 'center'> <b> Song: </b> {format_song_name(recs_df['Song'].values[10 + i])} <br>
                            	<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                <b> Artist: </b> {format_artist_name(recs_df['Artist Names'].values[10 + i])} <br>
                                <a href = {recs_df['Spotify Link'].values[10 + i]}>
                                <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                </p>""",
                            unsafe_allow_html=True)
            with st.container():
                cols = st.columns(5)
                for i in range(0, 5):
                    with cols[i]:
                        st.image(recs_df['Song Image'].values[15 + i], use_column_width=True)
                        st.markdown(
                            f"""<p align = 'center'> <b> Song: </b> {format_song_name(recs_df['Song'].values[15 + i])} <br>
                            	<b> Album: </b> {format_song_name(user_df['Album'].values[i])} <br>
                                <b> Artist: </b> {format_artist_name(recs_df['Artist Names'].values[15 + i])} <br>
                                <a href = {recs_df['Spotify Link'].values[15 + i]}>
                                <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                </p>""",
                            unsafe_allow_html=True)
            with st.container():
                left_col, right_col = st.columns([1, 7])
                with left_col:
                    components.html(astro_animation_html)
                with right_col:
                    st.markdown(
                        "<p style = 'font-size: 36px; font-weight: bold;'> <br> Sit back and stream or ..</p>""",
                        unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------- #
# --- ARTIST PROFILE, GENRE PROFILES & MOOD PLAYLIST ---

st.markdown("""---""")

st.title("Explore more")
line1 = """<p style = "font-size: 22px;"> 
Explore the profiles of your favourite artists and their genres by opting for an artist or an artist's genre. The resultant visualisations will show the trajectory of its popularity as well as how dominant various audio features are for the selected choice. Moreover, you can also listen to some of our mood playlists in the Playlists tab.
</p> """
st.markdown(line1, unsafe_allow_html=True)

# --- TAB CONFIG ---

listTabs = ["Artist", "Genre", "Playlists"]
tabs_font_css = st.markdown("""
<style> button[data-baseweb="tab"] {font-size: 26px; font-weight: 520; background-color: #ffffff; color: #000000;}
button[data-baseweb="tab"]:hover {font-size: 26px; font-weight: 520; background-color: #1DDA63; color:#FFFFFF;}
button[data-baseweb="tab"]:focus {font-size: 26px; font-weight: 520; background-color: #1DDA63; color:#FFFFFF;}
</style>""", unsafe_allow_html=True)

chosen_artist = None
chosen_genre = None
chosen_mood = None

with st.container():
    tabs = st.tabs([s.center(21, "\u2001") for s in listTabs])

    # ------------------------------------------------------------------------------------------ #
    # TAB-1 ARTIST PROFILE

    with tabs[0]:
        # Code to enable choosing an artist
        st.subheader("Choose an Artist")
        col1, col2 = st.columns([1.6, 1])
        with col1:
            user_artist = st.selectbox(label="Search", options=artists, label_visibility='collapsed')
        with col2:
            if st.button("Confirm Selection", key=1):
                chosen_artist = user_artist

        # Profile
        if chosen_artist != None:
            st.subheader(f"Artist Profile for {chosen_artist},")

            cols = st.columns([2.5, 1, 2.2])

            with cols[0]:
                st.markdown('<br>', unsafe_allow_html=True)
                st.markdown(
                    '<p align = "center" style = "font-size: 24px; font-weight: bold"> Popularity w.r.t. Time </p>',
                    unsafe_allow_html=True)
                st.pyplot(plotHitProfile(hit_profile['Artist'][chosen_artist]))
                st.markdown(
                    "<p align = 'center' style = 'font-size: 20px;'> The Hit Quality is a metric that measures the quality of the ranks.<br>To elaborate, instead of determining the popularity of an artist by counting the no. of times they've appeared in the Billboard Hot 100, the hit quality metric will try to emphasize the correction of ranking by giving more weightage to the higher ranks and less importance to the lower ones. This will result in a more robust judgement of an artist's popularity. </p>",
                    unsafe_allow_html=True)

            with cols[1]:
                st.write("")

            with cols[2]:
                st.markdown(
                    '<p align = "center" style = "font-size: 24px; font-weight: bold"> Mean Percentile Ranks <br> </p>',
                    unsafe_allow_html=True)
                vals = getFeaturePercentiles(artist_genre_ohe_df, chosen_artist, 'artist')
                st.pyplot(plotPizza(vals))
                st.markdown(
                    f"<p align = 'center' style = 'font-size: 20px;'> A percentile rank indicates the percentage of scores in the frequency distribution that are less than that score. <br> In simple terms, a mean percentile rank of {vals[1]} for Acousticness for the artist {chosen_artist} indicates that {vals[1]}% of the songs in our database fall below the mean acousticness of the songs by the artist {chosen_artist}.</p>",
                    unsafe_allow_html=True)

    # ------------------------------------------------------------------------------------------ #
    # TAB-2 GENRE PROFILE

    with tabs[1]:

        # Code to enable choosing a genre
        st.subheader("Choose a Genre")
        col1, col2 = st.columns([1.6, 1])
        with col1:
            user_genre = st.selectbox(label="Search", options=genres, label_visibility='collapsed')
        with col2:
            if st.button("Confirm Selection", key=2):
                chosen_genre = user_genre

                # Profile
        if chosen_genre != None:
            st.subheader(f"Genre Profile for {chosen_genre},")

            cols = st.columns([2.5, 1, 2.2])

            with cols[0]:
                st.markdown('<br>', unsafe_allow_html=True)
                st.markdown(
                    '<p align = "center" style = "font-size: 24px; font-weight: bold"> Popularity w.r.t. Time </p>',
                    unsafe_allow_html=True)
                st.pyplot(plotHitProfile(hit_profile['Genre'][chosen_genre]))
                st.markdown(
                    "<p align = 'center' style = 'font-size: 20px;'> The Hit Quality is a metric that measures the quality of the ranks.<br>To elaborate, instead of determining the popularity of an artist's genre by counting the no. of times it has appeared in the Billboard Hot 100, the hit quality metric will try to emphasize the correction of ranking by giving more weightage to the higher ranks and less importance to the lower ones. This will result in a more robust judgement of a genre's popularity. </p>",
                    unsafe_allow_html=True)

            with cols[2]:
                st.markdown(
                    '<p align = "center" style = "font-size: 24px; font-weight: bold"> Mean Percentile Ranks <br> </p>',
                    unsafe_allow_html=True)
                vals = getFeaturePercentiles(artist_genre_ohe_df, chosen_genre, 'genre')
                st.pyplot(plotPizza(vals))
                st.markdown(
                    f"<p align = 'center' style = 'font-size: 20px;'> A percentile rank indicates the percentage of scores in the frequency distribution that are less than that score. <br> In simple terms, a mean percentile rank of {vals[1]} for Acousticness for the {chosen_genre} genre indicates that {vals[1]}% of the songs in our database fall below the mean acousticness of the songs belonging to the {chosen_genre} genre.</p>",
                    unsafe_allow_html=True)

        # ------------------------------------------------------------------------------------------ #
        # TAB-3 MOOD PLAYLISTS

        with tabs[2]:
            moods = ["Trending songs", "Dance party", "Monday Blues", "Energizing", "Positive vibes"]

            # Code to enable choosing a mood
            st.subheader("Choose a Mood")
            col1, col2 = st.columns([1.6, 1])
            with col1:
                user_mood = st.selectbox(label="Search", options=moods, label_visibility='collapsed')
            with col2:
                if st.button("Confirm Selection", key=3):
                    chosen_mood = user_mood

                    # Playlist display
            if chosen_mood != None:
                recs_df = pd.read_csv('artifacts/recommendations.csv')

                mood_df = getMoodPlaylist(recs_df, chosen_mood)

                st.subheader(f"Here's a {chosen_mood} playlist for you,")

                with st.container():
                    cols = st.columns(5)
                    for i in range(0, 5):
                        with cols[i]:
                            st.image(mood_df['Song Image'].values[i], use_column_width=True)
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {mood_df['Song'].values[i]} <br>
                            			<b> Album: </b> {format_song_name(mood_df['Album'].values[i])} <br>
                                        <b> Artist: </b> {format_artist_name(mood_df['Artist Names'].values[i])} <br>
                                        <a href = {mood_df['Spotify Link'].values[i]}>
                                        <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                        </p>""",
                                        unsafe_allow_html=True)
                with st.container():
                    cols = st.columns(5)
                    for i in range(0, 5):
                        with cols[i]:
                            st.image(mood_df['Song Image'].values[5 + i], use_column_width=True)
                            st.markdown(f"""<p align = 'center'> <b> Song: </b> {mood_df['Song'].values[5 + i]} <br>
                            			<b> Album: </b> {format_song_name(mood_df['Album'].values[i])} <br>
                                        <b> Artist: </b> {format_artist_name(mood_df['Artist Names'].values[5 + i])} <br>
                                        <a href = {mood_df['Spotify Link'].values[5 + i]}>
                                        <img alt="Spotify" src = {spotify_logo} width=15 height=15 hspace=5px><b>Listen on Spotify</b></a>
                                        </p>""",
                                        unsafe_allow_html=True)


# ---------------------------------------------------------------------------------------------- #
# --- CONTACT FORM & SOCIAL LINKS ---

st.markdown("""---""")

contact_form = """
<form action="https://formsubmit.co/tusharmahalya@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea><br>
     <button type="submit">Send</button>
</form>"""

with st.container():
    left_col, right_col = st.columns([6, 4])
    with left_col:
        st.header(":mailbox: Get In Touch With Me!")
        st.markdown("""<p style = 'font-size: 20px;'>Social Links : <a href='https://www.instagram.com/tushar_mahalya/', target='_blank'><img width="48" height="48" src="https://img.icons8.com/fluency/48/instagram-new.png" alt="instagram-new"/></a>
        <a href='https://www.linkedin.com/in/tushar-5harma/' target='_blank'><img width="48" height="48" src="https://img.icons8.com/color/48/linkedin.png" alt="linkedin"/></a>
        <a target='_blank' href='https://github.com/tushar-mahalya/'><img width="48" height="48" src="https://img.icons8.com/sf-regular-filled/48/FFFFFF/github.png" alt="github"/></a>
        <a target='_blank' href='mailto:tusharmahalya@gmail.com'><img width="48" height="48" src="https://img.icons8.com/fluency/48/gmail.png" alt="gmail"/></a>
        <a target='_blank' href='https://wa.me/+917652064884'><img width="48" height="48" src="https://img.icons8.com/color/48/whatsapp--v1.png" alt="whatsapp--v1"/></a></p>
        """, unsafe_allow_html=True)
        st.markdown(contact_form, unsafe_allow_html=True)
        
    with right_col:
        st.image(casette, use_column_width = True)
        st.markdown("""<p align='right' style = 'font-size: 20px;'>Thanks For Visiting ! </p>""", unsafe_allow_html=True)

st.markdown("""
<style>
input[type=text],
input[type=email],
textarea {
    width: 80%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    margin-top: 6px;
    margin-bottom: 16px;
    resize: vertical 
	}

button[type=submit] {
    background-color: #1DDA63;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
	}
button[type=submit]:hover {
    background-color: #ffffff
    color: black;
	}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------------- #    
# --- FOOTER ---

footer = """<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #000000;
    color: black;
    text-align: center;
	}
</style>
<div class="footer">
<font color = 'white'>Developed with ❤ by Tushar Sharma</font>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
