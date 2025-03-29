from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_media():
    data = request.json
    url = data.get("url")
    output_format = data.get("format", "mp4")

    if not url:
        return jsonify({"error": "Please provide a valid URL!"}), 400

    ydl_opts = {
        'format': 'bestaudio/best' if output_format == "mp3" else 'bestvideo+bestaudio/best',
        'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}] if output_format == "mp3" else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        # Ambil nama file
        filename = os.path.basename(file_path)

        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
