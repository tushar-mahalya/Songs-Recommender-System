import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from spotipy import Spotify


def BillboardData(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Retrieves Billboard Year-End Hot 100 singles data from Wikipedia for the specified range of years.

    Args:
        start_year (int): The start year of the range.
        end_year (int): The end year of the range.

    Returns:
        pd.DataFrame: The DataFrame containing the Billboard data.

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
            rank.append(columns[0].text.strip())
            song.append(columns[1].text.strip('"\n'))
            artist.append(columns[2].text.strip('\n'))

        df = pd.DataFrame({'Rank': rank, 'Song': song, 'Artist': artist, 'Year': year})
        dfs.append(df)

    dfBillboards = pd.concat(dfs, ignore_index=True)
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
            searchResults = sp.search(q=f"track:{track} artist:{artist}", type='track')
            songURI = searchResults['tracks']['items'][0]['uri']
        except:
            try:
                searchResults = sp.search(q=f"track:{track} artist:{artist} year:{year}", type='track')
                songURI = searchResults['tracks']['items'][0]['uri']
            except:
                try:
                    searchResults = sp.search(q=f"artist:{artist} track:{track} year:{year}", type='track')
                    songURI = searchResults['tracks']['items'][0]['uri']
                except:
                    try:
                        artistResults = sp.search(q=f"artist:{artist}", limit=50)
                        songName = re.sub('[^A-Za-z0-9\s]+', '', track).lower()
                        for i in range(len(artistResults['tracks']['items'])):
                            artistSongName = re.sub('[^A-Za-z0-9\s]+', '',
                                                    artistResults['tracks']['items'][i]['name'].lower())
                            if songName in artistSongName or artistSongName in songName:
                                songURI = artistResults['tracks']['items'][i]['uri']
                                break
                    except:
                        try:
                            artist = artist.split('featuring')[0]
                            searchResults = sp.search(q=f"{track}, {artist}, {year}", type='track')
                            songURI = searchResults['tracks']['items'][0]['uri']
                        except:
                            try:
                                artist = artist.split('and')[0]
                                searchResults = sp.search(q=f"{track}, {artist}, {year}", type='track')
                                songURI = searchResults['tracks']['items'][0]['uri']
                            except:
                                songURI = 'Unavailable'

        songURIList.append(songURI)

    df['URI'] = songURIList
    return df
