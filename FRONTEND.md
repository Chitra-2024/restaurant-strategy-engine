# Frontend Dashboard

## 1. Overview

The frontend provides a simple React dashboard for restaurant strategy analysis. Users enter a restaurant name with optional location and days filters, the app calls the backend `/strategy` endpoint, and the page renders the global score, SWOT output, 4Ps, recommendations, and source-backed insights in a clean card-based layout.

## 2. Architecture

Core pieces:

- `RestaurantForm`: captures `restaurant_name`, `location`, and `days`, and also supports PDF export
- `DashboardPage`: manages loading, error, and response state, then renders all dashboard sections
- `src/services/api.js`: contains the strategy fetch helper and PDF export URL builder

## 3. Data Flow

User input -> form submit -> `fetchStrategy(filters)` -> backend `POST /strategy` -> JSON response -> React state update -> UI render

For export:

User input -> export action -> `/export-pdf` query string -> backend PDF response -> browser download

## 4. UI Structure

The dashboard is organized into readable sections:

- Health score: large color-coded score with a summary
- 4Ps framework: business interpretation of product, price, place, and promotion
- Strengths and weaknesses: shown as quick-scan badges
- SWOT: four cards for strengths, weaknesses, opportunities, and threats
- Recommendations: bullet list of business actions
- Strategic notes: human-readable insights with source links from backend analytics
- Aspect performance: per-aspect score cards with positive and negative counts

## 5. Design Decisions

- Simple UI: keeps attention on business insights rather than heavy interaction
- Tailwind CSS: makes spacing, cards, and responsive styling fast to maintain
- Card layout: separates strategic sections into easy-to-scan chunks for non-technical users

## 6. Future Improvements

- Add charts for trends and aspect comparisons
- Introduce subtle animations for loading and result transitions
- Support voice input for restaurant search
- Add real-time updates when new backend analysis is available
- Add inline PDF preview and richer report customization
