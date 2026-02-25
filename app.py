import os
import streamlit as st
import requests
import pandas as pd
import json

# --------------------------
# Config backend
# --------------------------
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# --------------------------
# Load sets (cached)
# --------------------------
@st.cache_data
def load_sets(timeout: int = 5):
    try:
        resp = requests.get(f"{BACKEND_URL}/api/v1/sets", timeout=timeout)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception:
        return []

# --------------------------
# Fetch favorites
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
st.set_page_config(page_title="MTG UnderDeck", layout="wide")
st.title("MTG UnderDeck - Card Search")

# --------------------------
# Session state init
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "favorites" not in st.session_state:
    st.session_state.favorites = fetch_favorites()

# --------------------------
# Sidebar filters
# --------------------------
st.sidebar.header("Filters")
name_filter = st.sidebar.text_input("Card name")
colors_filter = st.sidebar.multiselect("Colors", ["W", "U", "B", "R", "G"])
rarity_filter = st.sidebar.selectbox("Rarity", ["", "common", "uncommon", "rare", "mythic"])

sets_data = load_sets()
set_options = {f"{s['name']} ({s['code'].upper()})": s["code"] for s in sets_data}
selected_sets = st.sidebar.multiselect("Editions", list(set_options.keys()))

card_types = ["Creature", "Instant", "Sorcery", "Enchantment", "Artifact", "Planeswalker", "Land"]
types_filter = st.sidebar.multiselect("Card Type", card_types)
keywords_filter = st.sidebar.text_input("Keywords (comma separated)")

if st.sidebar.button("Search"):
    st.session_state.page = 1

# --------------------------
# Build query params
# --------------------------
query_params = {"page": st.session_state.page}
if name_filter: query_params["name"] = name_filter
if colors_filter: query_params["colors"] = ",".join(colors_filter)
if rarity_filter: query_params["rarity"] = rarity_filter
if selected_sets: query_params["set_code"] = ",".join(set_options[s] for s in selected_sets)
if keywords_filter: query_params["keywords"] = keywords_filter
if types_filter: query_params["card_type"] = ",".join(types_filter)

# --------------------------
# Fetch cards
# --------------------------
with st.spinner("Fetching cards..."):
    try:
        resp = requests.get(f"{BACKEND_URL}/api/v1/cards/search", params=query_params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        st.info("Use the filters in the sidebar to find your cards.")
        data = {"data": [], "has_more": False}

cards = data.get("data", [])
has_more = data.get("has_more", False)

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
# Render cards + favorites toggle
# --------------------------
cols_per_row = 5
favorites = st.session_state.favorites

for i in range(0, len(cards), cols_per_row):
    cols = st.columns(cols_per_row)
    for idx, card in enumerate(cards[i:i + cols_per_row]):
        with cols[idx]:
            image_url = card.get("image_uris", {}).get("normal")
            if not image_url and "card_faces" in card:
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
                    try:
                        requests.post(f"{BACKEND_URL}/api/favorites",
                                      json={"card_id": card_id, "name": card["name"], "image_url": image_url},
                                      timeout=3)
                    except Exception:
                        st.warning("Couldn't save favorite to backend; saved locally.")
                    favorites[card_id] = {"card_id": card_id, "name": card["name"], "image_url": image_url}
                else:
                    try:
                        requests.delete(f"{BACKEND_URL}/api/favorites/{card_id}", timeout=3)
                    except Exception:
                        st.warning("Couldn't remove favorite from backend; removed locally.")
                    favorites.pop(card_id, None)

# --------------------------
# Favorites section (LOCAL STATE + Download buttons)
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

# --------------------------
# Download favorites buttons
# --------------------------
if fav_list:
    st.markdown("---")
    st.markdown("### Download your favorites")

    # Prepara datos
    df = pd.DataFrame(fav_list)
    json_bytes = json.dumps(fav_list, indent=2).encode("utf-8")
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    # Botones en columna: izquierda JSON, derecha CSV
    col_json, col_csv = st.columns(2)
    with col_json:
        st.download_button(
            label="Download JSON",
            data=json_bytes,
            file_name="favorites.json",
            mime="application/json"
        )
    with col_csv:
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="favorites.csv",
            mime="text/csv"
        )