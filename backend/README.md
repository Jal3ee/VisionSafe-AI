# 🛡️ VisionSafe AI

**Proactive GLP & K3 Monitoring System for Pharmaceutical Laboratories**

VisionSafe AI adalah _Command Center_ cerdas berbasis _Computer Vision_ yang dirancang untuk memantau kepatuhan _Good Laboratory Practice_ (GLP) dan Keselamatan Kerja (K3) di fasilitas medis/farmasi secara _real-time_. Ditenagai oleh **Microsoft Azure AI Vision**, sistem ini mengubah kamera pengawas pasif menjadi Auditor Digital 24/7.

## ✨ Fitur Utama

- **GLP & Sterile Zone Monitoring:** Mendeteksi objek pemicu kontaminasi silang (makanan, minuman, penggunaan _smartphone_) di area meja pengujian.
- **Automated Lab PPE Detection:** Memantau kepatuhan penggunaan Alat Pelindung Diri (APD) seperti kacamata pelindung dan jas lab.
- **Emergency Access Tracker:** Mendeteksi rintangan yang menghalangi fasilitas keselamatan darurat (misal: _Emergency Eyewash_).
- **Incident Event Logger:** Mencatat riwayat pelanggaran secara instan sebagai log digital untuk keperluan audit.

## 💻 Teknologi yang Digunakan

- **AI Engine:** Microsoft Azure AI Vision (Image Analysis 4.0)
- **Backend:** Python (FastAPI, OpenCV)
- **Frontend:** React.js, Tailwind CSS

## 🚀 Cara Menjalankan Aplikasi Lokal

### Persyaratan:

1. Python 3.8+
2. Node.js & npm
3. Akun Microsoft Azure (Computer Vision Endpoint & Key)

### Instalasi & Konfigurasi Backend:

1. Buka folder `backend`:
   ```bash
   cd backend
   pip install fastapi uvicorn python-multipart azure-ai-vision-imageanalysis opencv-python
   ```
