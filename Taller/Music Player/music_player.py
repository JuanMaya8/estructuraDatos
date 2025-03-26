from flask import Flask, render_template, request, jsonify
import pygame
import os
from PIL import Image

app = Flask(__name__)
pygame.mixer.init()

# Rutas de archivos
MUSIC_FOLDER = r"C:\Users\Acer\OneDrive - Universidad Cooperativa de Colombia\S4\Estructura de datos\Listas dobles\Taller\Music Player\static\music"
COVERS_FOLDER = "static/covers"  # Carpeta donde se guardan las carátulas

# Lista de canciones con carátulas asociadas
songs = [
    {"title": "Prrum - Cosculluela", "file": "05 - Cosculluela - Prrum_160k.mp3", "cover": "prrum.jpg"},
    {"title": "Pobre diabla - Don omar", "file": "Don Omar - Pobre Diabla (Original Version)_160k.mp3", "cover": "pobrediabla.jpg"},
    {"title": "Salio el sol - Don omar", "file": "Don Omar - Salio El Sol (Official Music Video).mp3", "cover": "salioelsol.jpg"},
    {"title": "Don omar RKT - Gon RMX", "file": "DON OMAR RKT - GON RMX.mp3", "cover": "donomarrkt.jpg"},
    {"title": "Gasolina - Daddy Yankee", "file": "Gasolina_160k.mp3", "cover": "gasolina.jpg"},
    {"title": "El telefono - Hector el Bambino", "file": "Hector Bambino EL Father & Wisin & Yandel - El Teléfono.mp3", "cover": "eltelefono.jpg"},
    {"title": "Candy - Plan B", "file": "Plan B - Candy Official Audio _160k.mp3", "cover": "candy.jpg"},
    {"title": "Choca - Plan B", "file": "Plan B - Choca.mp3", "cover": "choca.jpg"},
    {"title": "Solos - Tony Dize", "file": "Tony Dize - Solos ft. Plan B.mp3", "cover": "solos.jpg"},
    {"title": "Abusadora - Wisin & Yandel", "file": "Wisin & Yandel - Abusadora_160k.mp3", "cover": "abusadora.jpg"}
]

# Redimensionar imágenes a 300x300
def resize_images():
    for song in songs:
        cover_path = os.path.join(COVERS_FOLDER, song["cover"])
        if os.path.exists(cover_path):
            img = Image.open(cover_path)
            img = img.resize((300, 300))
            img.save(cover_path)

resize_images()

# Clase para manejar la lista de reproducción
class TrackList:
    def __init__(self, tracks):
        self.tracks = tracks
        self.index = 0 if tracks else -1

    def current_track(self):
        return self.tracks[self.index] if self.index >= 0 else None

    def next_track(self):
        if self.index < len(self.tracks) - 1:
            self.index += 1
        else:
            self.index = 0
        return self.current_track()

    def prev_track(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = len(self.tracks) - 1
        return self.current_track()
    
    def add_track(self, track, position=None):
        if position is None or position >= len(self.tracks):
            self.tracks.append(track)
        elif position <= 0:
            self.tracks.insert(0, track)
        else:
            self.tracks.insert(position, track)

    def remove_track(self, position=None, title=None):
        if title:
            self.tracks = [track for track in self.tracks if track["title"] != title]
        elif position is not None and 0 <= position < len(self.tracks):
            del self.tracks[position]
    

playlist = TrackList(songs)

# Función para reproducir una canción
def play_track(track):
    pygame.mixer.music.stop()  # Detiene la canción en curso
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, track["file"]))
    pygame.mixer.music.play()

# Ruta principal para renderizar la interfaz con las canciones y carátulas
@app.route('/')
def index():
    return render_template('index.html', tracks=songs, covers_folder=COVERS_FOLDER)

# Ruta para reproducir una canción seleccionada
@app.route('/play_selected', methods=['GET'])
def play_selected():
    track_file = request.args.get('track')
    track_title = request.args.get('title')
    track_cover = request.args.get('cover')
    
    # Buscar la canción en la lista
    track = next((t for t in songs if t["file"] == track_file), None)
    
    if track:
        play_track(track)
        return jsonify({'status': 'playing', 'track': track_title, 'cover': track_cover})
    return jsonify({'status': 'error', 'message': 'Track not found'})

# Control de reproducción
@app.route('/play', methods=['GET'])
def play():
    track = playlist.current_track()
    if track:
        play_track(track)
        return jsonify({'status': 'playing', 'track': track["title"], 'cover': track["cover"]})
    return jsonify({'status': 'no tracks'})

@app.route('/pause', methods=['GET'])
def pause():
    pygame.mixer.music.pause()
    return jsonify({'status': 'paused'})

@app.route('/unpause', methods=['GET'])
def unpause():
    pygame.mixer.music.unpause()
    return jsonify({'status': 'playing'})

@app.route('/next', methods=['GET'])
def next_track():
    track = playlist.next_track()
    if track:
        play_track(track)
        return jsonify({'status': 'playing', 'track': track["title"], 'cover': track["cover"]})
    return jsonify({'status': 'error', 'message': 'No next track found'})

@app.route('/prev', methods=['GET'])
def prev_track():
    track = playlist.prev_track()
    if track:
        play_track(track)
        return jsonify({'status': 'playing', 'track': track["title"], 'cover': track["cover"]})
    return jsonify({'status': 'error', 'message': 'No previous track found'})

# Obtener el progreso de la canción en reproducción
@app.route('/get_progress', methods=['GET'])
def get_progress():
    current_time = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
    duration = pygame.mixer.music.get_length()  # Total song duration
    progress_percentage = (current_time / duration) * 100 if duration > 0 else 0
    return jsonify({'current_time': current_time, 'duration': duration, 'progress_percentage': progress_percentage})

@app.route('/add_song', methods=['POST'])
def add_song():
    data = request.json
    new_track = {"title": data["title"], "file": data["file"], "cover": data["cover"]}
    playlist.add_track(new_track, data.get("position"))
    return jsonify({'status': 'success', 'message': 'Song added successfully'})

@app.route('/add_song_first', methods=['POST'])
def add_song_first():
    data = request.json
    new_track = {"title": data["title"], "file": data["file"], "cover": data["cover"]}
    
    playlist.add_track(new_track, position=0)  # Insertar al inicio de la lista
    
    return jsonify({'status': 'success', 'message': 'Song added at the beginning'})

@app.route('/add_song_at_position', methods=['POST'])
def add_song_at_position():
    data = request.json
    new_track = {"title": data["title"], "file": data["file"], "cover": data["cover"]}
    
    # Obtener la posición, si no se envía, se agrega al final
    position = data.get("position")
    
    try:
        position = int(position)
    except (TypeError, ValueError):
        position = None  # Si la posición no es válida, agregar al final
    
    playlist.add_track(new_track, position)
    
    return jsonify({'status': 'success', 'message': f'Song added at position {position}'})

@app.route('/remove_song', methods=['DELETE'])
def remove_song():
    file_to_remove = request.args.get('file')

    if not file_to_remove:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400

    global songs
    songs = [track for track in songs if track["file"] != file_to_remove]
    
    playlist.tracks = songs  # Actualizar la lista en TrackList

    return jsonify({'status': 'success', 'message': f'Song {file_to_remove} removed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
