# CodeAlpha Task 4 - Sentiment Analysis
# Install: pip install pandas matplotlib seaborn nltk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../ecommerce_products_reviews.csv")

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    nltk.download("vader_lexicon", quiet=True)
    sia = SentimentIntensityAnalyzer()
    df["compound"] = df["review_text"].fillna("").apply(lambda x: sia.polarity_scores(x)["compound"])
    df["predicted_sentiment"] = df["compound"].apply(
        lambda x: "Positive" if x >= .05 else ("Negative" if x <= -.05 else "Neutral")
    )
except Exception:
    # Simple fallback lexicon so the project still runs offline.
    positive_words={"excellent","great","good","amazing","useful","recommended","perfectly","reliable","better"}
    negative_words={"poor","bad","faulty","disappointed","damaged","late","worse","not","stopped"}
    def score(text):
        words=set(str(text).lower().replace(".","").split())
        p=len(words & positive_words); n=len(words & negative_words)
        return p-n
    df["compound"]=df["review_text"].apply(score)
    df["predicted_sentiment"]=df["compound"].apply(lambda x:"Positive" if x>0 else ("Negative" if x<0 else "Neutral"))

print(df[["review_text","predicted_sentiment"]].head(10))
print(df["predicted_sentiment"].value_counts())

plt.figure(figsize=(8,5))
sns.countplot(data=df,x="predicted_sentiment",order=["Positive","Neutral","Negative"])
plt.title("Customer Sentiment")
plt.tight_layout(); plt.savefig("sentiment_distribution.png",dpi=160); plt.show()

sentiment_by_category=pd.crosstab(df["category"],df["predicted_sentiment"],normalize="index")*100
print(sentiment_by_category.round(2))

sentiment_by_category.plot(kind="bar",stacked=True,figsize=(10,6))
plt.title("Sentiment Mix by Category"); plt.ylabel("Percentage")
plt.xticks(rotation=25); plt.tight_layout()
plt.savefig("sentiment_by_category.png",dpi=160); plt.show()

# Save predictions
df.to_csv("sentiment_results.csv",index=False)
