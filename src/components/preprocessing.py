import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

def removeDuplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame based on selected columns.

    Args:
        df (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: The DataFrame with duplicate rows removed.
    """
    col = ['Song', 'Energy', 'Artist Names', 'Instrumentalness', 'Liveness',
           'Spotify Link', 'Loudness', 'Speechiness', 'Tempo', 'Valence']
    duplicate_idx = df[df.duplicated(subset=col)].index
    df.drop(duplicate_idx, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    df['Artist(s) Genres'] = df['Artist(s) Genres'].apply(lambda value: literal_eval(value))
    df['Artist Names'] = df['Artist Names'].apply(lambda value: literal_eval(value))
    return df

def TFIDF_Features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate TF-IDF features for the 'Artist(s) Genres' column of a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.

    Returns:
        pandas.DataFrame: The DataFrame with TF-IDF features.
    """
    def custom_tokenizer(text: str) -> list:
        return text.split(', ')

    tfidf = TfidfVectorizer(tokenizer=custom_tokenizer)
    tfidf_matrix = tfidf.fit_transform(df['Artist(s) Genres'].apply(lambda x: ", ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['Genre' + " | " + i for i in tfidf.get_feature_names_out()]
    genre_df.drop(columns='Genre | ', inplace=True)
    return genre_df

def OHE_Column(df: pd.DataFrame, column: str, new_name: str) -> pd.DataFrame:
    """
    Perform one-hot encoding on a specific column of a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column (str): The column name to be one-hot encoded.
        new_name (str): The prefix for the new column names.

    Returns:
        pandas.DataFrame: The DataFrame with one-hot encoded column.
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
        pandas.DataFrame: The DataFrame with standardized features.
    """
    num_df = df[columns]
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(num_df), columns=num_df.columns)
    return df_scaled
