import re
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from spotipy import Spotify


def Billboards_Hot100_Chart(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetches Billboard Hot 100 chart data from Wikipedia for a given range of years.

    Args:
        start_year (int): Starting year of the Billboard charts.
        end_year (int): Ending year of the Billboard charts.

    Returns:
        pd.DataFrame: DataFrame containing the Billboard Hot 100 chart data for the specified years.
    """

    dfs = []

    for year in range(start_year, end_year + 1):
        mainURL = f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}'
        req = requests.get(mainURL)
        soup = BeautifulSoup(req.text, 'html.parser')

        rank = []
        song = []
        artist = []

        table = soup.find('table', attrs={'class': 'wikitable'})
        rows = table.find_all('tr')[1:]

        for row in rows:
            columns = row.find_all('td')
            if len(columns) != 3:
                continue
            rank_text = columns[0].text.strip()
            match = re.match(r'\d+', rank_text)
            if match:
                rank_number = match.group()
                rank.append(rank_number)
                song.append(columns[1].text.strip('"\n'))
                artist.append(columns[2].text.strip('\n'))

        df = pd.DataFrame({'Rank': rank, 'Song': song, 'Artist': artist, 'Year': year})
        dfs.append(df)

    dfBillboards = pd.concat(dfs, ignore_index=True)
    dfBillboards[['Song', 'Artist']] = dfBillboards[['Song', 'Artist']].astype('str')
    dfBillboards[['Rank', 'Year']] = dfBillboards[['Rank', 'Year']].astype('Int64')
    return dfBillboards


# noinspection PyBroadException
def addURIColumn(df: pd.DataFrame, sp: Spotify) -> pd.DataFrame:
    """
    Adds a URI column to the given DataFrame by searching for song URIs using the Spotify API.

    Args:
        df (pd.DataFrame): The DataFrame containing song information.
        sp (spotipy.Spotify): An instance of the Spotipy client for making Spotify API calls.

    Returns:
        pd.DataFrame: The DataFrame with an additional URI column.

    """
    songURIList = []

    for _, row in df.iterrows():
        track = row['Song']
        year = row['Year']
        artist = row['Artist']

        try:
            searchResults = sp.search(q=f"track:{track} artist:{artist}", type='track', limit=1)
            songURI = searchResults['tracks']['items'][0]['uri']
        except:
            try:
                searchResults = sp.search(q=f"track:{track} artist:{artist} year:{year}", type='track', limit=1)
                songURI = searchResults['tracks']['items'][0]['uri']
            except:
                try:
                    searchResults = sp.search(q=f"artist:{artist} track:{track} year:{year}", type='track', limit=1)
                    songURI = searchResults['tracks']['items'][0]['uri']
                except:
                    try:
                        artist = artist.split('featuring')[0]
                        searchResults = sp.search(q=f"{track}, {artist}, {year}", type='track', limit=1)
                        songURI = searchResults['tracks']['items'][0]['uri']
                    except:
                        try:
                            artist = artist.split('and')[0]
                            searchResults = sp.search(q=f"{track}, {artist}, {year}", type='track', limit=1)
                            songURI = searchResults['tracks']['items'][0]['uri']
                        except:
                            songURI = 'Unavailable'

        songURIList.append(songURI)

    df['URI'] = songURIList
    return df


# noinspection PyBroadException
def Spotify_Features(df: pd.DataFrame, sp: Spotify) -> pd.DataFrame:
    """
    Fetch Data from Spotify API and give out fresh dataframe with other additional information and audio features
    of the songs.

    Args:
        df (pd.DataFrame): The DataFrame containing the Billboard data ('URI', 'Year' and 'Rank' cols are must).
        sp (spotipy.Spotify): An initialized Spotipy instance.

    Returns:
        pd.DataFrame: The new DataFrame with added Spotify features.

    """
    new_df = pd.DataFrame(columns=['Song', 'Album', 'Album Release Date', 'Artist Names', 'Artist(s) Genres',
                                   'Hot100 Ranking Year', 'Hot100 Rank', 'Song Length(ms)', 'Spotify Link',
                                   'Song Image', 'Spotify URI', 'Popularity', 'Acousticness',
                                   'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness',
                                   'Speechiness', 'Tempo', 'Valence'])

    # Looping over URI of all the Billboard songs
    for idx, (songURI, rankYear, BBrank) in enumerate(zip(df['URI'], df['Year'], df['Rank'])):
        song = sp.track(songURI)
        album = sp.album(song["album"]["external_urls"]["spotify"])
        genres = [sp.artist(artist['external_urls']['spotify'])['genres'] for artist in song['artists']]

        new_df.at[idx, 'Song'] = song['name']
        new_df.at[idx, 'Album'] = song['album']['name']
        new_df.at[idx, 'Album Release Date'] = album['release_date']
        new_df.at[idx, 'Artist Names'] = list(artist['name'] for artist in song['artists'])
        new_df.at[idx, 'Artist(s) Genres'] = list(set(np.concatenate(genres)))
        new_df.at[idx, 'Hot100 Ranking Year'] = rankYear
        new_df.at[idx, 'Hot100 Rank'] = BBrank
        new_df.at[idx, 'Song Length(ms)'] = song['duration_ms']
        new_df.at[idx, 'Spotify Link'] = song['external_urls']['spotify']
        new_df.at[idx, 'Song Image'] = song['album']['images'][1]['url']
        new_df.at[idx, 'Spotify URI'] = songURI
        new_df.at[idx, 'Popularity'] = song['popularity']

        try:
            audioFeatures = sp.audio_features(song['uri'])[0]
            new_df.at[idx, 'Song Image'] = song['album']['images'][1]['url']
            new_df.at[idx, 'Acousticness'] = audioFeatures['acousticness']
            new_df.at[idx, 'Danceability'] = audioFeatures['danceability']
            new_df.at[idx, 'Energy'] = audioFeatures['energy']
            new_df.at[idx, 'Instrumentalness'] = audioFeatures['instrumentalness']
            new_df.at[idx, 'Liveness'] = audioFeatures['liveness']
            new_df.at[idx, 'Loudness'] = audioFeatures['loudness']
            new_df.at[idx, 'Speechiness'] = audioFeatures['speechiness']
            new_df.at[idx, 'Tempo'] = audioFeatures['tempo']
            new_df.at[idx, 'Valence'] = audioFeatures['valence']
            new_df.at[idx, 'Key'] = audioFeatures['key']
            new_df.at[idx, 'Mode'] = audioFeatures['mode']
            new_df.at[idx, 'Time Signature'] = audioFeatures['time_signature']
        except:
            new_df.at[idx, 'Song Image'] = 'Unavailable'
            new_df.at[idx, 'Acousticness'] = 'Unavailable'
            new_df.at[idx, 'Danceability'] = 'Unavailable'
            new_df.at[idx, 'Energy'] = 'Unavailable'
            new_df.at[idx, 'Instrumentalness'] = 'Unavailable'
            new_df.at[idx, 'Liveness'] = 'Unavailable'
            new_df.at[idx, 'Loudness'] = 'Unavailable'
            new_df.at[idx, 'Speechiness'] = 'Unavailable'
            new_df.at[idx, 'Tempo'] = 'Unavailable'
            new_df.at[idx, 'Valence'] = 'Unavailable'
            new_df.at[idx, 'Key'] = 'Unavailable'
            new_df.at[idx, 'Mode'] = 'Unavailable'
            new_df.at[idx, 'Time Signature'] = 'Unavailable'

    new_df = new_df[new_df['Danceability'] != 'Unavailable']
    new_df[['Song', 'Album', 'Spotify URI',
            'Spotify Link', 'Song Image']] = new_df[['Song', 'Album', 'Spotify URI',
                                                     'Spotify Link', 'Song Image']].astype('str')
    new_df[['Hot100 Rank', 'Hot100 Ranking Year',
            'Popularity', 'Song Length(ms)', 'Mode',
            'Key', 'Time Signature']] = new_df[['Hot100 Rank', 'Hot100 Ranking Year',
                                                'Popularity', 'Song Length(ms)', 'Mode',
                                                'Key', 'Time Signature']].apply(
        lambda x: pd.to_numeric(x, errors='coerce').astype('Int64'))
    new_df[['Artist Names', 'Artist(s) Genres']] = new_df[['Artist Names', 'Artist(s) Genres']].astype('object')
    new_df[['Acousticness', 'Danceability', 'Energy', 'Instrumentalness',
            'Liveness', 'Loudness', 'Speechiness', 'Tempo', 'Valence']] = new_df[['Acousticness', 'Danceability',
                                                                                  'Energy', 'Instrumentalness',
                                                                                  'Liveness', 'Loudness',
                                                                                  'Speechiness', 'Tempo',
                                                                                  'Valence']].astype('float64')
    new_df.reset_index(inplace=True, drop=True)

    return new_df
