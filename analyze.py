import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chisquare

# 1. Load the data
df = pd.read_csv("powerball.csv")
df["Draw Date"] = pd.to_datetime(df["Draw Date"])

# 2. Split "Winning Numbers" into 5 white balls + the Powerball
nums = df["Winning Numbers"].str.split(expand=True).astype(int)
nums.columns = ["W1", "W2", "W3", "W4", "W5", "PB"]
df = pd.concat([df, nums], axis=1)

# 3. Keep only draws under the current rules (since Oct 7, 2015:
#    white balls 1-69, Powerball 1-26)
df = df[df["Draw Date"] >= "2015-10-07"].sort_values("Draw Date")
print(f"Draws analyzed: {len(df)} "
      f"({df['Draw Date'].min().date()} to {df['Draw Date'].max().date()})")

# 4. Count how often each white ball number was drawn
white = pd.concat([df[c] for c in ["W1", "W2", "W3", "W4", "W5"]])
counts = white.value_counts().reindex(range(1, 70), fill_value=0)
expected = len(white) / 69

print(f"\nExpected count per number if fair: {expected:.1f}")
print("\nMost drawn white balls:")
print(counts.sort_values(ascending=False).head(5).to_string())
print("\nLeast drawn white balls:")
print(counts.sort_values().head(5).to_string())

# 5. Chi-square test: are these counts consistent with a fair, random draw?
stat, p = chisquare(counts)
print(f"\nChi-square statistic: {stat:.2f}, p-value: {p:.3f}")
if p > 0.05:
    print("No evidence the draws are unfair -- the 'hot' numbers are just chance.")
else:
    print("Counts differ more than chance would usually explain -- worth a closer look.")

# 6. Chart
plt.figure(figsize=(14, 5))
plt.bar(counts.index, counts.values)
plt.axhline(expected, color="red", linestyle="--", label="Expected if random")
plt.xlabel("White ball number")
plt.ylabel("Times drawn")
plt.title("Powerball white ball frequency (since Oct 2015)")
plt.legend()
plt.tight_layout()
plt.savefig("white_ball_frequency.png")
print("\nSaved chart to white_ball_frequency.png")
