from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Admission Number: C027-01-1234/2024

app = FastAPI(
    title="GigHub API - Admission C027-01-2424/2024",
    description="API to manage freelance gigs in Nairobi (Admission: C027-01-1234/2024)",
    version="1.0.0"
)

# In-memory "database"
gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a React dashboard for a fintech startup. Must be responsive and mobile-friendly.",
        "category": "Development",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Logo Design for Coffee Shop",
        "description": "Design a modern, minimalistic logo for a new coffee shop in Nairobi.",
        "category": "Design",
        "budget": 500.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Kamau"
    },
    {
        "id": 3,
        "title": "SEO Optimization for Blog",
        "description": "Improve search engine ranking for a lifestyle blog using keyword research and backlinks.",
        "category": "Writing",
        "budget": 8000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Mary Wanjiru"
    },
    {
        "id": 4,
        "title": "Mobile App Bug Fixes",
        "description": "Fix critical bugs in an Android app and improve performance.",
        "category": "Development",
        "budget": 20000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Otieno"
    },
    {
        "id": 5,
        "title": "Social Media Campaign",
        "description": "Run a 2-week campaign on Instagram and Facebook to promote a new product.",
        "category": "Design",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Lucy Mwangi"
    },
    {
        "id": 6,
        "title": "Database Migration",
        "description": "Migrate legacy MySQL database to PostgreSQL with minimal downtime.",
        "category": "Development",
        "budget": 30000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Samuel Kariuki"
    },
    {
        "id": 7,
        "title": "Content Writing for Website",
        "description": "Write 10 SEO-friendly articles for a corporate website.",
        "category": "Writing",
        "budget": 10000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Grace Njeri"
    },
    {
        "id": 8,
        "title": "UI/UX Review",
        "description": "Conduct a usability review of an e-commerce platform and suggest improvements.",
        "category": "Design",
        "budget": 15000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Brian Mwangi"
    },
    {
        "id": 9,
        "title": "API Integration",
        "description": "Integrate a payment gateway API into an existing Django application.",
        "category": "Development",
        "budget": 25000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Alice Wambui"
    }
]

# Model for creating a new gig
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: str = Field(..., pattern="^(Development|Design|Writing)$")
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)

# Model for updating a gig
class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(Open|In Progress|Closed)$")

# 1. List all gigs (with optional filters)
@app.get("/gigs")
def list_gigs(category: Optional[str] = None, min_budget: Optional[float] = None, max_budget: Optional[float] = None):
    results = gigs_db
    if category:
        results = [gig for gig in results if gig["category"].lower() == category.lower()]
    if min_budget:
        results = [gig for gig in results if gig["budget"] >= min_budget]
    if max_budget:
        results = [gig for gig in results if gig["budget"] <= max_budget]
    return results

# 2. View gig by ID
@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    raise HTTPException(status_code=404, detail="Gig not found")

# 3. Search gigs by title
@app.get("/gigs/search")
def search_gigs(q: str):
    return [gig for gig in gigs_db if q.lower() in gig["title"].lower()]

# 4. Create a new gig
@app.post("/gigs")
def create_gig(gig: GigCreate):
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1
    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "USD",  # fixed by admission number
        "status": "Open",
        "client_name": gig.client_name
    }
    gigs_db.append(new_gig)
    return {"message": "Gig created successfully", "gig": new_gig}

# 5. Update gig budget or status
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status
            return {"message": "Gig updated successfully", "gig": gigs_db[index]}
    raise HTTPException(status_code=404, detail="Gig not found")

# 6. Delete a gig
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)
            return {"message": "Gig deleted successfully", "gig": deleted_gig}
    raise HTTPException(status_code=404, detail="Gig not found")
