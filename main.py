from flask import Flask, request, Response, stream_with_context
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/proxy_audio')
def proxy_audio():
    url = request.args.get("url")
    filename = request.args.get("filename", "audio.mp3")

    if not url:
        return "URL не указан", 400

    encoded_filename = urllib.parse.quote(filename)

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:

            return Response(
                stream_with_context(response.iter_content(chunk_size=4096)),
                headers={
                    "Content-Type": response.headers.get("Content-Type", "application/octet-stream"),
                    "Content-Disposition": f'attachment; filename="{encoded_filename}"',
                },
            )
        return "Не удалось скачать файл", response.status_code
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
