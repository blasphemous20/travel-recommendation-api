import threading
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


# ==========================================
# 1. LOAD DATASET & PERSISTENCE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "destinations_clean.csv"

_data_lock = threading.Lock()
df_destinations = pd.read_csv(DATA_PATH)

CATEGORY_COLUMNS = [
    "culinary",
    "culture",
    "nature",
    "shopping",
    "adventure",
    "history",
    "family"
]

CITY_DESCRIPTIONS = {
    "Jakarta": (
        "Jakarta merupakan kota metropolitan dinamis yang memadukan wisata sejarah dan budaya di Monas, "
        "Museum Sejarah Jakarta, serta kawasan Kota Tua, dengan beragam rekreasi modern keluarga di Ancol "
        "Taman Impian, Taman Mini Indonesia Indah, hingga Jakarta Aquarium Safari dan taman kota yang asri."
    ),
    "Bandung": (
        "Bandung menyuguhkan pesona wisata alam perbukitan yang sejuk di Tebing Karaton, Dago Dreampark, "
        "dan Tahura Ir. H. Djuanda, berpadu harmonis dengan wisata sejarah Konferensi Asia Afrika, instalasi "
        "seni modern, serta atmosfer jalanan legendaris di kawasan Braga."
    ),
    "Yogyakarta": (
        "Yogyakarta adalah pusat kebudayaan dan sejarah Jawa yang memikat lewat kemegahan Keraton Ngayogyakarta "
        "Hadiningrat, keindahan pemandian kuno Taman Sari, museum bersejarah Benteng Vredeburg dan Sonobudoyo, "
        "serta keramaian ikonik belanja dan seni budaya di kawasan Malioboro."
    ),
    "Surabaya": (
        "Surabaya menawarkan wisata sejarah kepahlawanan yang kaya melalui Monumen Tugu Pahlawan, Museum Sepuluh "
        "Nopember, dan Monumen Kapal Selam, dipadukan dengan keindahan panorama maritim di Surabaya North Quay, "
        "Kenjeran Park, serta ruang publik hijau Taman Bungkul."
    ),
    "Medan": (
        "Medan adalah kota multikultural yang kaya akan peninggalan arsitektur bersejarah seperti Istana Maimun "
        "dan Tjong A Fie Mansion, keberagaman tempat ibadah ikonik di Kuil Shri Mariamman dan Maha Vihara Maitreya, "
        "museum satwa kelas dunia, serta pusat kreativitas Pos Bloc."
    ),
    "Singapore": (
        "Singapore memukau sebagai destinasi modern kelas dunia dengan keajaiban arsitektur futuristik di Gardens "
        "by the Bay, Supertree Grove, dan Marina Bay Sands SkyPark, pemandangan ikonik Merlion Park dan Singapore "
        "Flyer, hingga petualangan satwa nokturnal di Night Safari."
    ),
    "Kuala Lumpur": (
        "Kuala Lumpur menggabungkan kemegahan gedung pencakar langit modern seperti Menara KL dan kawasan hijau "
        "KLCC Park dengan keindahan warisan budaya di Batu Caves, Kuil Thean Hou, arsitektur kolonial Dataran Merdeka, "
        "serta keasrian taman burung KL Bird Park."
    ),
    "Penang": (
        "Penang adalah pulau warisan dunia UNESCO yang terkenal dengan seni mural jalanan George Town, kemegahan kuil "
        "Buddha Kek Lok Si, pesona rumah terapung Clan Jetties, kemewahan sejarah Pinang Peranakan Mansion, serta "
        "rekreasi alam tropis di Entopia dan Spice Garden."
    ),
    "Bangkok": (
        "Bangkok menghadirkan perpaduan spektakuler antara keagungan istana dan kuil emas The Grand Palace serta "
        "Wat Phra Kaew, semarak kuliner dan budaya jalanan di Chinatown Yaowarat, ruang seni kontemporer BACC, "
        "hingga atraksi akuarium raksasa SEA LIFE Bangkok."
    ),
    "Manila": (
        "Manila menyajikan napak tilas sejarah kolonial Spanyol yang memikat di dalam benteng kuno Fort Santiago, "
        "kawasan walled-city Intramuros, gereja batu San Agustin, keindahan karya seni National Museum of Fine Arts, "
        "hingga rekreasi keluarga di Manila Ocean Park dan Rizal Park."
    ),
    "Seoul": (
        "Seoul menawarkan harmoni sempurna antara kemegahan istana Dinasti Joseon di Changdeokgung dan lorong "
        "tradisional Bukchon Hanok Village, dengan pesona gemerlap kota modern di N Seoul Tower, surga belanja "
        "Myeongdong, serta keseruan taman hiburan Lotte World."
    )
}

CITY_IMAGES = {
    "Jakarta": "https://images.unsplash.com/photo-1555899434-94d1368aa7af?w=800&auto=format&fit=crop&q=80",
    "Bandung": "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?w=800&auto=format&fit=crop&q=80",
    "Yogyakarta": "https://images.unsplash.com/photo-1584810359583-96fc3448beaa?w=800&auto=format&fit=crop&q=80",
    "Surabaya": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?w=800&auto=format&fit=crop&q=80",
    "Medan": "https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=800&auto=format&fit=crop&q=80",
    "Singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&auto=format&fit=crop&q=80",
    "Kuala Lumpur": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&auto=format&fit=crop&q=80",
    "Penang": "https://images.unsplash.com/photo-1571210862729-78a52d3779a2?w=800&auto=format&fit=crop&q=80",
    "Bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&auto=format&fit=crop&q=80",
    "Manila": "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&auto=format&fit=crop&q=80",
    "Seoul": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=800&auto=format&fit=crop&q=80"
}


def get_destination_image(data_or_row: dict) -> str:
    """Mengembalikan URL foto placeholder Unsplash berkualitas tinggi sesuai jenis destinasi."""
    name = str(data_or_row.get("name", "")).lower()
    types = str(data_or_row.get("types", "")).lower()
    text = name + " " + types

    if any(k in text for k in ["aquarium", "ocean park", "sea life", "water"]):
        return "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["taman mini", "ancol", "lotte world", "dino", "theme park", "amusement"]):
        return "https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["bird", "zoo", "safari", "wildlife", "butterfly"]):
        return "https://images.unsplash.com/photo-1555169062-013468b47731?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["pantai", "beach", "quay", "jetty", "jetties", "harbor"]):
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["masjid", "mosque"]):
        return "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["temple", "vihara", "kuil", "wat", "church", "gereja", "katedral", "shrine"]):
        return "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["palace", "istana", "keraton", "throne"]):
        return "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["menara", "tower", "skywalk", "skypark", "flyer", "supertree", "helix", "deck"]):
        return "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["mural", "street art", "art & culture", "bloc", "cyber", "village", "hanok"]):
        return "https://images.unsplash.com/photo-1561055657-b9e0bf0fa360?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["malioboro", "myeongdong", "market", "shopping", "chinatown", "slasar", "braga"]):
        return "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["tebing", "hutan", "forest", "botanic", "garden", "park", "taman", "kawah", "flower dome"]):
        return "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&auto=format&fit=crop&q=80"
    if any(k in text for k in ["museum", "monumen", "monument", "statue", "arca", "mansion", "benteng", "fort", "kapal selam"]):
        return "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?w=800&auto=format&fit=crop&q=80"
    return CITY_IMAGES.get(data_or_row.get("city"), "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop&q=80")


def recalculate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menghitung ulang fitur turunan ketika dataset berubah:
    1. category_count = penjumlahan kolom kategori (culinary, culture, nature, shopping, adventure, history, family)
    2. review_log = log1p(review_count)
    3. rating_norm = MinMax scaling rating terhadap seluruh dataset
    4. popularity_norm = MinMax scaling review_log terhadap seluruh dataset
    """
    if df.empty:
        return df

    # 1. category_count
    df["category_count"] = df[CATEGORY_COLUMNS].sum(axis=1).astype(int)

    # 2. review_log
    df["review_log"] = np.log1p(df["review_count"].astype(float))

    # 3. rating_norm
    rating_min = df["rating"].min()
    rating_max = df["rating"].max()
    if rating_max > rating_min:
        df["rating_norm"] = (df["rating"] - rating_min) / (rating_max - rating_min)
    else:
        df["rating_norm"] = 1.0

    # 4. popularity_norm
    rev_log_min = df["review_log"].min()
    rev_log_max = df["review_log"].max()
    if rev_log_max > rev_log_min:
        df["popularity_norm"] = (df["review_log"] - rev_log_min) / (rev_log_max - rev_log_min)
    else:
        df["popularity_norm"] = 1.0

    return df


def _save_and_sync(df: pd.DataFrame):
    """
    Menyimpan perubahan ke file destinations_clean.csv dan memperbarui variabel memori df_destinations.
    Harus dipanggil di dalam _data_lock.
    """
    global df_destinations
    df.to_csv(DATA_PATH, index=False)
    df_destinations = df.copy()


# ==========================================
# 2. CRUD OPERATIONS
# ==========================================

def get_all_destinations() -> List[Dict[str, Any]]:
    """Mengambil daftar semua destinasi wisata dari dataset."""
    with _data_lock:
        records = []
        for _, row in df_destinations.iterrows():
            item = {
                "id": int(row["id"]),
                "name": str(row["name"]),
                "city": str(row["city"]),
                "country": str(row["country"]),
                "rating": float(row["rating"]),
                "review_count": int(row["review_count"]),
            }
            if "description" in row and pd.notna(row["description"]):
                item["description"] = str(row["description"])
            if "image_url" in row and pd.notna(row["image_url"]):
                item["image_url"] = str(row["image_url"])
            records.append(item)
        return records


def get_destination_by_id(destination_id: int) -> Optional[Dict[str, Any]]:
    """Mengambil satu destinasi wisata berdasarkan ID."""
    with _data_lock:
        matches = df_destinations[df_destinations["id"] == destination_id]
        if matches.empty:
            return None
        row = matches.iloc[0]
        item = {
            "id": int(row["id"]),
            "name": str(row["name"]),
            "city": str(row["city"]),
            "country": str(row["country"]),
            "rating": float(row["rating"]),
            "review_count": int(row["review_count"]),
        }
        if "description" in row and pd.notna(row["description"]):
            item["description"] = str(row["description"])
        if "image_url" in row and pd.notna(row["image_url"]):
            item["image_url"] = str(row["image_url"])
        return item


def create_destination(data: dict) -> Dict[str, Any]:
    """
    Menambahkan destinasi baru.
    ID otomatis dibuat: integer terbesar + 1 (mencegah duplikat).
    Menghitung ulang fitur dan menyimpan ke CSV.
    """
    with _data_lock:
        global df_destinations
        if df_destinations.empty or "id" not in df_destinations.columns:
            new_id = 1
        else:
            new_id = int(df_destinations["id"].max()) + 1

        desc = data.get("description") or CITY_DESCRIPTIONS.get(data["city"], "")
        img_url = data.get("image_url") or get_destination_image(data)

        new_row = {
            "id": new_id,
            "name": data["name"],
            "city": data["city"],
            "country": data["country"],
            "description": desc,
            "image_url": img_url,
            "address": data["address"],
            "rating": float(data["rating"]),
            "review_count": int(data["review_count"]),
            "types": data.get("types", ""),
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"]),
            "culinary": int(data["culinary"]),
            "culture": int(data["culture"]),
            "nature": int(data["nature"]),
            "shopping": int(data["shopping"]),
            "adventure": int(data["adventure"]),
            "history": int(data["history"]),
            "family": int(data["family"]),
        }

        new_df = pd.concat([df_destinations, pd.DataFrame([new_row])], ignore_index=True)
        new_df = recalculate_features(new_df)
        _save_and_sync(new_df)

        return {
            "id": new_id,
            "name": new_row["name"],
            "city": new_row["city"],
            "country": new_row["country"],
            "rating": new_row["rating"],
            "review_count": new_row["review_count"],
            "description": new_row["description"],
            "image_url": new_row["image_url"],
        }


def update_destination(destination_id: int, data: dict) -> Optional[Dict[str, Any]]:
    """
    Memperbarui destinasi berdasarkan ID.
    ID tidak boleh diubah.
    Menghitung ulang fitur dan menyimpan ke CSV.
    """
    with _data_lock:
        global df_destinations
        matches = df_destinations.index[df_destinations["id"] == destination_id].tolist()
        if not matches:
            return None
        idx = matches[0]

        df = df_destinations.copy()
        df.loc[idx, "name"] = data["name"]
        df.loc[idx, "city"] = data["city"]
        df.loc[idx, "country"] = data["country"]
        if "description" in data and data["description"]:
            df.loc[idx, "description"] = data["description"]
        elif "description" not in df.columns or pd.isna(df.loc[idx, "description"]):
            df.loc[idx, "description"] = CITY_DESCRIPTIONS.get(data["city"], "")

        if "image_url" in data and data["image_url"]:
            df.loc[idx, "image_url"] = data["image_url"]
        elif "image_url" not in df.columns or pd.isna(df.loc[idx, "image_url"]):
            df.loc[idx, "image_url"] = get_destination_image(data)

        df.loc[idx, "address"] = data["address"]
        df.loc[idx, "rating"] = float(data["rating"])
        df.loc[idx, "review_count"] = int(data["review_count"])
        df.loc[idx, "types"] = data.get("types", "")
        df.loc[idx, "latitude"] = float(data["latitude"])
        df.loc[idx, "longitude"] = float(data["longitude"])
        df.loc[idx, "culinary"] = int(data["culinary"])
        df.loc[idx, "culture"] = int(data["culture"])
        df.loc[idx, "nature"] = int(data["nature"])
        df.loc[idx, "shopping"] = int(data["shopping"])
        df.loc[idx, "adventure"] = int(data["adventure"])
        df.loc[idx, "history"] = int(data["history"])
        df.loc[idx, "family"] = int(data["family"])

        df = recalculate_features(df)
        _save_and_sync(df)

        return {
            "id": destination_id,
            "name": data["name"],
            "city": data["city"],
            "country": data["country"],
            "rating": float(data["rating"]),
            "review_count": int(data["review_count"]),
            "description": str(df.loc[idx, "description"]) if "description" in df.columns and pd.notna(df.loc[idx, "description"]) else "",
            "image_url": str(df.loc[idx, "image_url"]) if "image_url" in df.columns and pd.notna(df.loc[idx, "image_url"]) else "",
        }


def delete_destination(destination_id: int) -> bool:
    """
    Menghapus destinasi berdasarkan ID.
    Menghitung ulang fitur pada sisa dataset dan menyimpan ke CSV.
    """
    with _data_lock:
        global df_destinations
        matches = df_destinations.index[df_destinations["id"] == destination_id].tolist()
        if not matches:
            return False

        df = df_destinations.drop(index=matches[0]).reset_index(drop=True)
        df = recalculate_features(df)
        _save_and_sync(df)
        return True


# ==========================================
# 3. ACTIVITY MAPPING
# ==========================================

activity_mapping = {
    "Relaxing": [
        "nature",
        "culture"
    ],
    "Exploration": [
        "culture",
        "history",
        "shopping"
    ],
    "Adventure": [
        "adventure",
        "nature"
    ]
}


# ==========================================
# 4. TRAVEL TYPE MAPPING
# ==========================================

travel_type_mapping = {
    "Solo": [
        "culture",
        "history",
        "shopping",
        "adventure"
    ],
    "Couple": [
        "nature",
        "culture",
        "culinary"
    ],
    "Family": [
        "family",
        "nature",
        "adventure"
    ],
    "Friends": [
        "adventure",
        "shopping",
        "culinary"
    ]
}


# ==========================================
# 5. RECOMMEND CITIES
# ==========================================

def recommend_cities(
    interests,
    activity,
    travel_type,
    top_n=5
):
    with _data_lock:
        df = df_destinations.copy()

    # Interest Match
    df["interest_match"] = (
        df[interests].sum(axis=1) / len(interests)
    )

    # Activity Match
    activity_categories = activity_mapping.get(
        activity,
        []
    )

    if activity_categories:
        df["activity_match"] = (
            df[activity_categories].sum(axis=1)
            / len(activity_categories)
        )
    else:
        df["activity_match"] = 0

    # Travel Type Match
    travel_categories = travel_type_mapping.get(
        travel_type,
        []
    )

    if travel_categories:
        df["travel_type_match"] = (
            df[travel_categories].sum(axis=1)
            / len(travel_categories)
        )
    else:
        df["travel_type_match"] = 0

    # Weighted Score
    df["score"] = (
        (df["interest_match"] * 0.40) +
        (df["activity_match"] * 0.15) +
        (df["travel_type_match"] * 0.15) +
        (df["rating_norm"] * 0.15) +
        (df["popularity_norm"] * 0.15)
    )

    # Ambil 3 destinasi terbaik dari setiap kota
    top_destinations = (
        df.sort_values(
            ["city", "score"],
            ascending=[True, False]
        )
        .groupby("city")
        .head(3)
    )

    # Hitung skor kota
    city_scores = (
        top_destinations
        .groupby(
            ["city", "country"],
            as_index=False
        )
        .agg(
            city_score=("score", "mean"),
            best_destination_score=("score", "max")
        )
    )

    city_scores["city_score_percent"] = (
        city_scores["city_score"] * 100
    )

    city_scores["description"] = city_scores["city"].map(CITY_DESCRIPTIONS).fillna("")
    city_scores["image_url"] = city_scores["city"].map(CITY_IMAGES).fillna("")

    # Ranking kota
    city_scores = city_scores.sort_values(
        "city_score",
        ascending=False
    )

    return city_scores.head(top_n)


# ==========================================
# 6. RECOMMEND DESTINATIONS BY CITY
# ==========================================

def recommend_destinations_by_city(
    city,
    interests,
    activity,
    travel_type,
    top_n=5
):
    with _data_lock:
        df = df_destinations.copy()

    # Filter berdasarkan kota
    df = df[
        df["city"].str.lower() == city.lower()
    ].copy()

    if df.empty:
        return pd.DataFrame()

    # Interest Match
    df["interest_match"] = (
        df[interests].sum(axis=1) / len(interests)
    )

    # Activity Match
    activity_categories = activity_mapping.get(
        activity,
        []
    )

    if activity_categories:
        df["activity_match"] = (
            df[activity_categories].sum(axis=1)
            / len(activity_categories)
        )
    else:
        df["activity_match"] = 0

    # Travel Type Match
    travel_categories = travel_type_mapping.get(
        travel_type,
        []
    )

    if travel_categories:
        df["travel_type_match"] = (
            df[travel_categories].sum(axis=1)
            / len(travel_categories)
        )
    else:
        df["travel_type_match"] = 0

    # Weighted Score
    df["score"] = (
        (df["interest_match"] * 0.40) +
        (df["activity_match"] * 0.15) +
        (df["travel_type_match"] * 0.15) +
        (df["rating_norm"] * 0.15) +
        (df["popularity_norm"] * 0.15)
    )

    df["score_percent"] = df["score"] * 100

    # Ranking destinasi
    result = df.sort_values(
        "score",
        ascending=False
    ).head(top_n)

    cols = [
        "name",
        "city",
        "country",
        "rating",
        "review_count",
        "score_percent"
    ]
    if "description" in result.columns:
        cols.append("description")
    if "image_url" in result.columns:
        cols.append("image_url")

    return result[cols]