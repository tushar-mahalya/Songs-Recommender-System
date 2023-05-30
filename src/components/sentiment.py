# Code Credit - https://gist.github.com/enjuichang/09dc4b7996db2f21828ab70ead1e8e35#file-text_feature-py

from textblob import TextBlob
import pandas as pd


def getSubjectivity(text: str) -> float:
    """
    Calculate the subjectivity score of a text.

    Args:
        text (str): The input text.

    Returns:
        float: The subjectivity score.
    """
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text: str) -> float:
    """
    Calculate the polarity score of a text.

    Args:
        text (str): The input text.

    Returns:
        float: The polarity score.
    """
    return TextBlob(text).sentiment.polarity


def score_category(score: float, task: str = "polarity") -> str:
    """
    Determine the analysis category based on the score.

    Args:
        score (float): The input score.
        task (str, optional): The type of analysis ("polarity" or "subjectivity"). Defaults to "polarity".

    Returns:
        str: The analysis category.
    """
    if task == "subjectivity":
        if score < 1/3:
            return "low"
        elif score > 1/3:
            return "high"
        else:
            return "medium"
    else:
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'


def Sentiment_Features(df: pd.DataFrame, text_col: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Perform sentiment analysis on a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        text_col (str): The name of the text column in the DataFrame.

    Returns:
        tuple[pandas.DataFrame, pandas.DataFrame]: DataFrame with subjectivity scores,
        DataFrame with polarity scores.
    """
    subject_df = pd.DataFrame()
    polar_df = pd.DataFrame()
    subject_df['subjectivity'] = df[text_col].apply(getSubjectivity).apply(lambda x: score_category(x, "subjectivity"))
    polar_df['polarity'] = df[text_col].apply(getPolarity).apply(score_category)
    return subject_df, polar_df
