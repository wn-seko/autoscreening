def score_to_number(score):
    if score == 'S':
        return 3
    if score == 'A':
        return 2
    if score == 'B':
        return 1
    if score == 'NG':
        return 0
    return None

def number_to_score(num):
    rounded = round(num)

    if rounded == 3:
        return 'S'
    if rounded == 2:
        return 'A'
    if rounded == 1:
        return 'B'
    if rounded == 0:
        return 'NG'
    return None
