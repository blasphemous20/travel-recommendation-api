import pandas as pd
from pathlib import Path


# ==========================================
# 1. LOAD DATASET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "destinations_clean.csv"

df_destinations = pd.read_csv(DATA_PATH)


# ==========================================
# 2. ACTIVITY MAPPING
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
# 3. TRAVEL TYPE MAPPING
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
# 4. RECOMMEND CITIES
# ==========================================

def recommend_cities(
    interests,
    activity,
    travel_type,
    top_n=5
):
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

    # Ranking kota
    city_scores = city_scores.sort_values(
        "city_score",
        ascending=False
    )

    return city_scores.head(top_n)


# ==========================================
# 5. RECOMMEND DESTINATIONS BY CITY
# ==========================================

def recommend_destinations_by_city(
    city,
    interests,
    activity,
    travel_type,
    top_n=5
):
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

    return result[
        [
            "name",
            "city",
            "country",
            "rating",
            "review_count",
            "score_percent"
        ]
    ]