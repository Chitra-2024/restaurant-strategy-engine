# Restaurant Strategy Engine

AI-powered platform that converts fragmented customer feedback into structured, actionable business intelligence.

---

## Overview

Customer feedback for restaurants is distributed across multiple platforms such as review sites, social media, and community forums. While this creates a large volume of data, it is often difficult to translate into clear, actionable insights.

Restaurant Strategy Engine addresses this by aggregating multi-source feedback, analyzing it using natural language processing, and transforming it into structured strategic outputs such as SWOT and 4Ps frameworks. The system is designed as a modular, extensible pipeline that can support real-world integrations.

---

## Key Features

* Multi-source feedback ingestion (simulated platforms: Zomato, Google, Reddit, Twitter)
* NLP-based sentiment analysis using transformer models
* Strategic analysis using:

  * SWOT (Strengths, Weaknesses, Opportunities, Threats)
  * 4Ps (Product, Price, Place, Promotion)
* Evidence-based insights derived from underlying review data
* Competitor comparison via `/compare` endpoint
* Executive summary generation for quick decision-making
* Caching layer to optimize repeated analysis requests
* Interactive frontend dashboard with structured layout and review feed
* PDF export of strategy reports

---

## System Architecture

The system follows a modular pipeline:

User Input → API → Ingestion → Processing → NLP → Analysis → Strategy → UI

### Backend

* FastAPI (asynchronous API framework)
* Service-oriented architecture (ingestion, processing, analytics, strategy)

### Frontend

* React
* Tailwind CSS

### Data Layer

* MongoDB for raw and processed review storage

### NLP Layer

* Hugging Face Transformers for sentiment analysis

---

## Tech Stack

### Frontend

* React
* Tailwind CSS

### Backend

* FastAPI
* Python

### Database

* MongoDB

### NLP / AI

* Hugging Face Transformers

### Other

* Asynchronous processing
* In-memory caching

---

## API Endpoints

| Endpoint           | Description                    |
| ------------------ | ------------------------------ |
| POST /ingest-data  | Fetch or simulate review data  |
| POST /process-data | Process raw reviews            |
| POST /analyze      | Generate analytical insights   |
| POST /strategy     | Generate full strategic report |
| POST /compare      | Compare multiple restaurants   |
| GET /export-pdf    | Export report as PDF           |

---

## Application Flow

1. User provides a restaurant name (and optional filters such as location or date range)
2. System ingests and processes feedback data
3. NLP layer extracts sentiment and structured signals
4. Analytics layer computes aspect-level insights
5. Strategy layer generates frameworks and recommendations
6. Results are displayed via the frontend dashboard

---

## Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Usage

* Enter a restaurant name on the landing page
* The system processes available feedback data
* The dashboard presents:

  * Global performance score
  * Strategic insights
  * SWOT and 4Ps frameworks
  * Recommendations
  * Customer feedback feed

---

## Design Considerations

* **Simulation over scraping**
  Due to platform restrictions, data is simulated while maintaining a system design that supports real integrations.

* **Modular architecture**
  Separation of ingestion, processing, analytics, and strategy layers improves scalability and maintainability.

* **Asynchronous processing**
  Enables efficient handling of multiple operations such as ingestion and analysis.

* **Flexible data storage**
  MongoDB supports unstructured and semi-structured review data.

---

## Limitations

* Data sources are simulated rather than live integrations
* NLP pipeline can be extended with more advanced models
* No real-time streaming of incoming data

---

## Future Work

* Integration with real-world APIs (review platforms, social media)
* Advanced NLP techniques (aspect-based sentiment, topic modeling)
* Time-series analysis for trend detection
* Enhanced competitor benchmarking
* Real-time data ingestion and updates
* Improved frontend with richer visualizations and analytics

---

## Conclusion

Restaurant Strategy Engine demonstrates how unstructured, multi-source customer feedback can be transformed into structured, decision-ready insights. The system highlights key concepts in full-stack development, NLP integration, and scalable system design, and can serve as a foundation for real-world business intelligence applications.
