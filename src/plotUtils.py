import math
import scipy
from mplsoccer import PyPizza, FontManager
import pandas as pd
import numpy as np

spotifyGreen = '#1dda63'
bg_color_cas = "#9bf0e1"
grey = "#979797"
lightgrey = "#bdbdbd"

robotoBold = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamBold.ttf')
robotoMed = FontManager('https://tushar-mahalya.github.io/images-repo/Fonts/GothamMedium.ttf')

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