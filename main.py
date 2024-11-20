from flask import Flask, request, send_file
import requests
import io


app = Flask(__name__)

@app.route('/proxy_audio')
def proxy_audio():
    url = request.args.get("url")
    filename = request.args.get("filename", "audio.mp3")

    if not url:
        return "URL не указан", 400

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return send_file(
            io.BytesIO(response.content),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=filename
        )
    return "Не удалось скачать файл", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
