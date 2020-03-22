import solitaire 
from termcolor import colored
import re
import time

SUITS_SYMBOLES = {
    solitaire.DIAMONDS: "♦",
    solitaire.CLUBS: "♣",
    solitaire.HEARTS: "♥",
    solitaire.SPADES: "♠"
}
VALUES_SYMBOLES = {
    "King": "K",
    "Queen": "Q",
    "Jack": "J",
    "10": "10",
    "9": "9",
    "8": "8",
    "7": "7",
    "6": "6",
    "5": "5",
    "4": "4",
    "3": "3",
    "2": "2",
    "Ace": "A"
}

CARD_DISPLAY_WIDTH = 3
EMPTY_STACK_STR = ("-" + " " * ((CARD_DISPLAY_WIDTH-1) // 2)).rjust(CARD_DISPLAY_WIDTH)
FACE_DOWN_CARD = "#"*CARD_DISPLAY_WIDTH


def cardString(card):
    return (VALUES_SYMBOLES[card.value]+SUITS_SYMBOLES[card.suit]).rjust(CARD_DISPLAY_WIDTH)


def coloredCardString(card):
    str = ''
    if (card.suit == solitaire.DIAMONDS or card.suit == solitaire.HEARTS):
        str = colored((VALUES_SYMBOLES[card.value] + SUITS_SYMBOLES[card.suit]).rjust(CARD_DISPLAY_WIDTH), 'red')
    if (card.suit == solitaire.CLUBS or card.suit == solitaire.SPADES):
        str = colored((VALUES_SYMBOLES[card.value] + SUITS_SYMBOLES[card.suit]).rjust(CARD_DISPLAY_WIDTH), 'grey')
    return str


def displayBoard(board):
    boardText = "Score: " + str(board.score) + "\n"
    boardText += (coloredCardString(board.diamondFoundation[-1]) if board.diamondFoundation.size > 0 else EMPTY_STACK_STR) + " "
    boardText += (coloredCardString(board.clubFoundation[-1]) if board.clubFoundation.size > 0 else EMPTY_STACK_STR) + " "
    boardText += (coloredCardString(board.heartFoundation[-1]) if board.heartFoundation.size > 0 else EMPTY_STACK_STR) + " "
    boardText += (coloredCardString(board.spadeFoundation[-1]) if board.spadeFoundation.size > 0 else EMPTY_STACK_STR) + " "
    boardText += " " * CARD_DISPLAY_WIDTH + " "
    boardText += (coloredCardString(board.waste[-1]) if board.waste.size > 0 else EMPTY_STACK_STR) + " "
    boardText += (FACE_DOWN_CARD if board.talon.size > 0 else EMPTY_STACK_STR) + " "
    boardText += "\n"
    boardText += ("-" * (CARD_DISPLAY_WIDTH + 1)) * solitaire.PILE_NUMBER + "\n"

    FaceUpPilesSizes = map(lambda stack: stack.size, board.faceUpPiles)
    FaceDownPilesSizes = map(lambda stack: stack.size, board.faceDownPiles)

    PilesSizes =  [a+b for a, b in zip(FaceUpPilesSizes, FaceDownPilesSizes)]

    maxPileSize = max(PilesSizes)

    if (maxPileSize > 0):
        for i in range(0, maxPileSize):
            for j in range(solitaire.PILE_NUMBER):
                faceDownPile = board.faceDownPiles[j]
                faceUpPile = board.faceUpPiles[j]
                if (faceDownPile.size + faceUpPile.size > 0):
                    if (i < faceDownPile.size):
                        boardText += FACE_DOWN_CARD + " "
                    elif (i < (faceDownPile.size + faceUpPile.size)):
                        boardText += coloredCardString(faceUpPile[i-faceDownPile.size]) + " "
                    else:
                        boardText += " " * CARD_DISPLAY_WIDTH + " "
                else:
                    boardText += (EMPTY_STACK_STR + " ") if i == 0 else (" " * CARD_DISPLAY_WIDTH + " ")
            boardText += "\n"
    else:
        boardText += (EMPTY_STACK_STR + " ") * solitaire.PILE_NUMBER

    print(boardText)

b = solitaire.Board()

displayBoard(b)
while True: 
    while True:
        cmd = input("Play: ")
        if cmd == "D":
            b.deal()
            break
        elif m := re.match('W>([0-7])', cmd):
            b.playWasteToPile(int(m.group(1)))
            break
        elif m := re.match('([0-7])>([0-7])', cmd):
            b.playPileToPile(int(m.group(1)), 0, int(m.group(2)))
            break
        elif m := re.match('([0-7]),([0-9]+)>([0-7])', cmd):
            b.playPileToPile(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            break
        elif m := re.match('([0-7])>([CSHD])', cmd):
            b.playPileToFoundation(int(m.group(1)), str(m.group(2)))
            break
        elif m := re.match('([CSHD])>([0-7])', cmd):
            b.playFoundationToPile(str(m.group(1)), int(m.group(2)))
            break
        elif m := re.match('W>([CSHD])', cmd):
            b.playWasteToFoundation(str(m.group(1)))
            break
        elif cmd == "exit":
            exit(0)
    displayBoard(b)
    if b.isResolved():
        while not b.isCompleted():
            b.playCompletionMove()
            time.sleep(.100)
            displayBoard(b)
        break
