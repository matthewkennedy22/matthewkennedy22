# Olist E-Commerce Business Insights

End-to-end analytics project on the Brazilian Olist e-commerce dataset, built as a consulting-style workflow: data preparation, business KPI engineering, exploratory analysis, and applied machine learning extensions.

## Project Objective

Analyze multi-table e-commerce operations to surface practical business insights across customer behavior, delivery performance, and retention risk.

## Executive Summary

This project translates raw Olist marketplace data into action-oriented recommendations to improve growth, customer satisfaction, and operational performance.

### Key Findings

- Customer concentration follows a Pareto-like pattern: a smaller share of repeat customers drives a large share of revenue.
- Delivery delays are strongly associated with worse customer reviews (about 1.2 points lower on average for delayed orders).
- Credit card is the dominant payment method, while installment usage is associated with higher average order values.
- Product-category performance differs: some categories drive higher long-term value while others contribute more volume than margin.

### Recommended Actions

- Invest in retention and loyalty programs for high-value and repeat customers.
- Reduce delivery delays by improving SLA performance in slower regions and lanes.
- Promote installment options for higher-ticket categories to increase cart size.
- Rebalance category-level marketing spend toward higher-LTV segments while preserving acquisition-focused categories.

### Estimated Business Impact

- A 10% improvement in on-time delivery could reduce negative reviews by roughly 15%, with a potential 5-7% lift in repeat purchases over 6-9 months.
- A 20% increase in installment adoption could raise average order value by roughly 8-10%.

## Project Structure

```text
Olist-E-Commerce-Business-Insights/
|- notebooks/
|  `- olist-e-commerce-business-insights-project.ipynb
|- data/                    # optional local data staging
|- documentation/           # notes, dictionaries, findings
|- assets/
|  `- screenshots/          # notebook or chart exports for GitHub preview
|- requirements.txt
`- README.md
```

## Technical Highlights

- Joined and standardized core Olist tables (orders, customers, products, sellers, payments, reviews, geolocation).
- Engineered customer- and operations-facing metrics including LTV proxies, delivery performance, and RFM-style signals.
- Used EDA to evaluate marketplace patterns and identify actionable opportunities.
- Extended analysis with `KMeans` customer segmentation and logistic regression for delivery-delay classification.
- Designed notebook workflow to run locally or in Kaggle environments.

## Tech Stack

Python, pandas, NumPy, Matplotlib, SQLite, scikit-learn, Jupyter

## Main Artifact

- `notebooks/olist-e-commerce-business-insights-project.ipynb`

## Dataset

- [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olist/brazilian-ecommerce)

## Kaggle Notebook

- [Olist E-Commerce Business Insights Project](https://www.kaggle.com/code/mattkennedy22/olist-e-commerce-business-insights-project)

## Run Locally

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Download the Olist CSV files from Kaggle.
3. Place the CSV files in your preferred local data directory and update notebook path variables if needed.
4. Open and run `notebooks/olist-e-commerce-business-insights-project.ipynb`.
