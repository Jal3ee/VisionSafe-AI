from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import cv2  # OpenCV untuk memproses video
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

app = FastAPI()

# Mengizinkan Frontend React untuk mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KONFIGURASI AZURE: MASUKKAN KEY DAN ENDPOINT ANDA DI SINI
AZURE_VISION_KEY = "MASUKKAN_KEY_AZURE_ANDA"
AZURE_VISION_ENDPOINT = "MASUKKAN_ENDPOINT_AZURE_ANDA"

@app.post("/api/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(await file.read())
        temp_video_path = temp_video.name

    try:
        cap = cv2.VideoCapture(temp_video_path)
        
        # --- KODE BARU: Ambil durasi video secara otomatis ---
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Hitung durasi dalam detik (default 15 detik jika gagal terbaca)
        duration_in_seconds = int(frame_count / fps) if fps > 0 else 15 
        
        success, frame = cap.read()
        cap.release()

        if not success:
            return {"status": "error", "message": "Gagal membaca frame dari video."}

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        client = ImageAnalysisClient(endpoint=AZURE_VISION_ENDPOINT, credential=AzureKeyCredential(AZURE_VISION_KEY))
        result = client.analyze(image_data=frame_bytes, visual_features=["Objects"])

        ai_results = []
        if result.objects is not None:
            for idx, obj in enumerate(result.objects.list):
                box = [obj.bounding_box.x, obj.bounding_box.y, obj.bounding_box.width, obj.bounding_box.height]
                label = obj.tags[0].name if obj.tags else "Unknown"
                confidence = round(obj.tags[0].confidence * 100)
                # --- HACKATHON DEMO LOGIC MULTI-CASE (LABORATORY K3) ---
                label_lower = label.lower()
                color = "#00FF00" # Default: Hijau (Aman / Sesuai GLP)
                display_text = f"Safe Object: {label.capitalize()} ({confidence}%)"

                # Case 1: Tidak Pakai APD Lab (Deteksi Manusia)
                if label_lower in ["person", "man", "woman", "human", "boy", "girl"]:
                    color = "#FF0000" # Merah (Kritis)
                    display_text = f"CRITICAL: No Lab Coat / Safety Goggles ({confidence}%)"
                
                # Case 2: Makanan/Minuman di Area Steril (Deteksi Gelas Kopi/Botol Minum/Makanan)
                elif label_lower in ["cup", "coffee cup", "wine glass", "mug", "food", "apple", "sandwich", "bowl"]:
                    color = "#FF0000" # Merah (Kritis)
                    display_text = f"CRITICAL: Food/Drink Detected in Sterile Zone ({confidence}%)"
                
                # Case 3: Area Darurat Terhalang (Deteksi Tas/Kardus di lantai)
                elif label_lower in ["box", "suitcase", "backpack", "luggage", "handbag", "carton"]:
                    color = "#FFFF00" # Kuning (Perhatian)
                    display_text = f"CAUTION: Emergency Equipment/Eyewash Blocked ({confidence}%)"
                
                # Case 4: Pekerja Main HP di Lab (Risiko Kontaminasi)
                elif label_lower in ["cell phone", "mobile phone", "telephone"]:
                    color = "#FFA500" # Oranye (Peringatan)
                    display_text = f"WARNING: Mobile Phone Usage (Contamination Risk) ({confidence}%)"
                
                # Tambahan: Jika mendeteksi botol lab/peralatan (sebagai objek aman)
                elif label_lower in ["bottle", "vase", "jug"]:
                    color = "#00FF00"
                    display_text = f"Lab Equipment Active ({confidence}%)"
                # --- KODE BARU: Looping waktu agar kotak persisten sepanjang video ---
                for t in range(duration_in_seconds + 1):
                    ai_results.append({
                        "time": t, # Akan mencetak detik ke 0, 1, 2, 3... dst
                        "box": box,
                        "label": display_text,
                        "color": color
                    })

        return {"status": "success", "message": "Video dianalisis", "data": ai_results}

    except Exception as e:
        print(f"Error Azure: {e}")
        return {"status": "error", "message": str(e)}
        
    finally:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)