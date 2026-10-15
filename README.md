# Travel Recommendation API

REST API untuk sistem rekomendasi destinasi wisata berdasarkan preferensi pengguna.

**Base URL**

`http://127.0.0.1:8000`

> Saat development, API berjalan pada localhost. Ketika API sudah di-deploy ke server, Base URL diganti dengan URL server tersebut.

---

## 1. Health Check

Digunakan untuk memastikan API sedang berjalan.

**Endpoint**

`GET /health`

**Response**

```json
{
  "status": "success",
  "message": "Travel Recommendation API is running"
}
```

---

# 2. Rekomendasi Kota

Endpoint digunakan untuk mendapatkan daftar kota yang paling sesuai dengan preferensi pengguna.

**Endpoint**

`POST /recommend/cities`

### Request

```json
{
  "interests": ["culture", "history"],
  "activity": "Exploration",
  "travel_type": "Solo",
  "top_n": 5
}
```

### Parameter

| Parameter     | Tipe    | Wajib | Keterangan                   |
| ------------- | ------- | ----- | ---------------------------- |
| `interests`   | array   | Ya    | Minat pengguna               |
| `activity`    | string  | Ya    | Aktivitas perjalanan         |
| `travel_type` | string  | Ya    | Jenis perjalanan             |
| `top_n`       | integer | Tidak | Jumlah kota yang ditampilkan |

### Nilai `interests`

```text
culinary
culture
nature
shopping
adventure
history
```

Pengguna dapat memilih lebih dari satu minat.

Contoh:

```json
["culture", "history"]
```

### Nilai `activity`

```text
Relaxing
Exploration
Adventure
```

### Nilai `travel_type`

```text
Solo
Couple
Family
Friends
```

### Response

```json
{
  "recommendations": [
    {
      "city": "Yogyakarta",
      "country": "Indonesia",
      "score": 85.51,
      "description": "Yogyakarta adalah pusat kebudayaan dan sejarah Jawa yang memikat lewat kemegahan Keraton Ngayogyakarta Hadiningrat, keindahan pemandian kuno Taman Sari...",
      "image_url": "https://images.unsplash.com/photo-1584810359583-96fc3448beaa?w=800&auto=format&fit=crop&q=80"
    },
    {
      "city": "Kuala Lumpur",
      "country": "Malaysia",
      "score": 80.3,
      "description": "Kuala Lumpur menggabungkan kemegahan gedung pencakar langit modern seperti Menara KL dan kawasan hijau KLCC Park dengan keindahan warisan budaya...",
      "image_url": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&auto=format&fit=crop&q=80"
    }
  ]
}
```

### Alur penggunaan

Frontend mengirimkan preferensi pengguna ke endpoint `/recommend/cities`.

API kemudian mengembalikan daftar kota berdasarkan skor rekomendasi dari yang tertinggi hingga terendah.

Frontend dapat menampilkan hasil tersebut sebagai pilihan kota kepada pengguna.

---

# 3. Rekomendasi Destinasi

Endpoint digunakan setelah pengguna memilih salah satu kota.

**Endpoint**

`POST /recommend/destinations`

### Request

```json
{
  "city": "Yogyakarta",
  "interests": ["culture", "history"],
  "activity": "Exploration",
  "travel_type": "Solo",
  "top_n": 5
}
```

### Parameter

| Parameter     | Tipe    | Wajib | Keterangan                        |
| ------------- | ------- | ----- | --------------------------------- |
| `city`        | string  | Ya    | Kota yang dipilih pengguna        |
| `interests`   | array   | Ya    | Minat pengguna                    |
| `activity`    | string  | Ya    | Aktivitas perjalanan              |
| `travel_type` | string  | Ya    | Jenis perjalanan                  |
| `top_n`       | integer | Tidak | Jumlah destinasi yang ditampilkan |

### Response

```json
{
  "city": "Yogyakarta",
  "recommendations": [
    {
      "name": "Tourism Zone Malioboro",
      "city": "Yogyakarta",
      "country": "Indonesia",
      "rating": 4.7,
      "review_count": 5489,
      "score": 88.39,
      "description": "Tourism Zone Malioboro merupakan kawasan sentra wisata belanja dan budaya legendaris di jantung Yogyakarta yang dipenuhi pedagang cinderamata, batik, kuliner khas, dan pertunjukan musisi jalanan.",
      "image_url": "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=800&auto=format&fit=crop&q=80"
    },
    {
      "name": "Titik Nol Kilometer Yogyakarta",
      "city": "Yogyakarta",
      "country": "Indonesia",
      "rating": 4.8,
      "review_count": 58874,
      "score": 84.63,
      "description": "Titik Nol Kilometer Yogyakarta merupakan ruang terbuka publik bersejarah di persimpangan jalan utama Yogyakarta...",
      "image_url": "https://images.unsplash.com/photo-1584810359583-96fc3448beaa?w=800&auto=format&fit=crop&q=80"
    }
  ]
}
```

Jika kota tidak ditemukan, API mengembalikan:

```json
{
  "city": "Nama Kota",
  "recommendations": []
}
```

---

# 4. Manajemen Destinasi Wisata (CRUD)

Fitur CRUD untuk mengelola data destinasi wisata secara dinamis. Perubahan data otomatis disimpan ke dataset CSV dan fitur turunan (`category_count`, `review_log`, `rating_norm`, `popularity_norm`) dihitung ulang untuk mendukung sistem rekomendasi.

### 4.1 Ambil Semua Destinasi
- **Method & Endpoint**: `GET /destinations`
- **Response (200 OK)**:
```json
{
  "destinations": [
    {
      "id": 1,
      "name": "Taman Mini Indonesia Indah",
      "city": "Jakarta",
      "country": "Indonesia",
      "rating": 4.6,
      "review_count": 174961,
      "description": "Taman Mini Indonesia Indah (TMII) merupakan kawasan taman rekreasi bertema budaya Indonesia...",
      "image_url": "https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=800&auto=format&fit=crop&q=80"
    }
  ]
}
```

### 4.2 Ambil Destinasi Berdasarkan ID
- **Method & Endpoint**: `GET /destinations/{id}`
- **Response (200 OK)**:
```json
{
  "id": 1,
  "name": "Taman Mini Indonesia Indah",
  "city": "Jakarta",
  "country": "Indonesia",
  "rating": 4.6,
  "review_count": 174961,
  "description": "Taman Mini Indonesia Indah (TMII) merupakan kawasan taman rekreasi bertema budaya Indonesia...",
  "image_url": "https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=800&auto=format&fit=crop&q=80"
}
```

### 4.3 Tambah Destinasi Baru
- **Method & Endpoint**: `POST /destinations`
- **Request Body (JSON)**:
```json
{
  "name": "Kura Kura Ocean Park",
  "city": "Jepara",
  "country": "Indonesia",
  "address": "Pantai Kartini, Jepara, Jawa Tengah",
  "rating": 4.5,
  "review_count": 3200,
  "types": "tourist_attraction, park, aquarium",
  "latitude": -6.5925,
  "longitude": 110.6558,
  "culinary": 0,
  "culture": 0,
  "nature": 1,
  "shopping": 0,
  "adventure": 1,
  "history": 0,
  "family": 1
}
```
- **Response (201 Created)**: Mengembalikan data destinasi dengan `id` unik yang dibuat otomatis (`max(id) + 1`).

### 4.4 Perbarui Destinasi
- **Method & Endpoint**: `PUT /destinations/{id}`
- **Request Body (JSON)**: Sama seperti POST (ID tidak dapat diubah).
- **Response (200 OK)**: Mengembalikan data destinasi yang diperbarui.

### 4.5 Hapus Destinasi
- **Method & Endpoint**: `DELETE /destinations/{id}`
- **Response (200 OK)**:
```json
{
  "message": "Destination deleted successfully"
}
```

### 4.6 Update / Set URL Gambar Destinasi
Digunakan oleh frontend untuk memperbarui atau mengisi foto destinasi secara spesifik tanpa perlu mengirim ulang data lainnya.
- **Method & Endpoint**: `POST /destinations/{id}/image`
- **Request Body (JSON)**:
```json
{
  "image_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1000"
}
```
- **Response (200 OK)**: Mengembalikan data destinasi dengan `image_url` terbaru.

### 4.7 Update / Set Deskripsi Destinasi
Digunakan oleh frontend untuk memperbarui atau mengisi narasi deskripsi destinasi secara spesifik.
- **Method & Endpoint**: `POST /destinations/{id}/description`
- **Request Body (JSON)**:
```json
{
  "description": "Taman Mini Indonesia Indah (TMII) merupakan kawasan taman rekreasi budaya Nusantara..."
}
```
- **Response (200 OK)**: Mengembalikan data destinasi dengan `description` terbaru.

### 4.8 Update / Set Gambar dan Deskripsi Sekaligus
Digunakan oleh frontend jika ingin mengupdate foto dan deskripsi sekaligus dalam satu kali request.
- **Method & Endpoint**: `POST /destinations/{id}/details`
- **Request Body (JSON)**:
```json
{
  "description": "Deskripsi baru...",
  "image_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1000"
}
```
- **Response (200 OK)**: Mengembalikan data destinasi yang diperbarui.

---

# 5. Alur Integrasi Frontend

Frontend dapat menggunakan API dengan alur berikut:

```text
User memilih:
- Interest
- Activity
- Travel Type
        ↓
POST /recommend/cities
        ↓
API mengembalikan Top 5 Kota
        ↓
User memilih salah satu kota
        ↓
POST /recommend/destinations
        ↓
API mengembalikan Top 5 Destinasi
        ↓
Frontend menampilkan rekomendasi
```

---

# 6. Catatan untuk Tim Web

1. `score` merupakan skor rekomendasi dari model dan dapat digunakan untuk mengurutkan hasil.
2. Hasil API sudah diurutkan dari skor tertinggi ke terendah.
3. `top_n` dapat digunakan untuk menentukan jumlah hasil yang ingin ditampilkan.
4. Nilai `interests`, `activity`, dan `travel_type` harus menggunakan pilihan yang telah ditentukan API.
5. Untuk mendapatkan rekomendasi destinasi, frontend harus mengirimkan nama kota yang dipilih pengguna ke `/recommend/destinations`.
6. Pada tahap development, API hanya dapat diakses melalui komputer yang menjalankan server menggunakan: `http://127.0.0.1:8000`.
7. Untuk integrasi dengan frontend pada komputer/server berbeda, API perlu menggunakan alamat host/server yang dapat diakses frontend.

---

# 7. Endpoint Summary

| Method | Endpoint                          | Fungsi                                                    |
| ------ | --------------------------------- | --------------------------------------------------------- |
| GET    | `/health`                         | Mengecek status API                                       |
| GET    | `/destinations`                   | Mengambil seluruh daftar destinasi wisata                 |
| GET    | `/destinations/{id}`              | Mengambil detail destinasi berdasarkan ID                 |
| POST   | `/destinations`                   | Menambahkan destinasi baru (ID otomatis dibuat)           |
| PUT    | `/destinations/{id}`              | Memperbarui seluruh data destinasi berdasarkan ID         |
| DELETE | `/destinations/{id}`              | Menghapus destinasi berdasarkan ID                        |
| POST   | `/destinations/{id}/image`        | Memperbarui/set URL gambar destinasi                      |
| POST   | `/destinations/{id}/description`  | Memperbarui/set deskripsi tempat wisata                   |
| POST   | `/destinations/{id}/details`      | Memperbarui/set gambar & deskripsi destinasi sekaligus    |
| POST   | `/recommend/cities`               | Mendapatkan rekomendasi kota                              |
| POST   | `/recommend/destinations`         | Mendapatkan rekomendasi destinasi berdasarkan kota        |

## Swagger Documentation

FastAPI juga menyediakan dokumentasi interaktif pada:

`http://127.0.0.1:8000/docs`

Tim web dapat menggunakan Swagger untuk mencoba setiap endpoint sebelum melakukan integrasi.
