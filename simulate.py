import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Settings ----
TICKET_PRICE = 2
NUM_PLAYERS = 1000      # how many simulated people
# Fixed Powerball prizes by (white balls matched, Powerball matched).
# The jackpot varies, so a jackpot win is counted separately.
# Double-check these on powerball.com in case the rules change.
PRIZES = {
    (5, False): 1_000_000,
    (4, True): 50_000,
    (4, False): 100,
    (3, True): 100,
    (3, False): 7,
    (2, True): 7,
    (1, True): 4,
    (0, True): 4,
}

# ---- Load the real draws (same cleaning as analyze.py) ----
df = pd.read_csv("powerball.csv")
df["Draw Date"] = pd.to_datetime(df["Draw Date"])
nums = df["Winning Numbers"].str.split(expand=True).astype(int)
nums.columns = ["W1", "W2", "W3", "W4", "W5", "PB"]
df = pd.concat([df, nums], axis=1)
df = df[df["Draw Date"] >= "2015-10-07"].sort_values("Draw Date")

rng = np.random.default_rng()
winnings = np.zeros(NUM_PLAYERS)
jackpots = 0

# ---- Each player buys one random ticket for every real draw ----
for _, row in df.iterrows():
    # 5 random white balls (1-69, no repeats) and 1 Powerball (1-26) per player
    white_tickets = rng.random((NUM_PLAYERS, 69)).argsort(axis=1)[:, :5] + 1
    pb_tickets = rng.integers(1, 27, NUM_PLAYERS)

    winning_white = np.zeros(70, dtype=bool)
    winning_white[[row.W1, row.W2, row.W3, row.W4, row.W5]] = True

    white_matches = winning_white[white_tickets].sum(axis=1)
    pb_match = pb_tickets == row.PB

    for i in range(NUM_PLAYERS):
        key = (white_matches[i], pb_match[i])
        if key == (5, True):
            jackpots += 1
        else:
            winnings[i] += PRIZES.get(key, 0)

# ---- Results ----
spent = len(df) * TICKET_PRICE
net = winnings - spent

print(f"Draws played: {len(df)}  |  Each player spent: ${spent:,}")
print(f"Average winnings per player: ${winnings.mean():,.2f}")
print(f"Average net result:          ${net.mean():,.2f}")
print(f"Players who came out ahead:  {(net > 0).sum()} of {NUM_PLAYERS}")
print(f"Jackpots won:                {jackpots}")
print(f"Average return per $1 spent: ${winnings.mean() / spent:.2f}")

plt.figure(figsize=(10, 5))
plt.hist(net, bins=40)
plt.axvline(0, color="red", linestyle="--", label="Break even")
plt.xlabel("Net result per player ($)")
plt.ylabel("Number of players")
plt.title(f"{NUM_PLAYERS} players buying one Powerball ticket every draw since Oct 2015")
plt.legend()
plt.tight_layout()
plt.savefig("simulation_results.png")
print("\nSaved chart to simulation_results.png")
