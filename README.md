# 💠 VertexLens: Intelligent Data Dictionary Flow

**VertexLens** is an AI-powered data intelligence engine built during **HackFest 2.0 2026**. It bridges the gap between complex relational databases and business logic by automating the creation and maintenance of a living Data Dictionary.

---

## 🚀 Overview
Managing a data dictionary for massive datasets like **Olist E-Commerce** (100k+ records) is manually intensive. VertexLens uses **Google Gemini 2.0 Flash** to automate metadata enrichment, relationship mapping, and data health monitoring in real-time.

### 🌟 Key Features
* **📸 Vision-to-Metadata:** Upload ER-Diagrams or whiteboard sketches to auto-generate table structures and relationships.
* **🧠 AI Business Context:** Technical schemas are translated into business-friendly summaries using Gemini 2.0.
* **🛠️ Self-Healing Loop:** Automatically detects data quality issues (e.g., nulls in `order_reviews`) and generates SQL repair scripts.
* **💬 Conversational SQL:** A natural language chatbot that converts business questions into optimized BigQuery/SQL scripts.
* **📊 Interactive Lineage:** Dynamic visualization of table relationships and data health scores.

---

## 🏗️ System Architecture
The system follows a modular pipeline from ingestion to actionable insights:

1.  **Data Sources:** Connects to Snowflake, PostgreSQL, or local SQLite (Olist Dataset).
2.  **Extraction Hub:** Uses **SQLAlchemy** for metadata and **Pandas** for statistical profiling.
3.  **AI Enrichment:** **Gemini 2.0 Flash** processes context to generate summaries and SQL suggestions.
4.  **UI Layer:** A sleek, interactive dashboard built with **Streamlit**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **AI/ML:** Google Gemini 2.0 Flash (Multimodal RAG)
* **Data Processing:** Pandas, NumPy
* **Database Engine:** SQLAlchemy, SQLite
* **Frontend:** Streamlit
* **Visualization:** Graphviz

---

## 📁 Project Structure
```text
├── .csv/                # Raw Olist E-Commerce Dataset
├── ai_engine.py         # Gemini 2.0 Logic & Prompt Engineering
├── app.py               # Streamlit UI & Orchestrator
├── database_helper.py   # Metadata Extraction & Data Profiling
├── olist_ecommerce.db   # Processed SQLite Database
├── setup_db.py          # Database initialization script
└── README.md            # Documentation

---

## ⚙️ Installation & Setup

1. Clone the repo:
    * git clone https://github.com/JAY007-think/Vertex_HackFest.git
    * cd Vertex_HackFest
2. Install dependencies:
    * pip install -r requirements.txt
3. Set up environment variables:
    * Create a .env file and add your Gemini API Key:
    * GEMINI_API_KEY=your_api_key_here
4. Run the App:
    * streamlit run app.py

---

## 👥 The Dream Team (Team Vertex)
1. Jay Soni - Project Lead & AI Engineer
2. Mohit Goswami - Fronted Developer
3. Pawan Prajapat - Data Engineer 

---

## 🏆 Acknowledgments
Developed at HackFest 2.0 2026 organized by GDG Cloud New Delhi and Turgon AI.

---

👨‍💻 Author

* Jay Soni
* LinkedIn: https://www.linkedin.com/in/jay-soni-01a791261/
* LeetCode: https://leetcode.com/u/ZysIunJ150/

> This project was built as a learning exercise and enhanced with additional features.