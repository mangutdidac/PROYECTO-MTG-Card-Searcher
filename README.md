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
