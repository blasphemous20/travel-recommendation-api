from pydantic import BaseModel, Field
from typing import List, Literal


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