from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Senin Bot Bilgilerin
BOT_TOKEN = "8642549149:AAEos9CYfQ0qh8nJMWes1jzUGY0X8wE08CE"
CHAT_ID = "-1003780760904"

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'Video dosyası gelmedi!'}), 400

    video = request.files['video']
    # Dosya adındaki boşlukları temizleyelim
    video_filename = video.filename.replace(" ", "_")
    video_path = os.path.join(os.getcwd(), f"temp_{video_filename}")
    
    video.save(video_path)
    print(f"📥 Video alındı: {video_filename}")

    try:
        print(f"🚀 Telegram'a fırlatılıyor...")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
        
        with open(video_path, 'rb') as f:
            payload = {'chat_id': CHAT_ID, 'caption': f'🎬 PixWatch Yeni Yükleme: {video_filename}'}
            files = {'video': f}
            r = requests.post(url, data=payload, files=files)
            res_data = r.json()

        # Videoyu gönderdikten sonra bilgisayarından siliyoruz (Yer kaplamasın)
        if os.path.exists(video_path):
            os.remove(video_path)

        if res_data.get('ok'):
            msg_id = res_data['result']['message_id']
            # Kanalın linki
            tg_link = f"https://t.me/pixwatch_depo_izmir/{msg_id}"
            print(f"✅ Başarılı! Telegram Linki: {tg_link}")
            
            return jsonify({
                'status': 'success',
                'video_path': tg_link,
                'thumb_path': 'https://via.placeholder.com/160x90.png?text=PixWatch'
            })
        else:
            print(f"❌ Telegram Hatası: {res_data.get('description')}")
            return jsonify({'status': 'error', 'message': res_data.get('description')}), 500

    except Exception as e:
        if os.path.exists(video_path): os.remove(video_path)
        print(f"🔥 Hata: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*40)
    print("🚀 PIXWATCH KURYESİ (PYTHON) BAŞLADI!")
    print("📡 Port: 8000 üzerinden dinliyor...")
    print("="*40 + "\n")
    app.run(port=8000)