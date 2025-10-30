# Poker Equity Calculator
Heads-up NLH Poker equity calculator. Accurate preflop, post-flop, turn, and river equity calculations using Monte-Carlo simulaitons


## How to use
- Input cards for each player, seperately.
- First type card and the suit. Repeat for each card.
- Ace of hearts is typed as 'Ah', King of hearts as **Kh**, 9 of clubs as **9c** and so on.
- AKo is typed as 'Ac Ks'. 
- Ten **MUST** be spelt using a "T".

## Requirements
- python 3.8 or higher.
- No installation needed - only built-in libaries (random, itertools, collections)


## How it works
- Monte-Carlo .random for preflop equities and then turn and river is calculated by running every scenario using .combinations from itertools
- Preflop there are 2 million+ combinations.
- Turn has 910.
- River has 44.
- Preflop equities are calculated by running 1_000_000 trials, so it may take a couple of seconds to load, depending on your PC specs.

## Current limitations / Update plans
- Ace-King suited cannot be spelt as AKs, will return an error. Cards need to be input seperately.
- If an invalid or duplicate card is input at the turn or river programme will stop working.
- Only heads up currently. Plans for multi-way equities.
- No UI. Have to run in IDE or cmd equivelent.
- Feel free to submit any other suggestions

## Development
1. Create and organise cards into ranks and suits.
   - Represent cards as tuples
2. Organise user input into data python can understand
   - using len()
   - assigning digit 1 to rank_order, digit 2 to suits
   - check for duplicates
   - remove used cards and create deck.copy
   - raise ValueError if input is weird
   - inverse format back to hand notation for user to understand
3. Build count dictionaries
   - import counter
   - split 7 cards (hole + board) into two lists. ranks and suits
   - count frequency of suits and ranks (detecting pairs, trips, quads)
   - detect straights using range and len
     - create an if statement for wheel straight (Ace -> 5). Ace is normally highest card but exception has to be made here.
   - detect flushes by grouping cards by suit and then finding a suit with at least 5 cards. return top rank of said flush.
   - detect straight flushes
   - 7 card hand strength function returns a totally ordered key
4. Build hand evaluator
   - split ranks and suits again
   - create variable and count for quads, trips, and pairs seperately
   - sort all hands by rating. straight flush - 9, quads - 8, full house - 7 and so on.
5. Calculate equities
   - import random import combinations
   - for preflop equities run entire board using for loop in range n = trials. n = 1_000_000. while removing used cards.
   - win1, win2, tie all start at zero. if, elif, else add += 1 to each count after each respective run. tie count/2 + wins divided by total equals equity for each hand.
   - for turn, run exact number of combos using combinations (990). same equities formula.
   - for river, 44 counts
   - once river card is out, python prints a fixed value. i.e. the winner. 1.0 or 0.0
6. User prompts
   - use previous functions in conjunction with input strings.
   - expected_n and allow empty is None and False except for the hole cards. User does not need to proceed past preflop.
