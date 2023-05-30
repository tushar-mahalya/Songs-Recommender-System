# --- IMPORTING DEPENDENCIES ---

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from matplotlib.ticker import MaxNLocator
from mplsoccer import PyPizza, FontManager
from sklearn.metrics.pairwise import cosine_similarity


# --- SETTING REQUIRED FONTS AND COLOURS ---

# FONTS
robotoBold = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamBold.ttf')
robotoMed = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamMedium.ttf')

# COLOURS
spotifyGreen = '#1dda63'
bg_color_cas = "#9bf0e1"
grey = "#979797"
lightgrey = "#bdbdbd"


# ---------------------------------------------------------------------------------------------- #

# --- DEFINING REQUIRED FUNCTIONS ---

# 1
# Quality function that determines the quality of the rank

def quality(ranks):
    rankQuality = []
    for rank in ranks:
        rankQuality.append(100 - rank + 1)

    return sum(rankQuality)


# 2
# Song values function that obtains the required feature values for a given song

def getFeaturePercentiles(df: pd.DataFrame, feature: str, feat_type: str = None):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']

    featProfile = df[df['Song-Artist'] == feature]
    featProfile.reset_index(inplace=True, drop=True)

    values = []
    if feat_type == 'song':
        feats = featProfile.filter(featColumns)
        feats = list(feats.iloc[0])
        for x in range(len(featColumns)):
            values.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], feats[x])))
        return values
    else:
        for idx in range(len(featProfile)):
            feats = list(featProfile.loc[idx])
            feats_lst = []
            for x in range(len(featColumns)):
                feats_lst.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], feats[x])))
            values.append(feats_lst)

        return np.round(np.mean(values, axis=0)).astype(int)





# 3
# Artist values function that obtains the mean of required feature values for a given artist

def getArtistValues(df, artist):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']

    artistData = df[df['Artist: ' + artist] == 1][featColumns]
    artistData.reset_index(drop=True, inplace=True)

    values = []
    for idx in range(len(artistData)):
        songFeats = list(artistData.loc[idx])
        valuesSong = []
        for x in range(len(featColumns)):
            valuesSong.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], songFeats[x])))
        values.append(valuesSong)

    return np.round(np.mean(values, axis=0)).astype(int)


# 4
# Genre values function that obtains the mean of required feature values for a given genre

def getGenreValues(df, genre):
    featColumns = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness',
                   'Speechiness', 'Tempo', 'Valence']

    genre = genre.lower()
    genreData = df[df['Genre: ' + genre] == 1][featColumns]
    genreData.reset_index(drop=True, inplace=True)

    values = []
    for idx in range(len(genreData)):
        genreFeats = list(genreData.loc[idx])
        valuesGenre = []
        for x in range(len(featColumns)):
            valuesGenre.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]], genreFeats[x])))
        values.append(valuesGenre)

    return np.round(np.mean(values, axis=0)).astype(int)


# ---------------------------------------------------------------------------------------------- #


# --- DEFINING REQUIRED PLOTTING FUNCTIONS ---

# 1
# Plot Artist function that plots the trends of a given artist

def plotArtist(artist):
    dfArtist = df[df['Artist: ' + artist] == 1]
    dfYearArtist = pd.DataFrame()
    dfYearArtist['Year'] = [year for year in range(1960, 2022)]
    tempArtist = dfArtist.groupby('Year')['Rank'].apply(list).apply(quality)
    dfYearArtist = dfYearArtist.merge(tempArtist, left_on='Year', right_index=True, how='left')
    dfYearArtist.columns = ['Year', 'Hit Quality']
    dfYearArtist['Year'] = dfYearArtist['Year'].astype(int)
    dfYearArtist.fillna(0, inplace=True)

    # Setting the color and linewidth of the spines/borders
    mpl.rc('axes', edgecolor=grey)
    mpl.rc('axes', linewidth='2')

    fig, ax = plt.subplots(figsize=(8, 6))

    # Adding bg color and setting the grid
    fig.set_facecolor(bg_color_cas)
    ax.set_facecolor('w')
    ax.set_axisbelow(True)
    ax.grid(color=lightgrey, which='major', linestyle='--', alpha=1)
    # Plotting
    ax.plot(dfYearArtist['Year'], dfYearArtist['Hit Quality'], '-', color=spotifyGreen, lw=4)
    # Setting the limits for x and y axes
    minYear = min(dfYearArtist[dfYearArtist['Hit Quality'] > 0]['Year'])
    ax.set_xlim([minYear, 2021])
    ax.set_xticks(np.arange(minYear, 2021, (2021 - minYear) / 10))
    # Setting the x label as year for every subplot
    ax.set_xlabel('Year', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Customizing the x and y ticklabels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    ax.tick_params(axis='both', which='major', labelcolor='k', length=0, color='#2b2b2b')

    return fig


# 2
# Plot Genre function that plots the trends of a given genre

def plotGenre(genre):
    genre = genre.lower()
    dfGenre = df[df['Genre: ' + genre] == 1]
    dfYearGenre = pd.DataFrame()
    dfYearGenre['Year'] = [year for year in range(1960, 2022)]
    tempGenre = dfGenre.groupby('Year')['Rank'].apply(list).apply(quality)
    dfYearGenre = dfYearGenre.merge(tempGenre, left_on='Year', right_index=True, how='left')
    dfYearGenre.columns = ['Year', 'Hit Quality']
    dfYearGenre.fillna(0, inplace=True)

    # Setting the color and linewidth of the spines/borders
    mpl.rc('axes', edgecolor='grey')
    mpl.rc('axes', linewidth='2')

    fig, ax = plt.subplots(figsize=(8, 6))

    # Adding bg color and setting the grid
    fig.set_facecolor(bg_color_cas)
    ax.set_facecolor('w')
    ax.set_axisbelow(True)
    ax.grid(color=lightgrey, which='major', linestyle='--', alpha=1)
    # Plotting
    ax.plot(dfYearGenre['Year'], dfYearGenre['Hit Quality'], '-', color=spotifyGreen, lw=4)
    # Setting the limits for x and y axes
    ax.set_xlim([1960, 2021])
    # Setting the x label as year for every subplot
    ax.set_xlabel('Year', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    ax.set_ylabel('Hit Quality', fontsize=16, labelpad=10, fontproperties=robotoMed.prop, color='k')
    # Customizing the x and y ticklabels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    for ticklabel in ax.get_xticklabels():
        ticklabel.set_fontproperties(robotoMed.prop)
        ticklabel.set_fontsize(14)
    ax.tick_params(axis='both', which='major', labelcolor='k', length=0, color='#2b2b2b')

    return fig


# 3
# Pizza plot function that takes values and plots a pizza chart

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