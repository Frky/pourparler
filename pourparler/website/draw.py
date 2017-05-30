
import sys
from random import shuffle

def collide(subjects, sub, part):
    for p, s in zip(part, sub):
        if p == s.author:
            return True
    return False

def random_draw(subjects):
    part = [s.author for s in subjects]
    sub = list(subjects)
    # Maximum number of draws: 100
    i = 0
    while i < 100 and collide(subjects, sub, part):
        shuffle(part)
        shuffle(sub)
        i += 1
    return sub, part

def display(sub, part):
    for i, (p, s) in enumerate(zip(part, sub)):
        print "{0}. {1} - {2} (propose par {3})".format(i + 1, p.user.username, s.text, s.author.user.username)

