# Matthew Kennedy

MS Business Analytics | Data Analytics | Machine Learning | Business Intelligence

Collection of analytics systems that solve real-world infrastructure, operational, and data problems. These projects combine data engineering, statistical modeling, machine learning, and interactive applications to turn complex data into actionable insights.

## Featured Projects

### Adventure Works Bike Shop Dashboard (Power BI)

Power BI | DAX | Power Query | Data Modeling | Business Intelligence

Built an end-to-end sales analytics dashboard for Adventure Works to track revenue, returns, customer behavior, and product performance. The report uses cleaned CSV data sources, dimensional modeling, and DAX measures to deliver executive KPIs and drilldown views for operational decision-making.

Repo

https://github.com/matthewkennedy22/Power-BI-Adventure-Works-Dashboard

---

### Agentic Essay-Writing Workflow (LangGraph + Tavily)

Python | Agentic AI | LangGraph | LangChain | OpenAI | Tool Use | Tavily | Gradio | SQLite Checkpoints

An **agentic multi-stage LangGraph** pipeline built as a structured **essay-writing assistant**: outline-style planning, **tool-grounded web research** (Pydantic-typed Tavily queries), draft generation, critic-driven reflection, and conditional re-retrieval—looping under a revision cap with **SqliteSaver** checkpointing per thread and **streamed** node traces for observability.

Technically, the emphasis is **inspectable agentic control flow** (nodes, conditional edges, `graph.stream`) rather than one monolithic prompt; grounding uses **live search APIs** instead of embedding-store RAG, with a Gradio UI for interactive runs.

Tech Stack

Python, LangGraph, LangChain, OpenAI API, Tavily, Pydantic, Gradio, SQLite (langgraph-checkpoint-sqlite), Jupyter

Repo

https://github.com/matthewkennedy22/langgraph-essay-writer

---

### Hyperscale Data Center Optimization Tool

Python | DuckDB | Streamlit | Climate Modeling

Developed a simulation platform to evaluate Power Usage Effectiveness (PUE) and Water Usage Effectiveness (WUE) across U.S. counties to identify optimal locations for hyperscale data centers.

The system integrates hourly climate data, energy pricing, water costs, and drought risk metrics to model cooling performance and infrastructure operating costs. A 27M+ row DuckDB analytics engine powers an interactive Streamlit dashboard for geographic comparison and site selection analysis.

Tech Stack

Python, DuckDB, Pandas, Streamlit, Climate APIs, Data Modeling

Repo

https://github.com/matthewkennedy22/hyperscale-data-center-optimization-tool

---

### BetBrain – Predictive Sports Analytics

Python | FastAPI | React | Machine Learning | APIs

Built a full-stack sports analytics platform that aggregates live betting odds, news sentiment, and line movement data to generate data-driven betting insights.

The backend integrates The Odds API for sportsbook data and uses TextBlob sentiment analysis on sports news to capture market sentiment signals. A custom algorithm evaluates expected value (EV), odds discrepancies, and sentiment signals to rank betting opportunities. Results are served through a FastAPI backend and React dashboard for real-time analysis.

Tech Stack

Python, FastAPI, Pandas, NumPy, TextBlob, SQLite, React, APIs

Repo

https://github.com/matthewkennedy22/Bet_Brain

---

### RAG Movie Recommendation System

Python | LLM | Vector Search | NLP

Built a Retrieval-Augmented Generation (RAG) system for semantic search and question answering over IMDB movie reviews.

Reviews are processed using NLTK tokenization and custom text chunking, then embedded with SentenceTransformers (all-MiniLM-L6-v2) and stored in a Qdrant vector database. User queries are embedded and matched using cosine similarity retrieval, and retrieved context is passed to Gemma 3 via Ollama to generate grounded responses with citation-style references.

Tech Stack

Python, Qdrant, SentenceTransformers, NLTK, Ollama, Gemma 3, Vector Search

Repo

https://github.com/matthewkennedy22/RAG-System-Gemma3b-IMDB

---

### SQL Auto Loan Database

SQL | Relational Database Design | Data Modeling

Designed and implemented a relational database system for managing auto loan portfolios, including borrower profiles, loan contracts, payment schedules, and servicing records.

The schema models key financial relationships and supports queries for loan performance tracking, borrower risk analysis, and payment history reporting.

Tech Stack

SQL, Relational Database Design, Data Modeling

Repo

https://github.com/matthewkennedy22/SQL-Auto-Loan-Database

---

### COVID Symptom & Demographics — ML Prediction

Python | scikit-learn | XGBoost | Pandas | Jupyter | Class Imbalance

End-to-end machine learning pipeline for **binary COVID test prediction** (positive vs negative) from symptoms, known exposure (**Contact**), age 60+, and sex. The project scales to roughly **one million** raw records: data cleaning removes incomplete demographic rows, encodes categoricals, optionally preserves duplicate symptom profiles to reflect real prevalence, and exports a modeling-ready dataset with a severe **~90% / ~10%** class imbalance.

Ensemble models include **Random Forest** (class-weighted, F1-tuned), **Histogram Gradient Boosting**, and **XGBoost** (with `scale_pos_weight`), using RandomizedSearchCV on stratified samples, refitting the best estimators on the full training set, and reporting **AUC**, **F1 / Fβ**, sensitivity, specificity, and threshold sweeps for operational tradeoffs. Exploratory **agglomerative clustering**, a cleaning script (`src/clean_covid_data.py`), and written findings (`docs/Ensemble_Learning_Findings.md`, data cleaning guide, and report PDF) document methods and results.

Tech Stack

Python, pandas, scikit-learn, XGBoost, Jupyter, openpyxl, NumPy

Repo

https://github.com/matthewkennedy22/covid-ml-symptom-prediction

---

### Olist E-Commerce Business Insights (Kaggle)

Python | Pandas | NumPy | Matplotlib | SQLite | scikit-learn | Jupyter

End-to-end practice project on the [Brazilian E-Commerce (Olist)](https://www.kaggle.com/datasets/olist/brazilian-ecommerce) dataset, modeled as a consulting-style analysis: **cleaning and joining** multiple CSVs (with **SQLite** for table organization and merges), **feature-style metrics** such as **customer LTV**, **delivery performance**, **RFM**-style customer scoring, and **churn**-related signals, **EDA** with Matplotlib, and **ML extensions** including **KMeans**-based **customer segmentation** and a **logistic regression** look at **delivery delay** classification.

This project is preserved in its **original Kaggle notebook format** so viewers can see the exact source workflow as published.

Original Project Location

https://www.kaggle.com/code/mattkennedy22/olist-e-commerce-business-insights-project

Tech Stack

Python, pandas, NumPy, Matplotlib, SQLite, scikit-learn, Jupyter

Project Folder

`Olist-E-Commerce-Business-Insights`

Kaggle Dataset

https://www.kaggle.com/datasets/olist/brazilian-ecommerce

---

## Contact

Matthew Kennedy

GitHub: https://github.com/matthewkennedy22

Email: matthewkennedy22@gmail.com
