from flask import Flask, request, jsonify
from urllib.parse import urlparse, parse_qs
from tru import get_transcript

app = Flask(__name__)

def get_video_id(youtube_url):
    try:
        parsed_url = urlparse(youtube_url)
        
        if 'youtu.be' in parsed_url.netloc:
            return parsed_url.path[1:]
        elif 'youtube.com' in parsed_url.netloc:
            if 'shorts' in parsed_url.path:
                return parsed_url.path.split('/')[-1]
            else:
                return parse_qs(parsed_url.query)['v'][0]
    except Exception as e:
        return None

@app.route('/get_transcript', methods=['GET', 'POST'])
def get_transcript_route():
    try:
        url_data = request.get_json()
        youtube_url = url_data.get("url")
        
        if not youtube_url:
            return jsonify({"error": "YouTube URL is required"}), 400
        
        video_id = get_video_id(youtube_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        link = f"https://youtubetotranscript.com/transcript?v={video_id}&current_language_code=en"
        data = get_transcript(link)
        return jsonify({"data": data}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
