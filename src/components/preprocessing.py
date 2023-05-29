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


def OHE_Artist_Genre(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-hot encode a column with list values in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str): The column name containing the list values to be one-hot encoded.
        col_name (str): The desired prefix for the resulting one-hot encoded columns.

    Returns:
        pd.DataFrame: The DataFrame with the specified column one-hot encoded.
        
    """
    mlb = MultiLabelBinarizer()

    ohe_artist = pd.DataFrame(mlb.fit_transform(df.pop('Artist Names')), index=df.index,
                              columns=['Artist' + ' | ' + cls for cls in mlb.classes_])
    ohe_genre = pd.DataFrame(mlb.fit_transform(df.pop('Artist(s) Genres')),index=df.index,
                             columns=['Genre' + ' | ' + cls for cls in mlb.classes_])
    audio_feats_df = df[['Popularity', 'Acousticness', 'Danceability', 'Energy',
                                 'Instrumentalness', 'Loudness', 'Speechiness', 'Tempo', 'Valence']]
    ohe_artist_genre = pd.concat([ohe_artist, ohe_genre, audio_feats_df], axis=1)
    return ohe_artist_genre


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


def getArtistGenre(df: pd.DataFrame) -> tuple[list[Any], list[Any]]:
    """
    Get the Unique value of the artists and the genres.

    Args:
        df (pandas.DataFrame): The input DataFrame with columns 'Artist Names' and 'Artist(s) Genre'.

    Returns:
        tuple[list[Any], list[Any]]: Lists with all artists and genres from the DataFrame.
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
    return artists, genres
