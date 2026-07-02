# GigHub API - Admission C027-01-2024/2024

This project is a FastAPI-based backend for managing freelance gig listings in Nairobi.  
It was developed as part of coursework to demonstrate API design and validation using Pydantic.

## Features
- List all gigs with optional filters (category, min/max budget).
- View details of a specific gig by ID.
- Search gigs by title.
- Create a new gig (validated input).
- Update a gig’s budget or status.
- Delete a gig.

## Tech Stack
- Python 3.13
- FastAPI
- Uvicorn

## Running the API
```bash
python -m uvicorn main:app --reload
