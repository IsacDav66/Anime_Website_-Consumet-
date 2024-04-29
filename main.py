from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
api_base_url = "https://consumet-api-jw7b.onrender.com"

@app.route('/')
def index():
    return render_template('index.html', results=[])

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_anime(query)
    return render_template('index.html', results=results)

@app.route('/anime-details', methods=['POST'])
def anime_details():
    provider = request.form['provider']
    anime_id = request.form['id']
    redirect
    return redirect(url_for('show_anime_details', provider=provider, id=anime_id))

@app.route('/anime-details/<provider>/<id>')
def show_anime_details(provider, id):
    url = f"{api_base_url}/anime/{provider}/info?id={id}"
    print(url)  # Esta línea imprime la URL correcta
    response = requests.get(url)
    print(response)  # Esta línea imprime el estado de la respuesta (200, 404, etc.)
    anime_data = response.json()
    print(anime_data)  # Esta línea imprime los datos del anime (si los hay)
    return render_template('anime_details.html', anime=anime_data)


def search_anime(query):
    providers = [
        ("AnimeFox", "animefox"),
        ("AnimePahe", "animepahe"),
        ("Crunchyroll", "crunchyroll"),
        ("GogoAnime", "gogoanime"),
        ("Zoro", "zoro")
    ]
    
    results = []
    for provider, endpoint in providers:
        url = f"{api_base_url}/anime/{endpoint}/{query}?page=1"
        response = requests.get(url)
        data = response.json()
        for result in data.get("results", []):
            anime_info = {
                "title": result["title"],
                "image": result.get("image", ""),
                "releaseDate": result.get("releaseDate", ""),
                "subOrDub": result.get("subOrDub", ""),
                "id": result.get("id",""),
                "episodes": result.get("episodes", []),
                "totalEpisodes": result.get("totalEpisodes", "")
            }
            results.append((provider, anime_info))
    return results

@app.route('/watch-episode', methods=['POST'])
def watch_episode():
    episode_id = request.form['episode_id']
    url_format = f"{api_base_url}/anime/zoro/watch?episodeId={episode_id}&server=vidcloud"
    response = requests.get(url_format)
    episode_data = response.json()
    return render_template('watch_episode.html', episode_data=episode_data, episode_id=episode_id)

if __name__ == '__main__':
    app.run(debug=True)
