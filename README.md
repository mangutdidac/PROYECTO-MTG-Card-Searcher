# 🃏 MTG UnderDeck – Project Description

**MTG UnderDeck** is a web-based application designed to streamline the process of searching, filtering, and managing *Magic: The Gathering (MTG)* cards. The project allows players to explore card databases efficiently, identify key cards for their decks, mark favorites, and export card data for further analysis or deck-building purposes.

## 🎯 Project Goals
- Efficient Card Search: Advanced filters for card name, type, color, rarity, keywords, and set/edition.
- Favorites Management: Mark cards as favorites, synced locally and with the backend.
- Export Capabilities: Download favorites in `CSV` or `JSON` for offline use or analysis.
- Real-Time Data: Direct integration with Scryfall API and a custom FastAPI backend.

## 💻 Technologies Used
- **Frontend:** Streamlit + Python for interactive browser interface.
- **Backend:** FastAPI for high-performance APIs, SQLAlchemy + PostgreSQL/SQLite for storage.
- **External APIs:** Scryfall API for real-time MTG card data.
- **Data Management:** Pandas & JSON libraries for CSV/JSON export.

## 🧠 Project Logic
- **Search Module:** Filters, query construction, and backend requests to fetch cards.
- **Favorites Module:** Mark and unmark cards, synced to session state and backend.
- **Export Module:** Download favorites in `CSV` or `JSON` formats.
- **Pagination & Performance:** Streamlit caching and controlled API calls for responsive UI.

## 💡 Practical Value
- Identify key cards across multiple sets and editions quickly.
- Organize favorites for deck building and strategy planning.
- Export card data for offline analysis, sharing, or integration with other tools.
- Save time in preparing decks for competitive or casual play.

## 🚀 Future Enhancements
- Full deck creation and editing in the frontend.
- User authentication for cross-device sync.
- Advanced analytics on card collections and usage patterns.

## HOW TO RUN THE PROJECT

1️⃣ Clone the repository
git clone https://github.com/<your-username>/mtg-underdeck.git
cd mtg-underdeck

2️⃣ Create and activate a Python virtual environment
Create a virtual environment
python -m venv venv

Activate
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the backend (FastAPI)
The backend handles Scryfall API calls, favorites, and sets. Run it with:

uvicorn backend.app.main:app --reload

The backend will be available at: http://127.0.0.1:8000
Test the health endpoint: http://127.0.0.1:8000/health → should return {"status": "ok"}
You can also add --port <PORT> if you want a different port.

5️⃣ Run the frontend (Streamlit)
In another terminal (make sure the virtual environment is active):

streamlit run main.py

Streamlit will open a browser window automatically, usually at http://localhost:8501.
The frontend connects to the backend at BACKEND_URL. By default, it points to http://127.0.0.1:8000, but you can override it using an environment variable:

export BACKEND_URL=http://127.0.0.1:8000  # macOS/Linux
set BACKEND_URL=http://127.0.0.1:8000     # Windows

6️⃣ Using the app

Search Cards: Use filters in the sidebar (name, color, type, rarity, set, keywords) and click “Search”.
Favorites: Click the ❤️ checkbox to save cards to favorites.
Download Favorites: Use the buttons at the top to download favorites as CSV or JSON.
Pagination: Use “Previous” and “Next” buttons to navigate pages.
All favorite cards are synced with the backend (if running) or saved locally in session state.

## Contact
- Dídac Mangut Soria
- (+34611443771)
- mangutdidac@gmail.com
- https://www.linkedin.com/in/dídac-mangut-soria/
