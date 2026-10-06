from fastapi import FastAPI

from app.model import (
    recommend_cities,
    recommend_destinations_by_city
)

from app.schemas import (
    CityRecommendationRequest,
    DestinationRecommendationRequest
)


app = FastAPI(
    title="Travel Recommendation API",
    description="REST API untuk sistem rekomendasi destinasi wisata",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "Travel Recommendation API is running"
    }


@app.post("/recommend/cities")
def recommend_city_endpoint(
    request: CityRecommendationRequest
):
    result = recommend_cities(
        interests=request.interests,
        activity=request.activity,
        travel_type=request.travel_type,
        top_n=request.top_n
    )

    recommendations = []

    for _, row in result.iterrows():
        recommendations.append({
            "city": row["city"],
            "country": row["country"],
            "score": round(
                row["city_score_percent"], 2
            )
        })

    return {
        "recommendations": recommendations
    }


@app.post("/recommend/destinations")
def recommend_destination_endpoint(
    request: DestinationRecommendationRequest
):
    result = recommend_destinations_by_city(
        city=request.city,
        interests=request.interests,
        activity=request.activity,
        travel_type=request.travel_type,
        top_n=request.top_n
    )

    if result.empty:
        return {
            "city": request.city,
            "recommendations": []
        }

    recommendations = []

    for _, row in result.iterrows():
        recommendations.append({
            "name": row["name"],
            "city": row["city"],
            "country": row["country"],
            "rating": row["rating"],
            "review_count": row["review_count"],
            "score": round(
                row["score_percent"], 2
            )
        })

    return {
        "city": request.city,
        "recommendations": recommendations
    }