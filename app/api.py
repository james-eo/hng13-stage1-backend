from fastapi import FastAPI, HTTPException, Query, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional
from .services.analyzer import analyze_string, sha256_hash
from .models.file_storage import FileStorage
from .utils.nlp_parser import parse_natural_language
import json

app = FastAPI(
    title="String Analyzer API",
    description="""
    A RESTful API service that analyzes strings and stores their computed properties.
    
    ## Features
    * Create and analyze strings
    * Retrieve stored strings
    * Filter strings by various criteria
    * Natural language query support
    * Delete strings
    
    ## String Properties Computed
    * Length
    * Palindrome detection (case-insensitive)
    * Unique character count
    * Word count
    * SHA-256 hash
    * Character frequency mapping
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
storage = FileStorage()


class StringRequest(BaseModel):
    value: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Custom validation error handler to return proper HTTP codes
    per task requirements
    """
    errors = exc.errors()

    for error in errors:
        error_type = error.get("type")
        error_loc = error.get("loc", [])

        # Check if it's related to the "value" field
        if "value" in error_loc:
            if error_type == "missing":
                # Missing "value" field -> 400 Bad Request
                return JSONResponse(
                    status_code=400,
                    content={
                        "detail": (
                            'Invalid request body or '
                            'missing "value" field'
                        )
                    }
                )
            elif error_type in ["string_type", "str_type"]:
                # Invalid data type for "value" -> 422 Unprocessable Entity
                return JSONResponse(
                    status_code=422,
                    content={
                        "detail": (
                            'Invalid data type for "value" '
                            '(must be string)'
                        )
                    }
                )

    # Default to 400 for other validation errors
    return JSONResponse(
        status_code=400,
        content={
            "detail": 'Invalid request body or missing "value" field'
        }
    )


@app.post("/strings", status_code=201)
async def create_string(request: StringRequest):
    """Create/Analyze String endpoint"""
    string_id = sha256_hash(request.value)

    # Check if string already exists (409 Conflict)
    if storage.exists(string_id):
        raise HTTPException(409, "String already exists in the system")

    # Analyze and store the string
    analyzed_data = analyze_string(request.value)
    storage.save_object(string_id, analyzed_data)

    return analyzed_data


@app.get("/strings/filter-by-natural-language")
async def filter_by_natural_language(query: str = Query(...)):
    """Natural Language Filtering endpoint"""
    try:
        parsed_filters = parse_natural_language(query)

        all_strings = list(storage.all().values())
        filtered_strings = []

        for string_obj in all_strings:
            props = string_obj["properties"]
            match = True

            for filter_key, filter_value in parsed_filters.items():
                if (filter_key == "is_palindrome" and
                        props["is_palindrome"] != filter_value):
                    match = False
                    break
                elif (filter_key == "word_count" and
                        props["word_count"] != filter_value):
                    match = False
                    break
                elif (filter_key == "min_length" and
                        props["length"] < filter_value):
                    match = False
                    break
                elif (filter_key == "contains_character" and
                        filter_value not in string_obj["value"]):
                    match = False
                    break

            if match:
                filtered_strings.append(string_obj)

        return {
            "data": filtered_strings,
            "count": len(filtered_strings),
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed_filters
            }
        }
    except ValueError as e:
        raise HTTPException(
            422,
            "Query parsed but resulted in conflicting filters"
        )
    except Exception as e:
        raise HTTPException(400, "Unable to parse natural language query")


@app.get("/strings/{string_value}")
async def get_string(string_value: str):
    """Get Specific String endpoint"""
    string_id = sha256_hash(string_value)

    if not storage.exists(string_id):
        raise HTTPException(404, "String does not exist in the system")

    return storage.get_object(string_id)


@app.get("/strings")
async def get_all_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None)
):
    """Get All Strings with Filtering endpoint"""
    try:
        all_strings = list(storage.all().values())
        filtered_strings = []

        for string_obj in all_strings:
            props = string_obj["properties"]

            # Apply filters
            if (is_palindrome is not None and
                    props["is_palindrome"] != is_palindrome):
                continue
            if min_length is not None and props["length"] < min_length:
                continue
            if max_length is not None and props["length"] > max_length:
                continue
            if word_count is not None and props["word_count"] != word_count:
                continue
            if (contains_character is not None and
                    contains_character not in string_obj["value"]):
                continue

            filtered_strings.append(string_obj)

        # Build filters_applied object
        filters_applied = {}
        if is_palindrome is not None:
            filters_applied["is_palindrome"] = is_palindrome
        if min_length is not None:
            filters_applied["min_length"] = min_length
        if max_length is not None:
            filters_applied["max_length"] = max_length
        if word_count is not None:
            filters_applied["word_count"] = word_count
        if contains_character is not None:
            filters_applied["contains_character"] = contains_character

        return {
            "data": filtered_strings,
            "count": len(filtered_strings),
            "filters_applied": filters_applied
        }
    except Exception as e:
        raise HTTPException(400, "Invalid query parameter values or types")


@app.delete("/strings/{string_value}", status_code=204)
async def delete_string(string_value: str):
    """Delete String endpoint"""
    string_id = sha256_hash(string_value)

    if not storage.exists(string_id):
        raise HTTPException(404, "String does not exist in the system")

    storage.delete_object(string_id)
    return None
