"""Handle API requests to the OMDB API."""

import os
from dotenv import load_dotenv
import requests

load_dotenv()
API = os.getenv('API')          # Base URL for OMDB API
API_KEY = os.getenv('API_KEY')  # API key for OMDB API


def validate_and_parse_api_response(
        movie_info: dict[str, str]
    ) -> dict[str, str | int | float | None] | None:
    """Validates the response object and return the extracted movie data."""
    if movie_info.get("Response") != "True":
        return None

    title = movie_info.get("Title")
    if not title:
        return None

    try:
        imdb_rating = float(movie_info.get("imdbRating"))
    except (ValueError, TypeError):
        return None

    try:
        year = int(movie_info.get("Year"))
    except (ValueError, TypeError):
        return None

    director = movie_info.get("Director")
    if not director:
        return None

    poster_url = movie_info.get("Poster")

    if poster_url:
        poster_url = poster_url.strip()

    if not poster_url or poster_url == "N/A":
        poster_url = None

    imdb_id = movie_info.get("imdbID")

    return {
        "title": title,
        "year": year,
        "director": director,
        "imdb_rating": imdb_rating,
        "poster_url": poster_url,
        "imdb_id": imdb_id
    }


def make_api_response(params: dict[str, str]) -> requests.Response | None:
    """Gets parameters for the API request and returns a response object if successful."""
    try:
        response = requests.get(API, params=params, timeout=5)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None
    return response


def get_search_api_response(search_title: str) -> requests.Response | None:
    """Send a movie request by search to the API and return a response object if successful."""
    params = {"apikey": API_KEY, "t": search_title, "type": "movie"}
    return make_api_response(params)
