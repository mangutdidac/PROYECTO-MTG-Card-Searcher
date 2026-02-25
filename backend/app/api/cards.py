from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import requests
import logging

router = APIRouter()

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"


@router.get("/search")
def search_cards(
    name: Optional[str] = None,
    colors: Optional[str] = None,
    rarity: Optional[str] = None,
    set_code: Optional[str] = None,
    keywords: Optional[str] = None,
    card_type: Optional[str] = None,   # <-- renombrado
    page: int = 1
):
    q_parts = []

    # Nombre
    if name:
        q_parts.append(name)

    # Colores (multicolor correcto)
    if colors:
        # Add one color token per selected color. Using 'c:<letter>' for each
        # ensures queries like 'c:u c:w' (cards that are both blue and white)
        for c in colors.split(","):
            q_parts.append(f"c:{c.strip().lower()}")


    # Rareza
    if rarity:
        q_parts.append(f"rarity:{rarity}")

    # Sets
    if set_code:
        sets = [s.strip() for s in set_code.split(",") if s.strip()]
        if sets:
            if len(sets) == 1:
                q_parts.append(f"set:{sets[0]}")
            else:
                # Multiple sets should be OR'ed: card in any of the selected editions
                q_parts.append("(" + " OR ".join(f"set:{s}" for s in sets) + ")")

    # Keywords: treat multiple keywords as OR (match any keyword) and use
    # oracle text search so free-text terms work as users expect.
    if keywords:
        kws = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        if kws:
            if len(kws) == 1:
                q_parts.append(f"oracle:{kws[0].lower()}")
            else:
                q_parts.append("(" + " OR ".join(f"oracle:{kw.lower()}" for kw in kws) + ")")

    # Tipos de carta: multiple selected types should be OR'ed (match any)
    if card_type:
        types = [t.strip() for t in card_type.split(",") if t.strip()]
        if types:
            if len(types) == 1:
                q_parts.append(f"type:{types[0].lower()}")
            else:
                q_parts.append("(" + " OR ".join(f"type:{t.lower()}" for t in types) + ")")

    params = {
        "q": " ".join(q_parts),
        "page": page
    }

    # Log the final Scryfall query for debugging filter issues
    logging.getLogger("mtg_underdeck").info("Scryfall query params: %s", params)

    try:
        # Fetch initial page
        resp = requests.get(SCRYFALL_SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # If exact color matching requested, we will post-filter results to
        # include only cards whose color_identity (or colors) exactly matches
        # the requested set. To increase likelihood of matching results we may
        # fetch additional pages (up to a small limit) and aggregate them.
        if colors:
            requested_colors = [c.strip().upper() for c in colors.split(",") if c.strip()]
            requested_set = set(requested_colors)

            collected = data.get("data", [])[:]  # shallow copy
            has_more = data.get("has_more", False)
            current_page = page
            pages_fetched = 1

            # Fetch additional pages to increase chance of finding exact matches.
            # Increase the page cap so combinations with more colors (e.g. U,R,G)
            # are more likely to appear in the collected set. We still enforce a
            # hard cap to avoid unbounded scans against Scryfall.
            MAX_COLOR_PAGES = 50
            while has_more and pages_fetched < MAX_COLOR_PAGES:
                current_page += 1
                pages_fetched += 1
                params["page"] = current_page
                resp = requests.get(SCRYFALL_SEARCH_URL, params=params, timeout=10)
                resp.raise_for_status()
                next_data = resp.json()
                collected.extend(next_data.get("data", []))
                has_more = next_data.get("has_more", False)

            # Helper to get a card's color identity set
            def card_color_set(card):
                ci = card.get("color_identity")
                if isinstance(ci, list) and ci:
                    return set(x.upper() for x in ci)
                # fallback to 'colors' (face colors) if no color_identity
                colors_field = card.get("colors") or []
                return set(x.upper() for x in colors_field)

            # Filter collected cards to exact color identity match
            filtered = [c for c in collected if card_color_set(c) == requested_set]

            # Replace the returned data and set has_more appropriately (we won't
            # attempt to re-paginate the filtered set; we return what we found)
            data = {
                "data": filtered,
                "has_more": False
            }
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Scryfall query failed: {resp.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected error: {e}"
        )

    return {
        "data": data.get("data", []),
        "has_more": data.get("has_more", False)
    }
