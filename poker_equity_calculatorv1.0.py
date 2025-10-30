#building deck
RANK_ORDER = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
SUITS = {'s','h','d','c'} # spades, hearts, diamonds, clubs

#converting user input into data python can understand
def parse_card(s: str):
    s = s.strip().upper()
    if len(s) != 2:
        raise ValueError(f"Card must be characters like 'Ah' or '10s', got: {s}")
    r, u = s[0], s[1].lower() #digit 1 of s is r and digit 2 of s is lowercased and assigned to u
    if r not in RANK_ORDER or u not in SUITS:
        raise ValueError(f"Bad card: {s}")
    return (RANK_ORDER[r], u)

#duplicate prevention
def parse_cards(seq):
    cards = [parse_card(x) for x in seq]
    if len(set(cards)) != len(cards):
        raise ValueError("Duplicae cards detected")
    return cards

#building full deck using list compression
def full_deck():
    return [(rv, u) for rv in RANK_ORDER.values() for u in SUITS] #making a tuple for each card in the deck

#removing cards in use. we dont want to include duplicates in our equity calculation
def remove_cards(deck, used):
    rem = deck.copy()
    for c in used:
        try:
            rem.remove(c)
        except ValueError:
            raise ValueError(f"Card {c} not available to remove (duplicate or invalid).")
    return rem

#inversing formatting back for user viewing. user wants to see cards not backend
INV_RANK = {v:k for k,v in RANK_ORDER.items()}
def fmt_card(c):
    r, u = c
    return f"{INV_RANK[r]}{u}"

def fmt_cards(cards):
    return " ".join(fmt_card(c) for c in cards)

'''
#SANITY TEST
#parsing
assert parse_card("Ah") == (14,'h')
assert parse_card("td") == (10,'d')

#deck size
d = full_deck()
assert len(d) == 52
assert len(set(d)) == 52

#remove used cards
used = parse_cards(["Ah","Kh","Qs","Jd"])
rem  = remove_cards(d, used)
assert len(rem) == 52 - 4
for c in used:
    assert c not in rem
'''

#building count dictionaries
#extracting values and suits
from collections import Counter

#seperates the 7 cards into two lists. ranks n suits
def split_ranks_suits(cards):
    ranks = [r for (r, _) in cards]
    suits = [s for (_, s) in cards]
    return ranks, suits

#frequency of each rank. detecting pairs, trips, quads
def rank_count_dict(ranks):
    return dict(Counter(ranks))

#frequency of each suit
def suit_count_dict(suits):
    return dict(Counter(suits))

'''
#TEST
# example 7-card set (2 hole + 5 board)
cards = [(14,'h'), (14,'s'), (13,'h'), (13,'d'), (13,'c'), (9,'h'), (2,'d')]

ranks, suits = split_ranks_suits(cards)
rc = rank_count_dict(ranks)
sc = suit_count_dict(suits)

print("ranks:", ranks)   # [14, 14, 13, 13, 13, 9, 2]
print("suits:", suits)   # ['h','s','h','d','c','h','d']
print("rank counts:", rc)  # {14:2, 13:3, 9:1, 2:1}
print("suit counts:", sc)  # {'h':3, 's':1, 'd':2, 'c':1}
'''

#detecting STRAIGHTs tool
#return will give us the top number of the straight
def find_straight_top(ranks):
    r = sorted(set(ranks), reverse=True)
    #wheel straight - Ace -> 5
    if {14, 5, 4, 3, 2}.issubset(r):
        return 5
    #reg straights
    for i in range(len(r) - 4):
        if r[i] - r[i + 4] == 4:
            return r[i]

    return None

'''
#straight TEST
print(find_straight_top([14,13,12,11,10,8,7]))   # 14 (A-high)
print(find_straight_top([13,12,11,10,9]))        # 13 (K-high)
print(find_straight_top([14,5,4,3,2]))           # 5  (A-2-3-4-5)
print(find_straight_top([14,13,11,10,8]))        # None
'''

#FLUSHes and return top ranks of said flush
def find_flush_ranks(cards):
    #grouping cards by suit first
    suit_groups = {}
    for (r, s) in cards:
        suit_groups.setdefault(s, []).append(r)

    #find a suit with at least 5 cards
    for s, ranks in suit_groups.items():
        if len(ranks) >= 5:
            return sorted(ranks, reverse = True)[:5]

    #if no flushes
    return None

'''
#TESTING flushes
cards = [(14,'h'), (13,'h'), (9,'h'), (4,'h'), (2,'h'), (13,'s'), (9,'d')]
print("flush lol", find_flush_ranks(cards))
#flush here

cards = [(14,'h'), (13,'h'), (9,'s'), (4,'h'), (2,'d'), (13,'s'), (9,'d')]
print(find_flush_ranks(cards))
#no flush
'''

# rank patterns + 7 card eval
from collections import Counter

# sorting helper
def ranks_multiset_desc(ranks):
    return sorted(ranks, reverse=True)

# list of ranks sorted by count desc, then rank desc etc
def counts_by_rank_desc(ranks):
    c = Counter(ranks)
    return sorted(((cnt, r) for r, cnt in c.items()), key=lambda x: (x[0], x[1]), reverse=True)

# kickers included in 7 card ranking
def take_kickers(exclude_ranks_multiset, all_ranks_multiset, k):
    rem = all_ranks_multiset.copy()
    for r in exclude_ranks_multiset:
        rem.remove(r)
    return rem[:k]

# straight flush detection, return top rank if there
def straight_flush_top(cards):
    # group by suit first
    suit_groups = {}
    for (r, s) in cards:
        suit_groups.setdefault(s, []).append(r)

    for ranks_in_suit in suit_groups.values():
        if len(ranks_in_suit) >= 5:
            top = find_straight_top(ranks_in_suit)
            if top is not None:
                return top
    return None

# MAIN EVALUATION!! HAND EVALUATION
# producing a hand strength key, higher better. 9 straight flush, 8 quads, 7 full house ETC

def score7(hole, board5):
    cards = hole + board5

    # split and counts
    ranks, suits = split_ranks_suits(cards)
    all_multiset = ranks_multiset_desc(ranks)
    by_cnt_rank = counts_by_rank_desc(ranks)

    # extract rank groups
    quads = [r for (cnt, r) in by_cnt_rank if cnt == 4]
    trips = [r for (cnt, r) in by_cnt_rank if cnt == 3]
    pairs = [r for (cnt, r) in by_cnt_rank if cnt == 2]
    singles_desc = [r for (cnt, r) in by_cnt_rank if cnt == 1]

    # straight - flush - straightflush
    sf_top = straight_flush_top(cards)
    if sf_top is not None:
        return (9, [sf_top])

    # QUADS
    if quads:
        quad_rank = quads[0]
        exclude = [quad_rank] * 4
        kick = take_kickers(exclude, all_multiset, 1)[0]
        return (8, [quad_rank, kick])

    # full house (2 scenarios)
    # 1 - 2 trips
    if len(trips) >= 2:
        trip_rank = trips[0]
        pair_rank = trips[1]
        return (7, [trip_rank, pair_rank])

    # 2 - 1 trip/1 pair minimum
    if trips and pairs:
        trip_rank = trips[0]
        pair_rank = pairs[0]
        return (7, [trip_rank, pair_rank])

    # fluhhh
    flush_ranks5 = find_flush_ranks(cards)
    if flush_ranks5 is not None:
        return (6, flush_ranks5)

    # straight
    st_top = find_straight_top(ranks)
    if st_top is not None:
        return (5, [st_top])

    # trips
    if trips:
        t = trips[0]
        exclude = [t] * 3
        kickers = take_kickers(exclude, all_multiset, 2)
        return (4, [t] + kickers)

    # twopair
    if len(pairs) >= 2:
        high_pair, low_pair = pairs[0], pairs[1]
        exclude = [high_pair] * 2 + [low_pair] * 2
        kicker = take_kickers(exclude, all_multiset, 1)[0]
        return (3, [high_pair, low_pair, kicker])

    # pair
    if pairs:
        p = pairs[0]
        exclude = [p] * 2
        kickers = take_kickers(exclude, all_multiset, 3)
        return (2, [p] + kickers)

    # highcard
    return (1, all_multiset[:5])

'''
#TESTING HAND EVALUATION
# Royal flush board → tie
h1 = parse_cards(["2s","3d"])
h2 = parse_cards(["7h","9c"])
bd = parse_cards(["Ts","Js","Qs","Ks","As"])
assert score7(h1, bd) == score7(h2, bd)

# Quads vs full house
h1 = parse_cards(["Ah","Ad"]); bd = parse_cards(["As","Ac","Kd","7h","2c"])
h2 = parse_cards(["Kh","Kd"])
s1 = score7(h1, bd)  # quads A with K kicker → (8, [14,13])
s2 = score7(h2, bd)  # full house K over A  → (7, [...])
assert s1 > s2

# Straight flush beats quads
h1 = parse_cards(["9s","8s"]); bd = parse_cards(["7s","6s","5s","Qd","Qc"])
h2 = parse_cards(["Qh","Qd"])
assert score7(h1, bd) > score7(h2, bd)

# Trips vs two pair
h1 = parse_cards(["7d","7s"]); bd = parse_cards(["7h","Qd","Jc","4s","2h"])
h2 = parse_cards(["Jd","Qc"])
assert score7(h1, bd) > score7(h2, bd)
'''

#PREFLOP equities calculations

import random #LFG

def equity_preflop_mc(h1, h2, trials=1_000_000, seed=None):
    if seed is not None:
        random.seed(seed)

    deck = full_deck()
    used = h1 + h2
    rem = remove_cards(deck, used)

    w1 = w2 = t = 0
    for _ in range(trials):
        board5 = random.sample(rem, 5)
        s1 = score7(h1, board5)
        s2 = score7(h2, board5)
        if s1 > s2:
            w1 += 1
        elif s2 > s1:
            w2 += 1
        else:
            t += 1

    total = w1 + w2 + t
    eq1 = (w1 + t/2) / total
    eq2 = (w2 + t/2) / total
    tie_frac = t / total
    return eq1, eq2, tie_frac


# FLOP equity (exact because we are iterating every single turn and river ~990 scenarios)
from itertools import combinations

def equity_flop_exact(h1, h2, flop3):
    if len(flop3) != 3:
        raise ValueError("Flop must contain exactly three cards ser.")

    deck = full_deck()
    rem = remove_cards(deck, h1 + h2 + flop3)

    w1 = w2 = t = 0

    for turn, river in combinations(rem, 2):  # 990 combos
        board5 = flop3 + [turn, river]
        s1 = score7(h1, board5)
        s2 = score7(h2, board5)
        if s1 > s2:
            w1 += 1
        elif s2 > s1:
            w2 += 1
        else:
            t += 1

    total = w1 + w2 + t
    eq1 = (w1 + t / 2) / total
    eq2 = (w2 + t / 2) / total
    tie = t / total
    return eq1, eq2, tie


#TURN equity (44 combos)

def equity_turn_exact(h1, h2, board4):
    if len(board4) != 4:
        raise ValueError("Turn must contain 4 cards bruh")
    deck = full_deck()
    rem = remove_cards(deck, h1 + h2 + board4)

    w1 = w2 = t = 0
    for r in rem: #44 rivers
        board5 = board4 + [r]
        s1 = score7(h1, board5)
        s2 = score7(h2, board5)
        if s1 > s2: w1 += 1
        elif s2 > s1: w2 += 1
        else: t += 1

    total = w1 + w2 + t
    eq1 = (w1 + t/2) / total
    eq2 = (w2 + t/2) / total
    tie = t / total
    return eq1, eq2, tie

#RIVER equity

def equity_river(h1, h2, board5):

    if len(board5) != 5:
        raise ValueError("River must contain exactly 5 cards.")

    s1 = score7(h1, board5)
    s2 = score7(h2, board5)
    if s1 > s2: return 1.0, 0.0, 0.0
    if s2 > s1: return 0.0, 1.0, 0.0
    return 0.5, 0.5, 1.0


# INPUT SECTION
# Prompt driven.

def prompt_cards(msg, expected_n=None, allow_empty=False):
    while True:
        s = input(msg).strip()
        if allow_empty and s == "":
            return []
        parts = s.split()
        if expected_n is not None and len(parts) != expected_n:
            print(f"Please enter exactly {expected_n} cards seperated by spaces.")
            continue
        try:
            return parse_cards(parts)
        except ValueError as e:
            print(f"ErrorL {e}. Try again.")


def run():
    print("=== Heads-up Equity Calculator ===")
    print("Card format: Ah Kh Qs Jd 7h (use 'T' for tens/10).")
    print()

    # 1 hands
    h1 = prompt_cards("Enter Player 1 hand (2 cards): ", expected_n=2)
    h2 = prompt_cards("Enter Player 2 hand (2 cards): ", expected_n=2)

    # sanity
    try:
        remove_cards(full_deck(), h1 + h2)
    except ValueError as e:
        print(f"Card overlap in hands: {e}")
        return

    # pflp equities
    eq1, eq2, tie = equity_preflop_mc(h1, h2, trials=1_000_000, seed=42)
    print(f"Preflop: Player 1 - {eq1:.4f}, Player 2 - {eq2:.4f}, tie - {tie:.4f}")

    # flop (optional)
    flop = prompt_cards("Enter flop (3 cards), or press Enter to skip: ", expected_n=3, allow_empty=True)
    if not flop:
        return
    # sanity
    try:
        remove_cards(full_deck(), h1 + h2 + flop)
    except ValueError as e:
        print(f"Invalid flop (duplicates with hands?): {e}")
        return

    eq1, eq2, tie = equity_flop_exact(h1, h2, flop)
    print(f"Flop: Player 1 - {eq1:.4f}, Player 2 - {eq2:.4f}, tie - {tie:.4f}")

    # turn card! (single card, enter to skip)
    turn = prompt_cards("Enter a turn card, or press Enter to skip: ", expected_n=1, allow_empty=True)
    if not turn:
        return
    board4 = flop + turn

    try:
        remove_cards(full_deck(), h1 + h2 + board4)
    except ValueError as e:
        print(f"Invalid turn (duplicate card?): {e}")
        return

    eq1, eq2, tie = equity_turn_exact(h1, h2, board4)
    print(f"Turn: Player 1 - {eq1:.4f}, Player 2 - {eq2:.4f}, tie - {tie:.4f}")

    # riverrrrr (single card, enter to skip same)
    river = prompt_cards("Enter river card, or press Enter to skip: ", expected_n=1, allow_empty=True)
    if not river:
        return
    board5 = board4 + river
    print("FINAL BOARD:", fmt_cards(board5))

    try:
        remove_cards(full_deck(), h1 + h2 + board5)
    except ValueError as e:
        print(f"Invalid river (duplicate?): {e}")
        return

    eq1, eq2, tie = equity_river(h1, h2, board5)
    print(f"River: Player 1 - {eq1:.4f}, Player 2 - {eq2:.4f}, tie - {tie:.4f}")

# run() to run

if __name__ == "__main__":
    run()
