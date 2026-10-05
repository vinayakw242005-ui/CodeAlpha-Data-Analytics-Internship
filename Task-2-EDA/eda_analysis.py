# CodeAlpha Task 2 - Exploratory Data Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../ecommerce_products_reviews.csv")
df["review_date"] = pd.to_datetime(df["review_date"])

print(df.head())
print(df.info())
print(df.describe(numeric_only=True))
print("Missing values:\n", df.isna().sum())

# Business questions
questions = [
    "Which category generates the highest revenue?",
    "Which products have the strongest ratings?",
    "Does price appear related to rating?",
    "Which brands sell the most units?",
    "What proportion of reviews are positive, neutral, and negative?"
]
for q in questions: print("-", q)

# Category analysis
category_summary = df.groupby("category").agg(
    revenue=("revenue","sum"),
    units_sold=("units_sold","sum"),
    avg_rating=("rating","mean")
).sort_values("revenue", ascending=False)
print(category_summary)

# Brand analysis
brand_summary = df.groupby("brand").agg(
    revenue=("revenue","sum"),
    units_sold=("units_sold","sum"),
    avg_rating=("rating","mean")
).sort_values("revenue", ascending=False)
print(brand_summary)

# Outliers using IQR
for col in ["price","rating","units_sold","revenue"]:
    q1,q3=df[col].quantile([.25,.75]); iqr=q3-q1
    out=df[(df[col]<q1-1.5*iqr)|(df[col]>q3+1.5*iqr)]
    print(f"{col}: {len(out)} potential outliers")

# Visual exploration
plt.figure(figsize=(9,5))
sns.histplot(df["price"], bins=30, kde=True)
plt.title("Product Price Distribution"); plt.tight_layout(); plt.show()

plt.figure(figsize=(9,5))
sns.boxplot(data=df, x="category", y="rating")
plt.xticks(rotation=25); plt.title("Ratings by Category"); plt.tight_layout(); plt.show()

plt.figure(figsize=(9,5))
sns.scatterplot(data=df, x="price", y="rating", hue="category", alpha=.6)
plt.title("Price vs Rating"); plt.tight_layout(); plt.show()

print("Correlation matrix:\n", df[["price","rating","review_count","units_sold","revenue"]].corr())
