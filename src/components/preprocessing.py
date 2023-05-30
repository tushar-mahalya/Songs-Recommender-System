import warnings
from ast import literal_eval
from collections import Counter
from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer

warnings.filterwarnings("ignore")


# noinspection PyBroadException
def formatToList(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrects the formatting of Artist Names and Artist(s) Genre column to List object.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'Artist Names' and 'Artist(s) Genre'.

    Returns:
        pd.DataFrame: Original DataFrame with correct formatting of specified columns.
    """
    try:
        df['Artist(s) Genres'] = df['Artist(s) Genres'].apply(lambda value: literal_eval(value))
        df['Artist Names'] = df['Artist Names'].apply(lambda value: literal_eval(value))
    except:
        df['Artist(s) Genres'] = df['Artist(s) Genres'].apply(lambda value: np.nan)
        df['Artist Names'] = df['Artist Names'].apply(lambda value: np.nan)

    return df


def combineArtistGenre(df: pd.DataFrame) -> pd.DataFrame:
    """
        Combines the song and artist names into a single column with a hyphen separator.

        Args:
            df (pd.DataFrame): The input DataFrame with columns 'Song' and 'Artist Names'.

        Returns:
            pd.DataFrame: Original DataFrame with extra column 'Song-Artist' combined of 'Artist Names' and 'Song'.
        """
    df['Song-Artist'] = df['Song'] + ' - ' + df['Artist Names'].apply(lambda artist: ', '.join(artist))
    return df


def removeDuplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame based on 'Song-Artist' columns.

    Args:
        df (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: Original DataFrame without duplicate rows and NaN values.
    """
    duplicate_idx = df[df.duplicated(subset=['Song-Artist'])].index
    df.drop(duplicate_idx, axis=0, inplace=True)
    df.dropna(subset=['Song', 'Acousticness', 'Danceability', 'Energy',
                      'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Tempo',
                      'Valence', 'Key', 'Mode', 'Time Signature', 'Popularity'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def TFIDF_Features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate TF-IDF features for the 'Artist(s) Genres' column of a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: New DataFrame with TF-IDF features.
    """

    def custom_tokenizer(text: str) -> list:
        return text.split(', ')

    tfidf = TfidfVectorizer(tokenizer=custom_tokenizer)
    tfidf_matrix = tfidf.fit_transform(df['Artist(s) Genres'].apply(lambda x: ", ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['Genre' + " | " + i for i in tfidf.get_feature_names_out()]
    genre_df.drop(columns='Genre | ', inplace=True)
    return genre_df


def OHE_List_w_Feats(df: pd.DataFrame, feature_type: str, audio_feats: bool = True) -> pd.DataFrame:
    """
    One-hot encode a column with list values in a DataFrame and optionally include additional audio features.

    Args:
        df (pd.DataFrame): The input DataFrame.
        feature_type (str): The type of the feature to be one-hot encoded ('Artist' or 'Genre').
        audio_feats (bool, optional): Whether to include additional audio features in the output DataFrame.
                                      Defaults to True.

    Returns:
        pd.DataFrame: The DataFrame with the specified column one-hot encoded and optionally combined with audio features.

    """
    mlb = MultiLabelBinarizer()

    if feature_type == 'Artist':
        col = 'Artist Names'
    elif feature_type == 'Genre':
        col = 'Artist(s) Genres'

    ohe_df = pd.DataFrame(mlb.fit_transform(df.pop(col)), index=df.index,
                          columns=[feature_type + ' | ' + cls for cls in mlb.classes_])
    if audio_feats:
        audio_feats_df = df[['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Hot100 Rank', 'Valence',
                             'Hot100 Ranking Year', 'Instrumentalness', 'Loudness', 'Speechiness', 'Tempo']]
        ohe_final_df = pd.concat([ohe_df, audio_feats_df], axis=1)
        return ohe_final_df
    else:
        return ohe_df


def OHE_Column(df: pd.DataFrame, column: str, new_name: str) -> pd.DataFrame:
    """
    Perform one-hot encoding on a specific column of a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column (str): The column name to be one-hot encoded.
        new_name (str): The prefix for the new column names.

    Returns:
        pandas.DataFrame: New DataFrame with one-hot encoded column.
    """
    ohe_col = pd.get_dummies(df[column], dtype=int)
    feature_names = ohe_col.columns
    ohe_col.columns = [new_name + " | " + str(i) for i in feature_names]
    return ohe_col


def Standardize_Features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Standardize selected numerical columns of a DataFrame using Min-Max scaling.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        columns (list): The list of column names to be standardized.

    Returns:
        pandas.DataFrame: New DataFrame with standardized features.
    """
    num_df = df[columns]
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(num_df), columns=num_df.columns)
    return df_scaled


def Hit_Quality_Annual(feature_name: str, ohe_df: pd.DataFrame, feature_type: str) -> dict[int, int]:
    """
    Calculate the annual hit quality for a specific feature based on the provided one-hot encoded DataFrame.

    Args:
        feature_name (str): The name of the feature for which the hit quality will be calculated.
        ohe_df (pandas.DataFrame): The one-hot encoded DataFrame containing the feature and hit rank information.
        feature_type (str): The type of the feature (e.g., 'Artist', 'Genre').

    Returns:
        dict[int, int]: A dictionary representing the annual hit quality for the specified feature. The dictionary has
        years as keys (int) and the corresponding hit quality scores (int) as values.

    """

    def quality(ranks: list[int]) -> int:
        rankQuality = []
        for rank in ranks:
            rankQuality.append(100 - rank + 1)

        return sum(rankQuality)

    feat_df = ohe_df[ohe_df[f'{feature_type} | ' + feature_name] == 1]
    new_feat_df = pd.DataFrame()
    new_feat_df['Year'] = [year for year in range(1946, 2023)]
    tempArtist = feat_df.groupby('Hot100 Ranking Year')['Hot100 Rank'].apply(list).apply(quality)
    new_feat_df = new_feat_df.merge(tempArtist, left_on='Year', right_index=True, how='left')
    new_feat_df.columns = ['Year', 'Hit Quality']
    new_feat_df['Year'] = new_feat_df['Year'].astype(int)
    new_feat_df.fillna(0, inplace=True)
    hit_rank_dict = new_feat_df.set_index('Year')['Hit Quality'].to_dict()
    return hit_rank_dict


def getAnnualHitQualityProfile(df: pd.DataFrame) -> tuple[dict[Any, Any], dict[Any, Any]]:
    """
    Calculate the annual hit quality profile for artists and genres based on the input DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame with columns 'Artist Names' and 'Artist(s) Genre'.

    Returns:
        tuple[dict[Any, Any], dict[Any, Any]]: A tuple containing two dictionaries representing the annual hit quality
        profiles for artists and genres respectively. The dictionaries have artists and genres as keys and their
        respective hit quality scores as values.
    """
    all_songs_list = list(df['Artist Names'])
    all_genre_list = list(df['Artist(s) Genres'])
    songs_flat_list = [artist for sublist in all_songs_list for artist in sublist]
    genre_flat_list = [artist for sublist in all_genre_list for artist in sublist]
    song_count = Counter(songs_flat_list)
    genre_count = Counter(genre_flat_list)
    artists = []
    genres = []
    for artist, _ in song_count.items():
        artists.append(artist)
    for genre, _ in genre_count.items():
        genres.append(genre)
    ohe_artist_df = OHE_List_w_Feats(df, 'Artist')
    ohe_genre_df = OHE_List_w_Feats(df, 'Genre')

    artist_rank_dict = {}
    genre_rank_dict = {}
    for artist in artists:
        artist_rank_dict[artist] = Hit_Quality_Annual(artist, ohe_artist_df, 'Artist')
    for genre in genres:
        genre_rank_dict[genre] = Hit_Quality_Annual(genre, ohe_genre_df, 'Genre')

    return artist_rank_dict, genre_rank_dict
