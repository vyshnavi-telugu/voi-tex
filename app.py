from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import os

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template("index.html")

# Text-to-Speech endpoint
@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Generate MP3 from text
    tts = gTTS(text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return send_file(mp3_fp, as_attachment=True, download_name="speech.mp3", mimetype="audio/mpeg")

# Audio recording upload endpoint
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    audio_data = BytesIO(audio_file.read())

    try:
        audio_segment = AudioSegment.from_file(audio_data, format="webm")
        mp3_fp = BytesIO()
        audio_segment.export(mp3_fp, format="mp3")
        mp3_fp.seek(0)
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    return send_file(mp3_fp, as_attachment=True, download_name="recording.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True)
