import streamlit as st
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from scipy.sparse import load_npz

# Set up Streamlit page configuration
st.set_page_config(
    page_title="BeatBuddy",
    page_icon="🎸",
    layout="wide",
)

# Spotify API credentials (hide in a secure way, e.g., environment variables in production)
CLIENT_ID = "3a53f879c80840dd93074b5fceebb366"
CLIENT_SECRET = "04cda66d5f3f403c9ee80b050e996861"

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load pre-trained music dataset and similarity matrix (now in sparse format)
music = pickle.load(open('df.pkl', 'rb'))
similarity = load_npz('similarity.npz')  # Load sparse matrix

# Streamlit App Header
st.header("🎵 Song Recommendation Engine")
st.subheader("Select a song, and we'll show you 10 similar recommendations based on lyrics!")

# Helper function to fetch album cover and Spotify URL
def get_song_info(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        spotify_url = track["external_urls"]["spotify"]  
        return album_cover_url, spotify_url
    else:
        return "icon.svg", "#"  # Placeholder for image and link if not found

# Recommendation function using sparse similarity matrix
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index].toarray()[0])), reverse=True, key=lambda x: x[1])  # Convert sparse to dense for comparison
    recommended_music_names = []        
    recommended_music_posters = []
    recommended_music_urls = []
    
    # Get top 10 recommendations from index 1 to 10 (excluding itself)
    for i in distances[1:11]:
        artist = music.iloc[i[0]].artist
        album_cover_url, spotify_url = get_song_info(music.iloc[i[0]].song, artist)
        recommended_music_posters.append(album_cover_url)
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_urls.append(spotify_url)  # Add Spotify URL to the list
    
    return recommended_music_names, recommended_music_posters, recommended_music_urls

# Create a formatted list for the dropdown with song and artist
music_list = [f"{row['song']} - {row['artist']}" for index, row in music.iterrows()]

# Use selectbox to allow user to pick a song
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

# Extract only the song name from the selected item
selected_song_name = selected_song.split(" - ")[0]  # Get only the song name

# When 'Show Recommendation' is clicked
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_music_urls = recommend(selected_song_name)
    
    # Create five columns for displaying recommendations in a 2x5 format
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"**[{recommended_music_names[0]}]({recommended_music_urls[0]})**")
        st.image(recommended_music_posters[0], use_column_width=True)
        st.markdown(f"**[{recommended_music_names[5]}]({recommended_music_urls[5]})**")
        st.image(recommended_music_posters[5], use_column_width=True)

    with col2:
        st.markdown(f"**[{recommended_music_names[1]}]({recommended_music_urls[1]})**")
        st.image(recommended_music_posters[1], use_column_width=True)
        st.markdown(f"**[{recommended_music_names[6]}]({recommended_music_urls[6]})**")
        st.image(recommended_music_posters[6], use_column_width=True)

    with col3:
        st.markdown(f"**[{recommended_music_names[2]}]({recommended_music_urls[2]})**")
        st.image(recommended_music_posters[2], use_column_width=True)
        st.markdown(f"**[{recommended_music_names[7]}]({recommended_music_urls[7]})**")
        st.image(recommended_music_posters[7], use_column_width=True)

    with col4:
        st.markdown(f"**[{recommended_music_names[3]}]({recommended_music_urls[3]})**")
        st.image(recommended_music_posters[3], use_column_width=True)
        st.markdown(f"**[{recommended_music_names[8]}]({recommended_music_urls[8]})**")
        st.image(recommended_music_posters[8], use_column_width=True)

    with col5:
        st.markdown(f"**[{recommended_music_names[4]}]({recommended_music_urls[4]})**")
        st.image(recommended_music_posters[4], use_column_width=True)
        st.markdown(f"**[{recommended_music_names[9]}]({recommended_music_urls[9]})**")
        st.image(recommended_music_posters[9], use_column_width=True)

    # Success message after displaying recommendations
    st.success("Hope you like these recommendations! 🎶")
