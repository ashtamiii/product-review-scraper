import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# User search keyword (acts like product search)
PRODUCT_KEYWORD = "coffee"   # change this anytime

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Load dataset
df = pd.read_csv("data/Reviews.csv")

# Keep only required columns
df = df[["ProductId", "Score", "Text"]]

# Filter by user keyword
filtered = df[df["Text"].str.contains(PRODUCT_KEYWORD, case=False, na=False)].head(200)

# Sentiment function
def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Apply sentiment
filtered["sentiment"] = filtered["Text"].apply(get_sentiment)

# Save final output
filtered.to_csv("data/processed_reviews.csv", index=False)

print("\n Dataset loaded successfully")
print(" Keyword:", PRODUCT_KEYWORD)
print(" Total reviews used:", len(filtered))
print(" Output saved to data/processed_reviews.csv")
