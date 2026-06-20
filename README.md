# 🛒 E-Commerce Orders EDA + Machine Learning (2023–2026)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> End-to-end EDA + Machine Learning project on 30,000 e-commerce orders across 10 countries (2023–2026) with an interactive Streamlit dashboard.

---

## 📊 Dataset Overview

| Feature | Detail |
|---------|--------|
| Records | 30,000 orders |
| Period | 2023–2026 |
| Countries | 10 (India, USA, UK, UAE, Germany, etc.) |
| Product Categories | 8 (Fashion, Electronics, Groceries, etc.) |
| Features | 41 columns |
| ML Tasks | Classification + Regression |

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-username>/ecommerce-orders-eda.git
cd ecommerce-orders-eda
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
ecommerce-orders-eda/
│
├── ecommerce_orders_dataset.csv     # Main dataset
├── data_dictionary.csv              # Column descriptions
├── Ecommerce_Orders_EDA.ipynb       # Full EDA + ML Notebook
├── app.py                           # Streamlit Dashboard
├── requirements.txt
└── README.md
```

---

## 🔍 Key Analyses

- **Revenue** — Monthly trends, by category/country/season
- **Customers** — Age, gender, CLV, membership, segments
- **Products** — Revenue, return rate, rating by category
- **Payment & Traffic** — Payment method, traffic source, device type
- **Shipping** — Order status, delivery days, shipping method
- **Profit** — Margin analysis, discount vs profit
- **Correlations** — Full feature heatmap
- **ML Models** — RF Classifier (High-Value Order) + RF Regressor (Order Amount)

---

## 🤖 ML Models

| Task | Model | Metric |
|------|-------|--------|
| High-Value Order Prediction | Random Forest Classifier | ~90% Accuracy |
| Order Amount Prediction | Random Forest Regressor | R² ~0.88 |

---

## 🛠️ Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit` · `Scikit-learn`

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
