rock = 'A'
paper = 'B'
scissors = 'C'

lose = 'X'
draw = 'Y'
win = 'Z'

pick_scores = {
    rock: 1,
    paper: 2,
    scissors: 3
}

your_pick = {
    'X': rock,
    'Y': paper,
    'Z': scissors
}

# their pick, your game state
your_pick_2 = {
    (rock, lose): scissors,
    (rock, draw): rock,
    (rock, win): paper,
    (paper, lose): rock,
    (paper, draw): paper,
    (paper, win): scissors,
    (scissors, lose): paper,
    (scissors, draw): scissors,
    (scissors, win): rock
}


# them, you
game_scores = {
    (rock, rock): 3,
    (rock, paper): 6,
    (rock, scissors): 0,
    (paper, rock): 0,
    (paper, paper): 3,
    (paper, scissors): 6,
    (scissors, rock): 6,
    (scissors, paper): 0,
    (scissors, scissors): 3
}


def main():
    inputs = []
    with open("input") as file:
        for line in file:
            inputs.append(line.strip().split(" "))

    total_score = 0
    for game in inputs:
        (them, you) = game[0], your_pick[game[1]]
        total_score += game_scores[(them, you)] + pick_scores[you];

    print(f"Total Score 1: {total_score}")

    total_score = 0
    for game in inputs:
        (them, gamestate) = game
        you = your_pick_2[(them, gamestate)]
        total_score += game_scores[(them, you)] + pick_scores[you]

    print(f"Total Score 2: {total_score}")


if __name__ == '__main__':
    main()
