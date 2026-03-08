from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Senin Bot Bilgilerin
BOT_TOKEN = "8642549149:AAEos9CYfQ0qh8nJMWes1jzUGY0X8wE08CE"
CHAT_ID = "-1003780760904"

@app.route('/')
def home():
    return "PixWatch Kuryesi Calisiyor!"

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'Video dosyası gelmedi!'}), 400

    video = request.files['video']
    video_filename = video.filename.replace(" ", "_")
    
    # Render'da sadece /tmp klasörüne yazma izni vardır
    video_path = os.path.join("/tmp", f"temp_{video_filename}")
    
    video.save(video_path)

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
        with open(video_path, 'rb') as f:
            payload = {'chat_id': CHAT_ID, 'caption': f'🎬 PixWatch Yeni Yükleme: {video_filename}'}
            files = {'video': f}
            r = requests.post(url, data=payload, files=files)
            res_data = r.json()

        # İşlem bitince geçici dosyayı siliyoruz
        if os.path.exists(video_path):
            os.remove(video_path)

        if res_data.get('ok'):
            msg_id = res_data['result']['message_id']
            # Mesaj linkini oluşturuyoruz
            tg_link = f"https://t.me/pixwatch_depo_izmir/{msg_id}"
            return jsonify({
                'status': 'success',
                'video_path': tg_link,
                'thumb_path': 'https://via.placeholder.com/160x90.png?text=PixWatch'
            })
        else:
            return jsonify({'status': 'error', 'message': res_data.get('description')}), 500

    except Exception as e:
        if os.path.exists(video_path): os.remove(video_path)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # RENDER İÇİN EN KRİTİK AYAR: host='0.0.0.0'
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
