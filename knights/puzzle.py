from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    
    Or(And(AKnight, And(AKnight, AKnave)),
    And(AKnave, Not(And(AKnight, AKnave))))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# A has to be a knave, B must be a knight
knowledge1 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    
    Or(And(AKnight, And(AKnave, BKnave)),
    And(AKnave, Not(And(AKnave, BKnave))))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    
    Or(
        (And(And(AKnight, BKnight), And(AKnight, BKnave))),
        (And(And(AKnave, BKnight), And(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave))))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    Not(And(CKnight, CKnave)),
    Or(CKnight, CKnave),
    And(Or(AKnight, AKnave), Or(AKnave, AKnight)),

    Or(
        And(
            And(AKnight, BKnight), AKnave, CKnave, AKnave),
        And(
            And(AKnight, BKnave), AKnight, CKnight, AKnight),
        And(
            And(AKnave, BKnight), AKnight, CKnave, AKnave),
        And(
            And(AKnave, BKnave), AKnight, CKnight, AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
