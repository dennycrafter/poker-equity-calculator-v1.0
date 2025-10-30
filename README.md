# poker-equity-calculator
Heads-up NLH Poker equity calculator. Accurate preflop, post-flop, turn, and river equity calculations using Monte Carlo simulaitons

# requirements
python 3.8 or higher
no installation needed - only built-in libaries (random, itertools, collections)

# how-to-use
Input cards for each player, seperately. Ace of hearts is spelt as Ah, King of hearts as Kh, 9 of clubs as 9c and so on.
Ten MUST be spelt using a "T"

# how-it-works
Monte-Carlo random for preflop equities and then turn and river is calculated by running every scenario.
Preflop there are 2 million+ combinations
Turn has 910
River has 44
Preflop equities are calculated by running 1_000_000 trials, so it may take a couple of seconds to load, depending on your PC specs.

# current-limitations / future-updates
Ace-King suited cannot be spelt as AKs, shortcuts will be implemented in next update.
If an invalid or duplicate card is input at the turn or river programme will stop working.
Multi-Way equities coming soon
No UI
