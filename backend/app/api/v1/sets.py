from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

SCRYFALL_SETS_URL = "https://api.scryfall.com/sets"

@router.get("/")
def get_sets():
    try:
        resp = requests.get(
            SCRYFALL_SETS_URL,
            timeout=10
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching sets from Scryfall: {e}"
        )

    data = resp.json().get("data", [])

    sets = [
        {
            "code": s["code"],
            "name": s["name"],
            "released_at": s.get("released_at"),
            "set_type": s.get("set_type"),
        }
        for s in data
        if s.get("set_type") in {"core", "expansion", "masters", "commander"}
    ]

    sets.sort(key=lambda x: x["released_at"] or "", reverse=True)

    return {
        "count": len(sets),
        "data": sets
    }
