#利用角度判斷手勢
def strai(finger):
    return finger < 50

#大拇指
def is_good(f1, f2, f3, f4, f5):
    return strai(f1) and not strai(f2) and not strai(f3) and not strai(f4) and not strai(f5)

#中指
def is_middle(f1, f2, f3, f4, f5):
    return not strai(f1) and not strai(f2) and strai(f3) and not strai(f4) and not strai(f5)

#rock
def is_rock(f1, f2, f3, f4, f5):
    return strai(f1) and strai(f2) and not strai(f3) and not strai(f4) and strai(f5)

#ok
def is_ok(f2, f3, f4, f5):
    return not strai(f2) and strai(f3) and strai(f4) and strai(f5)

#0
def is_zero(f1, f2, f3, f4, f5):
    return not strai(f1) and not strai(f2) and not strai(f3) and not strai(f4) and not strai(f5)

#1
def is_one(f1, f2, f3, f4, f5):
    return not strai(f1) and strai(f2) and not strai(f3) and not strai(f4) and not strai(f5)

#2
def is_two(f1, f2, f3, f4, f5):
    return not strai(f1) and strai(f2) and strai(f3) and not strai(f4) and not strai(f5)

#3
def is_three(f1, f2, f3, f4, f5):
    return not strai(f1) and strai(f2) and strai(f3) and strai(f4) and not strai(f5)

#4
def is_four(f1, f2, f3, f4, f5):
    return not strai(f1) and strai(f2) and strai(f3) and strai(f4) and strai(f5)

#5
def is_five(f1, f2, f3, f4, f5):
    return strai(f1) and strai(f2) and strai(f3) and strai(f4) and strai(f5)

#6
def is_six(f1, f2, f3, f4, f5):
    return strai(f1) and not strai(f2) and not strai(f3) and not strai(f4) and strai(f5)

#7
def is_seven(f1, f2, f3, f4, f5):
    return strai(f1) and strai(f2) and not strai(f3) and not strai(f4) and not strai(f5)

#8
def is_eight(f1, f2, f3, f4, f5):
    return strai(f1) and strai(f2) and strai(f3) and not strai(f4) and not strai(f5)

#9s
def is_nine(f1, f2, f3, f4, f5):
    return strai(f1) and strai(f2) and strai(f3) and strai(f4) and not strai(f5)