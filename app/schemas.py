from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional


Interest = Literal[
    "culinary",
    "culture",
    "nature",
    "shopping",
    "adventure",
    "history"
]

Activity = Literal[
    "Relaxing",
    "Exploration",
    "Adventure"
]

TravelType = Literal[
    "Solo",
    "Couple",
    "Family",
    "Friends"
]


# ==========================================
# 1. RECOMMENDATION SCHEMAS (EXISTING)
# ==========================================

class CityRecommendationRequest(BaseModel):
    interests: List[Interest] = Field(
        min_length=1,
        description="Contoh: ['culture', 'history']"
    )

    activity: Activity = Field(
        description="Relaxing, Exploration, atau Adventure"
    )

    travel_type: TravelType = Field(
        description="Solo, Couple, Family, atau Friends"
    )

    top_n: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Jumlah kota yang direkomendasikan"
    )


class DestinationRecommendationRequest(BaseModel):
    city: str = Field(
        description="Nama kota, contoh: Yogyakarta"
    )

    interests: List[Interest] = Field(
        min_length=1,
        description="Contoh: ['culture', 'history']"
    )

    activity: Activity = Field(
        description="Relaxing, Exploration, atau Adventure"
    )

    travel_type: TravelType = Field(
        description="Solo, Couple, Family, atau Friends"
    )

    top_n: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Jumlah destinasi yang direkomendasikan"
    )


# ==========================================
# 2. CRUD DESTINATION SCHEMAS (NEW)
# ==========================================

class DestinationBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        description="Nama destinasi wisata (tidak boleh kosong)"
    )
    city: str = Field(
        ...,
        min_length=1,
        description="Kota lokasi destinasi wisata (tidak boleh kosong)"
    )
    country: str = Field(
        ...,
        min_length=1,
        description="Negara lokasi destinasi wisata (tidak boleh kosong)"
    )
    description: Optional[str] = Field(
        default=None,
        description="Deskripsi kota/destinasi untuk kebutuhan website"
    )
    address: str = Field(
        ...,
        description="Alamat lengkap destinasi wisata"
    )
    rating: float = Field(
        ...,
        ge=0.0,
        le=5.0,
        description="Rating destinasi (harus berada pada rentang 0.0 - 5.0)"
    )
    review_count: int = Field(
        ...,
        ge=0,
        description="Jumlah ulasan pengunjung (harus >= 0)"
    )
    types: str = Field(
        default="",
        description="Tipe atau kategori tag destinasi wisata"
    )
    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Garis lintang lokasi valid (-90.0 hingga 90.0)"
    )
    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Garis bujur lokasi valid (-180.0 hingga 180.0)"
    )
    culinary: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori kuliner (0 atau 1)"
    )
    culture: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori budaya (0 atau 1)"
    )
    nature: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori alam (0 atau 1)"
    )
    shopping: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori belanja (0 atau 1)"
    )
    adventure: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori petualangan (0 atau 1)"
    )
    history: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori sejarah (0 atau 1)"
    )
    family: int = Field(
        ...,
        ge=0,
        le=1,
        description="Kategori ramah keluarga (0 atau 1)"
    )

    @field_validator("name", "city", "country")
    @classmethod
    def check_non_empty(cls, value: str, info) -> str:
        if not value or not value.strip():
            raise ValueError(f"{info.field_name} tidak boleh kosong")
        return value.strip()


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(DestinationBase):
    pass


class DestinationResponse(BaseModel):
    id: int = Field(
        ...,
        description="ID unik destinasi"
    )
    name: str = Field(
        ...,
        description="Nama destinasi wisata"
    )
    city: str = Field(
        ...,
        description="Kota destinasi wisata"
    )
    country: str = Field(
        ...,
        description="Negara destinasi wisata"
    )
    rating: float = Field(
        ...,
        description="Rating destinasi"
    )
    review_count: int = Field(
        ...,
        description="Jumlah ulasan pengunjung"
    )
    description: Optional[str] = Field(
        default=None,
        description="Deskripsi kota/destinasi untuk kebutuhan website"
    )


class DestinationListResponse(BaseModel):
    destinations: List[DestinationResponse] = Field(
        ...,
        description="Daftar destinasi wisata"
    )


class MessageResponse(BaseModel):
    message: str = Field(
        ...,
        description="Pesan status operasi"
    )