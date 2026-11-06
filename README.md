Powerball Lotto Tracker

An analysis of every Powerball drawing under the current game rules (October 2015 to present), asking two questions:

Are some numbers really "hot"? Do certain numbers come up more often than random chance would predict?
What happens if you play every draw? How much would a regular player actually win or lose?
Data

Winning numbers come from New York State's official open data portal (Lottery Powerball Winning Numbers: Beginning 2010). Powerball changed its format on October 7, 2015 (white balls went from 1–59 to 1–69, and the Powerball from 1–35 to 1–26), so only draws after that date are analyzed to keep the comparison fair.

Methods

Frequency analysis (analyze.py)

Split each draw into its five white balls and the Powerball.
Counted how many times each white ball (1–69) was drawn and compared it to the count expected if every number were equally likely.
Ran a chi-square goodness-of-fit test to check whether the differences between numbers are larger than random chance would explain.

Simulation (simulate.py)

Simulated 1,000 players, each buying one random $2 ticket for every real draw in the dataset.
Scored every ticket against the actual winning numbers using Powerball's fixed prize table.
Compared total money spent to total winnings for each player.
Results

Draws analyzed: 1429 times (2015-10-07 to 2026-11-04)

Frequency: The most drawn white ball was 21 (128 times) and the least drawn was 13 (79 times), compared to an expected 103.6 draws per number. The chi-square test gave a p-value of 0.212, meaning there is no evidence the draws are unfair. The "hot" and "cold" numbers are what random variation looks like.

White ball frequency

Simulation: Each player spent $2,858. On average, players won back $355.46, about $0.12 for every $1 spent. Only 2 of 1,000 players came out ahead, and no one hit the jackpot.

Simulation results

Conclusion

Past results don't make any number more or less likely to be drawn, and playing regularly loses money for almost everyone. The lottery behaves exactly like a random game with a negative expected value.

How to Run
python3 -m venv venv
source venv/bin/activate
pip install pandas matplotlib scipy
curl -L -o powerball.csv "https://data.ny.gov/api/views/d6yy-54nr/rows.csv?accessType=DOWNLOAD"
python3 analyze.py
python3 simulate.py
Tools

Python, pandas, NumPy, SciPy, matplotlib