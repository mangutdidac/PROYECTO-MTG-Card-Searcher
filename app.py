import os
import streamlit as st
import requests

# Allow overriding backend URL via environment (useful when deploying)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")


# --------------------------
# Load sets (cached) — add timeouts and graceful failures
# --------------------------
@st.cache_data
def load_sets(timeout: int = 5):
    try:
        resp = requests.get(f"{BACKEND_URL}/api/v1/sets", timeout=timeout)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception:
        # If the backend isn't available (e.g. when deploying to Streamlit cloud)
        # return an empty list quickly instead of blocking indefinitely.
        return []

# --------------------------
# Fetch favorites from backend (solo al inicio)
# --------------------------
def fetch_favorites(timeout: int = 5):
    try:
        resp = requests.get(f"{BACKEND_URL}/api/favorites", timeout=timeout)
        resp.raise_for_status()
        return {f["card_id"]: f for f in resp.json()}
    except Exception:
        return {}

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="MTG UnderDeck",
    layout="wide"
)

st.title("MTG UnderDeck - Card Search")

# --------------------------
# Session state init
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "favorites" not in st.session_state:
    try:
        st.session_state.favorites = fetch_favorites()
    except Exception:
        st.session_state.favorites = {}

# --------------------------
# App navigation (Search vs Decks)
# --------------------------
selected_page = st.sidebar.radio("Page", ["Search", "Decks"])

if selected_page == "Decks":
    st.header("Decks")

    # List existing decks
    try:
        resp = requests.get(f"{BACKEND_URL}/api/decks", timeout=5)
        resp.raise_for_status()
        decks = resp.json() or []
    except Exception:
        decks = []

    # Create new deck
    st.subheader("Create deck")
    new_name = st.text_input("Deck name")
    new_desc = st.text_area("Description (optional)")
    if st.button("Create deck") and new_name:
        try:
            # backend expects name as query param
            r = requests.post(f"{BACKEND_URL}/api/decks", params={"name": new_name}, timeout=5)
            r.raise_for_status()
            st.success("Deck created")
            # refresh list
            decks = requests.get(f"{BACKEND_URL}/api/decks", timeout=5).json()
        except Exception as e:
            st.error(f"Couldn't create deck: {e}")

    st.subheader("Your decks")
    deck_map = {f"{d.get('name')} (#{d.get('id')})": d.get('id') for d in decks}
    if deck_map:
        selected_label = st.selectbox("Select deck", list(deck_map.keys()))
        selected_deck_id = deck_map[selected_label]

        # Show deck details
        try:
            deck_resp = requests.get(f"{BACKEND_URL}/api/decks/{selected_deck_id}", timeout=5)
            deck_resp.raise_for_status()
            deck = deck_resp.json()
        except Exception:
            st.error("Couldn't load deck details")
            deck = None

        if deck:
            st.markdown(f"### {deck.get('name')} (#{deck.get('id')})")
            if deck.get('description'):
                st.write(deck.get('description'))

            # Cards in deck
            st.write("Cards")
            cards = deck.get('cards') or []
            for c in cards:
                cols = st.columns([6, 2, 2, 2])
                with cols[0]:
                    st.write(c.get('card_name') or c.get('name') or c.get('card_id'))
                with cols[1]:
                    st.write(f"x{c.get('quantity')}")
                with cols[2]:
                    if st.button(f"-", key=f"dec_{c.get('id')}"):
                        # decrease quantity
                        try:
                            q = max(1, c.get('quantity', 1) - 1)
                            requests.patch(f"{BACKEND_URL}/api/decks/cards/{c.get('id')}", params={"quantity": q}, timeout=5)
                            st.rerun()
                        except Exception:
                            st.error("Couldn't update quantity")
                with cols[3]:
                    if st.button(f"Remove", key=f"rem_{c.get('id')}"):
                        try:
                            requests.delete(f"{BACKEND_URL}/api/decks/cards/{c.get('id')}", timeout=5)
                            st.rerun()
                        except Exception:
                            st.error("Couldn't remove card")

            # Removed inline "Add card to deck" controls here — use the Search page to add cards to decks.

            st.markdown("---")
            if st.button("Delete deck"):
                try:
                    requests.delete(f"{BACKEND_URL}/api/decks/{selected_deck_id}", timeout=5)
                    st.success("Deck deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"Couldn't delete deck: {e}")
    else:
        st.info("No decks yet. Create one above.")

    # stop further rendering of the Search page
    st.stop()

# --------------------------
# Sidebar filters
# --------------------------
st.sidebar.header("Filters")

name_filter = st.sidebar.text_input("Card name")
colors_filter = st.sidebar.multiselect("Colors", ["W", "U", "B", "R", "G"])
rarity_filter = st.sidebar.selectbox(
    "Rarity", ["", "common", "uncommon", "rare", "mythic"]
)

sets_data = load_sets()
set_options = {f"{s['name']} ({s['code'].upper()})": s["code"] for s in sets_data}
selected_sets = st.sidebar.multiselect("Editions", list(set_options.keys()))

card_types = [
    "Creature", "Instant", "Sorcery",
    "Enchantment", "Artifact",
    "Planeswalker", "Land"
]
types_filter = st.sidebar.multiselect("Card Type", card_types)
keywords_filter = st.sidebar.text_input("Keywords (comma separated)")

if st.sidebar.button("Search"):
    st.session_state.page = 1

# --------------------------
# Build query params
# --------------------------
query_params = {"page": st.session_state.page}

if name_filter:
    query_params["name"] = name_filter
if colors_filter:
    query_params["colors"] = ",".join(colors_filter)
if rarity_filter:
    query_params["rarity"] = rarity_filter
if selected_sets:
    query_params["set_code"] = ",".join(set_options[s] for s in selected_sets)
if keywords_filter:
    query_params["keywords"] = keywords_filter
if types_filter:
    query_params["type"] = ",".join(types_filter)

# --------------------------
# Fetch cards
# --------------------------
with st.spinner("Fetching cards..."):
    try:
        # Add a timeout so Streamlit doesn't hang if backend is down.
        resp = requests.get(
            f"{BACKEND_URL}/api/v1/cards/search",
            params=query_params,
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        st.warning("Backend request timed out. Make sure the backend is running.")
        data = {"data": [], "has_more": False}
    except Exception:
        st.info("Use the filters in the sidebar to find your cards.")
        data = {"data": [], "has_more": False}

cards = data.get("data", [])
has_more = data.get("has_more", False)

# Debug: show how many cards were fetched for current filters
try:
    st.sidebar.markdown(f"**Fetched**: `{len(cards)}` cards")
except Exception:
    pass

# --------------------------
# Load user's decks (for quick Add to deck from search results)
# --------------------------
try:
    decks_resp = requests.get(f"{BACKEND_URL}/api/decks", timeout=3)
    decks_resp.raise_for_status()
    decks_list = decks_resp.json() or []
except Exception:
    decks_list = []

deck_map = {f"{d.get('name')} (#{d.get('id')})": d.get('id') for d in decks_list}

if len(cards) == 0:
    # Show query and backend info to help debug empty results
    st.warning("No cards returned for the current filters.")
    st.sidebar.markdown("**Query params**")
    st.sidebar.write(query_params)
    st.sidebar.markdown("**Backend URL**")
    st.sidebar.write(BACKEND_URL)

# --------------------------
# Render cards + favorites toggle
# --------------------------
cols_per_row = 5
favorites = st.session_state.favorites

for i in range(0, len(cards), cols_per_row):
    cols = st.columns(cols_per_row)
    for idx, card in enumerate(cards[i:i + cols_per_row]):
        with cols[idx]:
            image_url = None
            if "image_uris" in card:
                image_url = card["image_uris"].get("normal")
            elif "card_faces" in card:
                image_url = card["card_faces"][0]["image_uris"].get("normal")

            if image_url:
                st.image(image_url, width=200)

            st.write(f"**{card['name']}**")
            st.write(card.get("type_line"))

            card_id = card["id"]
            is_fav = card_id in favorites

            new_state = st.checkbox("❤️", value=is_fav, key=f"fav_{card_id}")

            if new_state != is_fav:
                if new_state:
                    # Añadir a favoritos backend (non-blocking with timeout)
                    try:
                        requests.post(
                            f"{BACKEND_URL}/api/favorites",
                            json={
                                "card_id": card_id,
                                "name": card["name"],
                                "image_url": image_url,
                            },
                            timeout=3,
                        )
                    except Exception:
                        st.warning("Couldn't save favorite to backend; saved locally.")

                    # Añadir a session_state local
                    favorites[card_id] = {
                        "card_id": card_id,
                        "name": card["name"],
                        "image_url": image_url,
                    }
                else:
                    # Quitar de favoritos backend (non-blocking with timeout)
                    try:
                        requests.delete(
                            f"{BACKEND_URL}/api/favorites/{card_id}",
                            timeout=3,
                        )
                    except Exception:
                        st.warning("Couldn't remove favorite from backend; removed locally.")

                    # Quitar de session_state local
                    favorites.pop(card_id, None)

            # --- Add-to-deck UI (always available, independent of favorites change) ---
            show_add_key = f"show_add_{card_id}"
            if show_add_key not in st.session_state:
                st.session_state[show_add_key] = False

            # Toggle the inline add controls
            if st.button("Add to deck", key=f"show_add_btn_{card_id}"):
                st.session_state[show_add_key] = not st.session_state[show_add_key]

            if st.session_state[show_add_key]:
                st.markdown("---")
                if deck_map:
                    deck_label = st.selectbox("Deck", list(deck_map.keys()), key=f"deck_select_{card_id}")
                    selected_deck_id = deck_map.get(deck_label)
                    qty = st.selectbox("Quantity", [1, 2, 3, 4], index=0, key=f"qty_{card_id}")

                    # Disable button when adding to prevent duplicates; use session_state flag per-card
                    adding_key = f"adding_{card_id}"
                    if adding_key not in st.session_state:
                        st.session_state[adding_key] = False

                    add_disabled = bool(st.session_state[adding_key])

                    if st.button("Confirm add", key=f"confirm_add_{card_id}", disabled=add_disabled):
                        # mark in-progress
                        st.session_state[adding_key] = True
                        try:
                            with st.spinner("Adding to deck..."):
                                post_resp = requests.post(
                                    f"{BACKEND_URL}/api/decks/{selected_deck_id}/cards",
                                    params={
                                        "card_id": card_id,
                                        "name": card.get("name"),
                                        "image_url": image_url,
                                        "mana_cost": card.get("mana_cost"),
                                        "colors": ",".join(card.get("color_identity", [])) if card.get("color_identity") else None,
                                        "type_line": card.get("type_line"),
                                    },
                                    timeout=5,
                                )
                                post_resp.raise_for_status()
                                added = post_resp.json()

                                # If user requested more than 1 copy, PATCH to set the quantity (API enforces 1-4)
                                if qty > 1:
                                    deck_card_id = added.get("id")
                                    if deck_card_id:
                                        patch_resp = requests.patch(
                                            f"{BACKEND_URL}/api/decks/cards/{deck_card_id}",
                                            params={"quantity": qty},
                                            timeout=5,
                                        )
                                        patch_resp.raise_for_status()

                            # Successful add — re-fetch decks list and update local selector map (partial refresh)
                            try:
                                decks_resp = requests.get(f"{BACKEND_URL}/api/decks", timeout=3)
                                decks_resp.raise_for_status()
                                decks_list = decks_resp.json() or []
                            except Exception:
                                # keep previous decks_list if refresh fails
                                pass

                            deck_map = {f"{d.get('name')} (#{d.get('id')})": d.get('id') for d in decks_list}

                            st.success(f"Card added: {card.get('name')} x{qty} to {deck_label}")

                            # hide the inline add controls after success
                            st.session_state[show_add_key] = False

                        except requests.exceptions.HTTPError as he:
                            try:
                                detail = post_resp.json().get("detail") if 'post_resp' in locals() else str(he)
                                st.error(detail)
                            except Exception:
                                st.error(str(he))
                        except Exception as e:
                            st.error(f"Couldn't add to deck: {e}")
                        finally:
                            st.session_state[adding_key] = False
                else:
                    st.info("No decks available. Create one in the Decks page.")

# --------------------------
# Pagination
# --------------------------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous") and st.session_state.page > 1:
        st.session_state.page -= 1
        st.rerun()
with col2:
    if st.button("Next") and has_more:
        st.session_state.page += 1
        st.rerun()

# --------------------------
# Favorites section (LOCAL STATE)
# --------------------------
st.markdown("## ❤️ Favorites")
fav_list = list(favorites.values())

for i in range(0, len(fav_list), cols_per_row):
    cols = st.columns(cols_per_row)
    for idx, fav in enumerate(fav_list[i:i + cols_per_row]):
        with cols[idx]:
            if fav.get("image_url"):
                st.image(fav["image_url"], width=200)
            st.write(f"**{fav['name']}**")
