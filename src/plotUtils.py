import math
from ast import literal_eval

import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mplsoccer import PyPizza, FontManager
import pandas as pd
import numpy as np

spotifyGreen = '#1dda63'
bg_color_cas = "#9bf0e1"
grey = "#979797"
lightgrey = "#bdbdbd"

robotoBold = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamBold.ttf')
robotoMed = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamMedium.ttf')


def format_song_name(song: str):
    new = song.split('(')[0].strip()
    new = new.split('-')[0].strip()
    return new


def format_artist_name(artist_str: str):
    new = literal_eval(artist_str)[0]
    return new


def getFeaturePercentiles(df: pd.DataFrame, feature: str, feat_type: str = 'song'):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']
    values = []
    if feat_type == 'song':
        songProfile = df[df['Song-Artist'] == feature]
        songProfile.reset_index(inplace=True, drop=True)

        songFeats = songProfile.filter(featColumns)
        songFeats = list(songFeats.iloc[0])
        for x in range(len(featColumns)):
            values.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], songFeats[x])))

        return values
    elif feat_type == 'artist':
        artistData = df[df['Artist | ' + feature] == 1][featColumns]
        artistData.reset_index(drop=True, inplace=True)

        for idx in range(len(artistData)):
            songFeats = list(artistData.loc[idx])
            valuesSong = []
            for x in range(len(featColumns)):
                valuesSong.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], songFeats[x])))
            values.append(valuesSong)

        return np.round(np.mean(values, axis=0)).astype(int)

    elif feat_type == 'genre':
        genreData = df[df['Genre | ' + feature] == 1][featColumns]
        genreData.reset_index(drop=True, inplace=True)

        for idx in range(len(genreData)):
            genreFeats = list(genreData.loc[idx])
            valuesGenre = []
            for x in range(len(featColumns)):
                valuesGenre.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], genreFeats[x])))
            values.append(valuesGenre)

        return np.round(np.mean(values, axis=0)).astype(int)


def plotPizza(values):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']
    slice_colors = [spotifyGreen] * 9
    text_colors = ["w"] * 9

    # Instantiate PyPizza class
    baker = PyPizza(
        params=featColumns,
        background_color=bg_color_cas,
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
        color_blank_space=["w"] * 9,
        slice_colors=slice_colors,
        value_bck_colors=slice_colors,
        param_location=115,
        blank_alpha=1,
        kwargs_slices=dict(edgecolor="k", zorder=2, linewidth=2, alpha=.8, linestyle='-'),
        kwargs_params=dict(color="k", fontsize=22, fontweight='bold',
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
    ax.set_facecolor('w')
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

    # Setting the x label as year for every subplot
    ax.set_xlabel('Year', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Customizing the x and y tick labels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)

    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)

    ax.tick_params(axis='both', which='major', labelcolor='k', length=0, color='#2b2b2b')

    return fig


def getMoodPlaylist(recc_df, chosen_mood):
    if chosen_mood == "Trending songs":
        rec_songs_idx = list(recc_df.sort_values(by='Popularity', ascending=False).index)[0:20]

    elif chosen_mood == "Dance party":
        rec_songs_idx = list(recc_df.sort_values(by='Danceability', ascending=False).index)[0:20]

    elif chosen_mood == "Monday Blues":
        rec_songs_idx = list(recc_df.sort_values(by='Valence', ascending=True).index)[0:20]

    elif chosen_mood == "Energizing":
        rec_songs_idx = list(recc_df.sort_values(by='Energy', ascending=False).index)[0:20]

    elif chosen_mood == "Positive vibes":
        rec_songs_idx = list(recc_df.sort_values(by='Valence', ascending=False).index)[0:20]

    mood_df = recc_df.iloc[rec_songs_idx]

    return mood_df
