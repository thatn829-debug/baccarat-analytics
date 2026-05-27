import random

def create_deck(num_decks=8):
    # Tạo bộ bài (10, J, Q, K tính là 0 điểm, Ace tính là 1)
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0] * 4
    deck = values * num_decks
    random.shuffle(deck)
    return deck

def calculate_score(cards):
    return sum(cards) % 10

def simulate_baccarat_hand(deck):
    if len(deck) < 6:
        return None, "Low cards"
    
    # Chia 2 lá đầu tiên
    player = [deck.pop(), deck.pop()]
    banker = [deck.pop(), deck.pop()]
    
    p_score = calculate_score(player)
    b_score = calculate_score(banker)
    
    # Luật thắng tự nhiên (Natural)
    if p_score >= 8 or b_score >= 8:
        return (p_score, b_score), "Natural"
        
    # Luật rút lá thứ 3 của Player
    p_third_card = None
    if p_score <= 5:
        p_third_card = deck.pop()
        player.append(p_third_card)
        p_score = calculate_score(player)
        
    # Luật rút lá thứ 3 của Banker (phụ thuộc vào lá thứ 3 của Player)
    if p_third_card is None:
        if b_score <= 5:
            banker.append(deck.pop())
    else:
        if b_score <= 2:
            banker.append(deck.pop())
        elif b_score == 3 and p_third_card != 8:
            banker.append(deck.pop())
        elif b_score == 4 and p_third_card in [2, 3, 4, 5, 6, 7]:
            banker.append(deck.pop())
        elif b_score == 5 and p_third_card in [4, 5, 6, 7]:
            banker.append(deck.pop())
        elif b_score == 6 and p_third_card in [6, 7]:
            banker.append(deck.pop())
            
    b_score = calculate_score(banker)
    return (p_score, b_score), "Normal"

# Chạy thử nghiệm 10,000 ván để xem tỷ lệ
deck = create_deck()
player_wins = 0
banker_wins = 0
ties = 0

for _ in range(10000):
    if len(deck) < 10:
        deck = create_deck()
    result, mode = simulate_baccarat_hand(deck)
    if result:
        p, b = result
        if p > b:
            player_wins += 1
        elif b > p:
            banker_wins += 1
        else:
            ties += 1

print(f"Kết quả sau 10,000 ván mô phỏng:")
print(f"Player thắng: {player_wins} ván ({player_wins/10000*100:.2f}%)")
print(f"Banker thắng: {banker_wins} ván ({banker_wins/10000*100:.2f}%)")
print(f"Hòa (Tie): {ties} ván ({ties/10000*100:.2f}%)")

