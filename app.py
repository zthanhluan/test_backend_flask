from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (useful for development)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/convert', methods=['POST'])
def convert_video():
    try:
        data = request.json
        url = data.get('url')
        quality = data.get('quality', '128k')  # Default to 128kbps
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Configure yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality.rstrip('k'),
            }],
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True,
            'cookies_from_browser': ('chrome',),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        return jsonify({
            "message": "Conversion successful",
            "file_name": os.path.basename(file_name),
            "download_url": f"/download/{os.path.basename(file_name)}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
