import asyncio
import io
import os
import pygame
import edge_tts
from openai import OpenAI
from dotenv import load_dotenv
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, JoinEvent, GiftEvent

# --- 1. LOAD CONFIG DARI .env ---
load_dotenv()
TIKTOK_USERNAME = os.getenv("TIKTOK_USER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Inisialisasi Groq
client_groq = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Konfigurasi Suara
VOICE_BOCIL = "id-ID-GadisNeural" 
VOICE_NORMAL = "id-ID-ArdiNeural"

pygame.mixer.init()
audio_queue = asyncio.Queue()

# --- 2. AUDIO ENGINE ---

async def worker():
    """Memproses antrean suara satu per satu"""
    while True:
        text, mode = await audio_queue.get()
        
        # Anti-Delay: Skip jika antrean menumpuk > 5
        if audio_queue.qsize() > 5:
            print(f"🗑️ Antrean penuh, skip: {text[:20]}...")
            audio_queue.task_done()
            continue
            
        await generate_and_play(text, mode)
        audio_queue.task_done()

async def generate_and_play(text, mode):
    """Generate suara Edge-TTS ke memori (BytesIO)"""
    try:
        # Karakteristik Suara
        if mode == "bocil":
            voice, pitch, rate = VOICE_BOCIL, "+25Hz", "+20%"
        else:
            voice, pitch, rate = VOICE_NORMAL, "+0Hz", "+12%"

        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        if audio_data:
            f = io.BytesIO(audio_data)
            pygame.mixer.music.load(f)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.05)
            pygame.mixer.music.unload()
    except Exception as e:
        print(f"❌ Audio Error ({mode}): {e}")

# --- 3. AI ENGINE (GROQ) ---

async def get_groq_response(user_text, user_name):
    """Respon pelawak lucu via Llama 3.1"""
    try:
        completion = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Kamu pelawak lucu. Jawab singkat padat (maks 7 kata). Tanpa simbol."},
                {"role": "user", "content": f"{user_name} bilang: {user_text}"}
            ],
            max_tokens=50
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return None

# --- 4. TIKTOK HANDLERS ---

async def handle_interaction(user, msg):
    """Alur Sinkron: Bocil Baca -> Ardi Jawab"""
    print(f"💬 {user}: {msg}")
    
    # 1. Bocil bacain chat
    await audio_queue.put((f"{user} bilang, {msg}", "bocil"))
    
    # 2. Ambil jawaban dari Groq
    jawaban = await get_groq_response(msg, user)
    
    if jawaban:
        print(f"🤖 Ardi: {jawaban}")
        # 3. Ardi menjawab
        await audio_queue.put((jawaban, "normal"))

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    asyncio.create_task(handle_interaction(event.user.nickname, event.comment))

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    if audio_queue.empty():
        await audio_queue.put((f"Halo {event.user.nickname}, selamat datang!", "normal"))

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    print(f"🎁 Gift dari {event.user.nickname}: {event.gift.name}")
    await audio_queue.put((f"Wih! Makasih {event.user.nickname} buat {event.gift.name}-nya!", "normal"))

# --- 5. RUNNER ---

async def main():
    asyncio.create_task(worker())
    print(f"🚀 Bot v2.5 (Groq Edition) Online: {TIKTOK_USERNAME}")
    try:
        await client.connect()
    except Exception as e:
        print(f"❌ Koneksi Gagal: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pygame.quit()
