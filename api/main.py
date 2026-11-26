from __future__ import annotations

import logging
from typing import Any, Optional, Union

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from api.internship_parser import parse_internship
from api.matcher import rank_internships
from api.models import (
    InternshipDetail,
    StudentProfile,
)
from api.orchestrator import orchestrate_matching
from api.resume_parser import (
    MAX_RESUME_SIZE,
    extract_file_text,
    parse_resume,
)

logger = logging.getLogger(__name__)

MAX_TEXT_LENGTH = 60_000

app = FastAPI(
    title="JobMatch AI API",
    version="0.2.0",
    description="Student-side internship decision-support and eligibility assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class InternshipInput(BaseModel):
    id: Optional[str] = None
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(default="", max_length=200)
    description: str = Field(min_length=1, max_length=20000)
    source_url: Optional[str] = None


class LegacyMatchRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)
    internships: list[InternshipInput] = Field(min_length=1, max_length=20)


class StructuredMatchRequest(BaseModel):
    profile: StudentProfile
    internships: list[InternshipDetail] = Field(min_length=1, max_length=20)


class TextParseRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)


class InternshipParseRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(default="", max_length=200)
    description: str = Field(min_length=1, max_length=20000)
    source_url: Optional[str] = None


def _ensure_text_length(text: str) -> None:
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Resume text exceeds {MAX_TEXT_LENGTH:,} characters. "
                "Please upload a shorter resume or paste only the relevant sections."
            ),
        )


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled server error while processing %s",
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.2.0"}


@app.post("/api/resume/extract")
async def extract_resume(file: UploadFile = File(...)) -> dict[str, Any]:
    filename = file.filename or ""
    try:
        content = await file.read(MAX_RESUME_SIZE + 1)
        text = await run_in_threadpool(extract_file_text, filename, content)
        _ensure_text_length(text)
        profile = await run_in_threadpool(parse_resume, text)
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Failed to parse uploaded resume '%s'", filename)
        raise HTTPException(
            status_code=422, detail="Could not parse the uploaded resume."
        ) from error

    return {
        "text": text,
        "filename": filename,
        "structured_profile": profile.model_dump(),
    }


@app.post("/api/resume/parse-text")
def parse_resume_text(request: TextParseRequest) -> dict[str, Any]:
    try:
        _ensure_text_length(request.text)
        profile = parse_resume(request.text)
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Failed to parse resume text")
        raise HTTPException(
            status_code=422, detail="Could not parse the provided resume text."
        ) from error

    return {
        "structured_profile": profile.model_dump(),
    }


@app.post("/api/internship/extract")
def extract_internship_details(request: InternshipParseRequest) -> dict[str, Any]:
    try:
        detail = parse_internship(
            title=request.title,
            description=request.description,
            company=request.company,
            source_url=request.source_url,
        )
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Failed to parse internship details")
        raise HTTPException(
            status_code=422, detail="Could not parse the internship details."
        ) from error

    return {
        "internship": detail.model_dump(),
    }


@app.post("/api/match")
def match(request: Union[StructuredMatchRequest, LegacyMatchRequest]) -> dict[str, Any]:
    try:
        if isinstance(request, StructuredMatchRequest):
            response = orchestrate_matching(request.profile, request.internships)
            return response.model_dump()

        # Legacy request handling
        raw_internships = [
            internship.model_dump() for internship in request.internships
        ]
        legacy_result = rank_internships(request.resume_text, raw_internships)

        # Also include full structured response
        profile_model = parse_resume(request.resume_text)
        internship_models = [
            parse_internship(
                title=item.get("title", ""),
                description=item.get("description", ""),
                company=item.get("company", ""),
                internship_id=str(idx),
            )
            for idx, item in enumerate(raw_internships)
        ]
        orchestrated = orchestrate_matching(profile_model, internship_models)

        legacy_result["structured_response"] = orchestrated.model_dump()
        return legacy_result
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Failed to complete internship matching")
        raise HTTPException(
            status_code=500, detail="Could not complete matching."
        ) from error


@app.post("/api/reanalyze")
def reanalyze(request: StructuredMatchRequest) -> dict[str, Any]:
    try:
        response = orchestrate_matching(request.profile, request.internships)
        return response.model_dump()
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Failed to complete re-analysis")
        raise HTTPException(
            status_code=500, detail="Could not complete analysis."
        ) from error
