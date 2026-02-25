<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MTG UnderDeck - Project Description</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f9f9f9;
            color: #333;
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #4B0082;
        }
        h1 {
            font-size: 2rem;
        }
        h2 {
            font-size: 1.5rem;
        }
        h3 {
            font-size: 1.2rem;
        }
        ul {
            margin: 0.5rem 0 1rem 2rem;
        }
        .emoji {
            margin-right: 0.5rem;
        }
        .section {
            margin-bottom: 2rem;
        }
        code {
            background-color: #eee;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <h1>🃏 MTG UnderDeck – Project Description</h1>


        <p><strong>MTG UnderDeck</strong> is a web-based application designed to streamline the process of searching, filtering, and managing <em>Magic: The Gathering (MTG)</em> cards. The project allows players to explore card databases efficiently, identify key cards for their decks, mark favorites, and export card data for further analysis or deck-building purposes.</p>


    <div class="section">
        <h2>🎯 Project Goals</h2>
        <ul>
            <li>Efficient Card Search: Advanced filters for card name, type, color, rarity, keywords, and set/edition.</li>
            <li>Favorites Management: Mark cards as favorites, synced locally and with the backend.</li>
            <li>Export Capabilities: Download favorites in <code>CSV</code> or <code>JSON</code> for offline use or analysis.</li>
            <li>Real-Time Data: Direct integration with Scryfall API and a custom FastAPI backend.</li>
        </ul>
    </div>

    <div class="section">
        <h2>💻 Technologies Used</h2>
        <ul>
            <li><strong>Frontend:</strong> Streamlit + Python for interactive browser interface.</li>
            <li><strong>Backend:</strong> FastAPI for high-performance APIs, SQLAlchemy + PostgreSQL/SQLite for storage.</li>
            <li><strong>External APIs:</strong> Scryfall API for real-time MTG card data.</li>
            <li><strong>Data Management:</strong> Pandas & JSON libraries for CSV/JSON export.</li>
        </ul>
    </div>

    <div class="section">
        <h2>🧠 Project Logic</h2>
        <ul>
            <li><strong>Search Module:</strong> Filters, query construction, and backend requests to fetch cards.</li>
            <li><strong>Favorites Module:</strong> Mark and unmark cards, synced to session state and backend.</li>
            <li><strong>Export Module:</strong> Download favorites in <code>CSV</code> or <code>JSON</code> formats.</li>
            <li><strong>Pagination & Performance:</strong> Streamlit caching and controlled API calls for responsive UI.</li>
        </ul>
    </div>

    <div class="section">
        <h2>💡 Practical Value</h2>
        <ul>
            <li>Identify key cards across multiple sets and editions quickly.</li>
            <li>Organize favorites for deck building and strategy planning.</li>
            <li>Export card data for offline analysis, sharing, or integration with other tools.</li>
            <li>Save time in preparing decks for competitive or casual play.</li>
        </ul>
    </div>

    <div class="section">
        <h2>🚀 Future Enhancements</h2>
        <ul>
            <li>Full deck creation and editing in the frontend.</li>
            <li>User authentication for cross-device sync.</li>
            <li>Advanced analytics on card collections and usage patterns.</li>
        </ul>
    </div>
</body>
</html>
