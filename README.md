# 🚀 TikTok AI Streamer Bot v2.5 (Groq Edition)

Bot interaktif untuk TikTok Live yang menggabungkan pembaca chat otomatis dengan suara "Bocil" dan asisten AI pintar dengan suara "Ardi". Dirancang khusus untuk streamer (seperti pemain Minecraft) agar Live menjadi lebih interaktif dan menghibur.

## ✨ Fitur Utama

- **Dual-Voice Interaction**: 
  - **Suara Bocil**: Membacakan komentar penonton secara otomatis dengan nada tinggi (*High Pitch*).
  - **Suara Ardi**: Menjawab komentar menggunakan asisten AI dengan suara normal.
- **Powered by Groq AI**: Menggunakan model `Llama-3.1-8b-instant` untuk respon AI yang super cepat (low latency).
- **In-Memory Audio**: Proses pengolahan suara dilakukan di RAM (BytesIO), sehingga lebih cepat dan tidak membebani Harddisk/SSD.
- **Anti-Delay System**: Secara otomatis melewati antrean chat yang menumpuk jika Live terlalu ramai.
- **Apresiasi Event**: Otomatis menyapa penonton yang bergabung (*Join*) dan berterima kasih saat menerima *Gift*.

## 🛠️ Teknologi yang Digunakan

* [Python 3.10+](https://www.python.org/)
* [TikTokLive](https://github.com/isaackogan/TikTokLive) - Menghubungkan ke API TikTok Live.
* [Groq Cloud SDK](https://groq.com/) - Otak AI (Llama 3.1).
* [Edge-TTS](https://github.com/rany2/edge-tts) - Konversi teks ke suara menggunakan server Microsoft Edge.
* [Pygame](https://www.pygame.org/) - Untuk pemutaran audio yang stabil.

## 🚀 Cara Instalasi

1. **Clone Repository ini:**
   ```bash
   git clone [https://github.com/Taufik908/tiktok-ai-streamer.git](https://github.com/Taufik908/tiktok-ai-streamer.git)
   cd tiktok-ai-streamer

2. **Instal Library yang Dibutuhkan:**
```bash
pip install -r requirements.txt

```


3. **Konfigurasi API Key:**
Buat file bernama `.env` di folder utama dan masukkan API Key kamu:
```env
GROQ_API_KEY=your_groq_api_key_here
TIKTOK_USER=username_tiktok_kamu

```


4. **Jalankan Bot:**
Pastikan akun TikTok kamu sedang **LIVE** sebelum menjalankan bot.
```bash
python main.py

```

## ⚠️ Disclaimer
Penting: Project ini menggunakan library pihak ketiga yang tidak berafiliasi dengan TikTok.

Perubahan API: TikTok dapat mengubah struktur data atau sistem keamanan mereka sewaktu-waktu, yang dapat menyebabkan bot ini berhenti berfungsi hingga library TikTokLive diperbarui.

Risiko Akun: Penggunaan bot otomatis pada platform pihak ketiga memiliki risiko terhadap akun. Gunakan dengan bijak dan tanggung risiko sendiri (Use at your own risk).

Penyalahgunaan: Pengembang tidak bertanggung jawab atas penyalahgunaan kode ini yang melanggar ketentuan layanan platform.

## 📝 Lisensi

Project ini bersifat open-source. Silakan modifikasi sesuai kebutuhan streaming kamu!
