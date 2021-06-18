from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/")
async def read_items():
    return {"Hello": "items"}

