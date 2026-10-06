from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.model import (
    recommend_cities,
    recommend_destinations_by_city,
    get_all_destinations,
    get_destination_by_id,
    create_destination,
    update_destination,
    delete_destination,
)

from app.schemas import (
    CityRecommendationRequest,
    DestinationRecommendationRequest,
    DestinationCreate,
    DestinationUpdate,
    DestinationResponse,
    DestinationListResponse,
    MessageResponse,
)


app = FastAPI(
    title="Travel Recommendation API",
    description="REST API untuk sistem rekomendasi destinasi wisata dan pengelolaan data destinasi (CRUD)",
    version="1.1.0"
)


# ==========================================
# EXCEPTION HANDLER
# ==========================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Mengembalikan HTTP 400 saat request payload tidak valid,
    sesuai panduan penanganan error API.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "message": "Data request tidak valid"
        })
    )


# ==========================================
# 1. HEALTH CHECK (EXISTING)
# ==========================================

@app.get(
    "/health",
    summary="Health Check",
    description="Memeriksa status operasional API."
)
def health_check():
    return {
        "status": "success",
        "message": "Travel Recommendation API is running"
    }


# ==========================================
# 2. CRUD DESTINATIONS (NEW)
# ==========================================

@app.get(
    "/destinations",
    response_model=DestinationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Ambil semua destinasi",
    description="Mengambil daftar seluruh destinasi wisata yang tersedia di dalam sistem."
)
def get_destinations_endpoint():
    destinations = get_all_destinations()
    return {
        "destinations": destinations
    }


@app.get(
    "/destinations/{id}",
    response_model=DestinationResponse,
    status_code=status.HTTP_200_OK,
    summary="Ambil satu destinasi berdasarkan ID",
    description="Mengambil detail destinasi wisata tertentu berdasarkan ID unik."
)
def get_destination_by_id_endpoint(id: int):
    destination = get_destination_by_id(id)
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destinasi dengan ID {id} tidak ditemukan"
        )
    return destination


@app.post(
    "/destinations",
    response_model=DestinationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tambah destinasi baru",
    description="Menambahkan data destinasi wisata baru ke dalam dataset CSV. ID dibuat otomatis secara unik (ID terbesar + 1)."
)
def create_destination_endpoint(request: DestinationCreate):
    created = create_destination(request.model_dump())
    return created


@app.put(
    "/destinations/{id}",
    response_model=DestinationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update data destinasi",
    description="Memperbarui data destinasi wisata berdasarkan ID. ID tidak dapat diubah dan tetap terjaga."
)
def update_destination_endpoint(id: int, request: DestinationUpdate):
    updated = update_destination(id, request.model_dump())
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destinasi dengan ID {id} tidak ditemukan"
        )
    return updated


@app.delete(
    "/destinations/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Hapus destinasi berdasarkan ID",
    description="Menghapus destinasi wisata tertentu dari dataset CSV berdasarkan ID unik."
)
def delete_destination_endpoint(id: int):
    success = delete_destination(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destinasi dengan ID {id} tidak ditemukan"
        )
    return {
        "message": "Destination deleted successfully"
    }


# ==========================================
# 3. RECOMMENDATIONS (EXISTING)
# ==========================================

@app.post(
    "/recommend/cities",
    summary="Rekomendasi Kota",
    description="Mendapatkan daftar rekomendasi kota terbaik berdasarkan preferensi minat, aktivitas, dan tipe perjalanan."
)
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


@app.post(
    "/recommend/destinations",
    summary="Rekomendasi Destinasi",
    description="Mendapatkan rekomendasi destinasi wisata spesifik di dalam suatu kota berdasarkan preferensi pengguna."
)
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