from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List
import re
from bson import ObjectId
from starlette.concurrency import run_in_threadpool
import prototype  # Gemini & LangGraph logic
from db import reviews_collection  # Motor collection

app = FastAPI(title="Code Review API with MongoDB")

class ReviewResponse(BaseModel):
    language_detected: str
    issues: List[str]
    suggestions: List[str]
    improved_code: str
    details: dict

def parse_review(markdown_text: str):
    issues, suggestions, improved_code = [], [], ""
    issues_section = re.search(r"🔍 \*\*Issues Found:\*\*(.*?)(?=✅|\Z)", markdown_text, re.S)
    if issues_section:
        issues = [line.strip("-• ").strip() for line in issues_section.group(1).splitlines() if line.strip()]
    suggestions_section = re.search(r"✅ \*\*Suggestions:\*\*(.*?)(?=📝|\Z)", markdown_text, re.S)
    if suggestions_section:
        suggestions = [line.strip("-• ").strip() for line in suggestions_section.group(1).splitlines() if line.strip()]
    code_section = re.search(r"```.*?\n(.*?)```", markdown_text, re.S)
    if code_section:
        improved_code = code_section.group(1).strip()
    return issues, suggestions, improved_code

@app.post("/review", response_model=ReviewResponse)
async def review_code(code: str = Body(..., media_type="text/plain")):
    try:
        language, _, pyg_lang, pyg_conf, gem_lang, gem_conf = prototype.determine_final_language(code)
        
        review_md = await run_in_threadpool(prototype.generate_review, code, language)
        issues, suggestions, improved_code = parse_review(review_md)

        if not issues and not suggestions:
            raise HTTPException(status_code=500, detail="Failed to parse Gemini review")

        response_data = ReviewResponse(
            language_detected=language,
            issues=issues,
            suggestions=suggestions,
            improved_code=improved_code,
            details={
                "pygments": {"language": pyg_lang, "confidence": pyg_conf},
                "gemini": {"language": gem_lang, "confidence": gem_conf}
            }
        )

        await reviews_collection.insert_one({
            "code": code,
            **response_data.dict()
        })
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reviews")
async def get_all_reviews(limit: int = 100):
    reviews = await reviews_collection.find().to_list(limit)
    for r in reviews:
        r["_id"] = str(r["_id"])
    return reviews

@app.get("/reviews/{review_id}")
async def get_review_by_id(review_id: str):
    query = {}
    try:
        query["_id"] = ObjectId(review_id)
    except:
        query["_id"] = review_id
    review = await reviews_collection.find_one(query)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review["_id"] = str(review["_id"])
    return review

@app.get("/reviews/by-language/{language}")
async def get_reviews_by_language(language: str, limit: int = 100):
    reviews = await reviews_collection.find({"language_detected": language}).to_list(limit)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this language")
    for r in reviews:
        r["_id"] = str(r["_id"])
    return reviews
