# CodeAlpha Task 3 - Data Visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../ecommerce_products_reviews.csv")
df["review_date"] = pd.to_datetime(df["review_date"])

# KPI values
print("Total Revenue:", round(df["revenue"].sum(),2))
print("Units Sold:", int(df["units_sold"].sum()))
print("Average Rating:", round(df["rating"].mean(),2))
print("Products:", df["product_name"].nunique())

# 1 Revenue by category
cat = df.groupby("category")["revenue"].sum().sort_values()
plt.figure(figsize=(9,5)); cat.plot(kind="barh")
plt.title("Revenue by Category"); plt.xlabel("Revenue"); plt.tight_layout()
plt.savefig("01_revenue_by_category.png", dpi=160); plt.show()

# 2 Units by brand
brand = df.groupby("brand")["units_sold"].sum().sort_values(ascending=False)
plt.figure(figsize=(9,5)); brand.plot(kind="bar")
plt.title("Units Sold by Brand"); plt.ylabel("Units"); plt.xticks(rotation=25)
plt.tight_layout(); plt.savefig("02_units_by_brand.png", dpi=160); plt.show()

# 3 Rating distribution
plt.figure(figsize=(8,5)); sns.countplot(data=df, x="rating")
plt.title("Rating Distribution"); plt.tight_layout()
plt.savefig("03_rating_distribution.png", dpi=160); plt.show()

# 4 Sentiment
plt.figure(figsize=(8,5)); sns.countplot(data=df, x="sentiment", order=["Positive","Neutral","Negative"])
plt.title("Customer Sentiment Distribution"); plt.tight_layout()
plt.savefig("04_sentiment_distribution.png", dpi=160); plt.show()

# 5 Monthly revenue
monthly=df.groupby(df["review_date"].dt.to_period("M"))["revenue"].sum()
plt.figure(figsize=(10,5)); monthly.plot(marker="o")
plt.title("Monthly Revenue Trend"); plt.ylabel("Revenue"); plt.xlabel("Month")
plt.xticks(rotation=35); plt.tight_layout()
plt.savefig("05_monthly_revenue.png", dpi=160); plt.show()

# 6 Price vs rating
plt.figure(figsize=(9,5)); sns.scatterplot(data=df,x="price",y="rating",hue="category",alpha=.55)
plt.title("Price vs Customer Rating"); plt.tight_layout()
plt.savefig("06_price_vs_rating.png", dpi=160); plt.show()
