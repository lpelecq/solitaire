# Import the base classes:
import pydealer

DIAMONDS = "Diamonds"
CLUBS = "Clubs"
HEARTS = "Hearts"
SPADES = "Spades"

SOLITAIRE_RANK = {
    "values": {
        "King": 13,
        "Queen": 12,
        "Jack": 11,
        "10": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "Ace": 1
    },
    "suits": {
        SPADES: 4,
        HEARTS: 3,
        CLUBS: 2,
        DIAMONDS: 1
    }
}

PILE_NUMBER = 7


def canBePlaced(topCard, bottomCard):
    if ((bottomCard.suit == DIAMONDS or bottomCard.suit == HEARTS) and (topCard.suit == DIAMONDS or topCard.suit == HEARTS)
        or (bottomCard.suit == CLUBS or bottomCard.suit == SPADES) and (topCard.suit == CLUBS or topCard.suit == SPADES)):
        return False
    return SOLITAIRE_RANK["values"][bottomCard.value] == (SOLITAIRE_RANK["values"][topCard.value] + 1)

class Board:
    def __init__(self):
        self.score = 0
        self.deck = pydealer.Deck()
        self.talon = pydealer.Stack()
        self.waste = pydealer.Stack()
        self.diamondFoundation = pydealer.Stack(ranks=SOLITAIRE_RANK)
        self.clubFoundation = pydealer.Stack(ranks=SOLITAIRE_RANK)
        self.heartFoundation = pydealer.Stack(ranks=SOLITAIRE_RANK)
        self.spadeFoundation = pydealer.Stack(ranks=SOLITAIRE_RANK)
        self.faceDownPiles = []
        for i in range(PILE_NUMBER):
            self.faceDownPiles.append(pydealer.Stack())        
        self.faceUpPiles = []
        for i in range(PILE_NUMBER):
            self.faceUpPiles.append(pydealer.Stack())

        self.deck.shuffle()

        for i in range(PILE_NUMBER):
            for j in range((PILE_NUMBER-1)-i):
                self.faceDownPiles[(PILE_NUMBER-1)-j].add(self.deck.deal())
        
        for faceUpPile in self.faceUpPiles:
            faceUpPile.add(self.deck.deal())

        self.talon.add(self.deck.deal(self.deck.size))

    def deal(self):
        if self.talon.size == 0:
            self.talon.add(self.waste.deal(self.waste.size))
        self.waste.add(self.talon.deal())


    def playWasteToPile(self, destinationPileIndex):
        if self.waste.size > 0:
            if (self.faceUpPiles[destinationPileIndex].size == 0) and (self.waste[-1].value == "King"):
                self.faceUpPiles[destinationPileIndex].add(self.waste.deal())
                self.score += 5
            if (self.faceUpPiles[destinationPileIndex].size > 0) and canBePlaced(self.waste[-1], self.faceUpPiles[destinationPileIndex][-1]):
                self.faceUpPiles[destinationPileIndex].add(self.waste.deal())
                self.score += 5
    
    def playPileToPile(self, sourcePileIndex, movedCardIndex, destinationPileIndex):
        if self.faceUpPiles[sourcePileIndex].size > movedCardIndex:
            if (self.faceUpPiles[destinationPileIndex].size == 0) and (self.faceUpPiles[sourcePileIndex][movedCardIndex].value == "King"):
                movedCards = self.faceUpPiles[sourcePileIndex].deal(self.faceUpPiles[sourcePileIndex].size - movedCardIndex)
                movedCards.reverse()
                self.faceUpPiles[destinationPileIndex].add(movedCards)
            elif (self.faceUpPiles[destinationPileIndex].size > 0) and canBePlaced(self.faceUpPiles[sourcePileIndex][movedCardIndex], self.faceUpPiles[destinationPileIndex][-1]):
                movedCards = self.faceUpPiles[sourcePileIndex].deal(self.faceUpPiles[sourcePileIndex].size - movedCardIndex)
                movedCards.reverse()
                self.faceUpPiles[destinationPileIndex].add(movedCards)
        if self.faceUpPiles[sourcePileIndex].size == 0:
            self.faceUpPiles[sourcePileIndex].add(self.faceDownPiles[sourcePileIndex].deal())
            self.score += 5
    
    def playPileToFoundation(self, sourcePileIndex, destinationFoundation):
        if self.faceUpPiles[sourcePileIndex].size > 0:
            if destinationFoundation == "D":
                card = self.faceUpPiles[sourcePileIndex][self.faceUpPiles[sourcePileIndex].size-1]
                if (card.suit == DIAMONDS) and (card.value == "Ace" or ((self.diamondFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.diamondFoundation[-1].value] + 1)))):
                    self.diamondFoundation.add(self.faceUpPiles[sourcePileIndex].deal())
                    self.score += 10
            elif destinationFoundation == "C":
                card = self.faceUpPiles[sourcePileIndex][self.faceUpPiles[sourcePileIndex].size-1]
                if (card.suit == CLUBS) and (card.value == "Ace" or ((self.clubFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.clubFoundation[-1].value] + 1)))):
                    self.clubFoundation.add(self.faceUpPiles[sourcePileIndex].deal())
                    self.score += 10
            elif destinationFoundation == "H":
                card = self.faceUpPiles[sourcePileIndex][self.faceUpPiles[sourcePileIndex].size-1]
                if (card.suit == HEARTS) and (card.value == "Ace" or ((self.heartFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.heartFoundation[-1].value] + 1)))):
                    self.heartFoundation.add(self.faceUpPiles[sourcePileIndex].deal())
                    self.score += 10
            elif destinationFoundation == "S":
                card = self.faceUpPiles[sourcePileIndex][self.faceUpPiles[sourcePileIndex].size-1]
                if (card.suit == SPADES) and (card.value == "Ace" or ((self.spadeFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.spadeFoundation[-1].value] + 1)))):
                    self.spadeFoundation.add(self.faceUpPiles[sourcePileIndex].deal())
                    self.score += 10
        if self.faceUpPiles[sourcePileIndex].size == 0:
            self.faceUpPiles[sourcePileIndex].add(self.faceDownPiles[sourcePileIndex].deal())
            self.score += 5

    def playFoundationToPile(self, sourceFoundation, destinationPileIndex):
        if sourceFoundation == "D":
            if (self.diamondFoundation.size > 0) and (self.faceUpPiles[destinationPileIndex].size > 0):
                if canBePlaced(self.diamondFoundation[self.diamondFoundation.size-1], self.faceUpPiles[destinationPileIndex][-1]):
                    self.faceUpPiles[destinationPileIndex].add(self.diamondFoundation.deal())
                    self.score = max(0, self.score - 15)
        elif sourceFoundation == "C":
            if (self.clubFoundation.size > 0) and (self.faceUpPiles[destinationPileIndex].size > 0):
                if canBePlaced(self.clubFoundation[self.clubFoundation.size-1], self.faceUpPiles[destinationPileIndex][-1]):
                    self.faceUpPiles[destinationPileIndex].add(self.clubFoundation.deal())
                    self.score = max(0, self.score - 15)
        elif sourceFoundation == "H":
            if (self.heartFoundation.size > 0) and (self.faceUpPiles[destinationPileIndex].size > 0):
                if canBePlaced(self.heartFoundation[self.heartFoundation.size-1], self.faceUpPiles[destinationPileIndex][-1]):
                    self.faceUpPiles[destinationPileIndex].add(self.heartFoundation.deal())
                    self.score = max(0, self.score - 15)
        elif sourceFoundation == "S":
            if (self.spadeFoundation.size > 0) and (self.faceUpPiles[destinationPileIndex].size > 0):
                if canBePlaced(self.spadeFoundation[self.spadeFoundation.size-1], self.faceUpPiles[destinationPileIndex][-1]):
                    self.faceUpPiles[destinationPileIndex].add(self.spadeFoundation.deal())
                    self.score = max(0, self.score - 15)
        

    def playWasteToFoundation(self, destinationFoundation):
        if destinationFoundation == "D":
            if self.waste.size > 0:
                card = self.waste[-1]
                if (self.waste[-1].suit == DIAMONDS) and ((card.value == "Ace") or ((self.diamondFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.diamondFoundation[-1].value] + 1)))):
                    self.diamondFoundation.add(self.waste.deal())
                    self.score += 10
        elif destinationFoundation == "C":
            if self.waste.size > 0:
                card = self.waste[-1]
                if (self.waste[-1].suit == CLUBS) and ((card.value == "Ace") or ((self.clubFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.clubFoundation[-1].value] + 1)))):
                    self.clubFoundation.add(self.waste.deal())
                    self.score += 10
        elif destinationFoundation == "H":
            if self.waste.size > 0:
                card = self.waste[-1]
                if (self.waste[-1].suit == HEARTS) and ((card.value == "Ace") or ((self.heartFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.heartFoundation[-1].value] + 1)))):
                    self.heartFoundation.add(self.waste.deal())
                    self.score += 10
        elif destinationFoundation == "S":
            if self.waste.size > 0:
                card = self.waste[-1]
                if (self.waste[-1].suit == SPADES) and ((card.value == "Ace") or ((self.spadeFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.spadeFoundation[-1].value] + 1)))):
                    self.spadeFoundation.add(self.waste.deal())
                    self.score += 10

    def isResolved(self):
        return sum(map(lambda stack: stack.size, self.faceDownPiles)) == 0

    def isCompleted(self):
        return sum(map(lambda stack: stack.size, [self.diamondFoundation, self.clubFoundation, self.heartFoundation, self.spadeFoundation])) == 52

    def playCompletionMove(self):
        if self.isResolved():
            for faceUpPile in self.faceUpPiles:
                if faceUpPile.size > 0:
                    card = faceUpPile[-1]
                    if card.suit == DIAMONDS:
                        if (card.value == "Ace") or ((self.diamondFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.diamondFoundation[-1].value] + 1))):
                            self.diamondFoundation.add(faceUpPile.deal())
                            self.score += 10
                            return
                    elif card.suit == CLUBS:
                        if (card.value == "Ace") or ((self.clubFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.clubFoundation[-1].value] + 1))):
                            self.clubFoundation.add(faceUpPile.deal())
                            self.score += 10
                            return
                    elif card.suit == HEARTS:
                        if (card.value == "Ace") or ((self.heartFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.heartFoundation[-1].value] + 1))):
                            self.heartFoundation.add(faceUpPile.deal())
                            self.score += 10
                            return
                    elif card.suit == SPADES:
                        if (card.value == "Ace") or ((self.spadeFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.spadeFoundation[-1].value] + 1))):
                            self.spadeFoundation.add(faceUpPile.deal())
                            self.score += 10
                            return
            if self.waste.size > 0:
                card = self.waste[-1]
                if (self.waste[-1].suit == DIAMONDS) and ((card.value == "Ace") or ((self.diamondFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.diamondFoundation[-1].value] + 1)))):
                    self.diamondFoundation.add(self.waste.deal())
                    self.score += 10
                    return
                elif (self.waste[-1].suit == CLUBS) and ((card.value == "Ace") or ((self.clubFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.clubFoundation[-1].value] + 1)))):
                    self.clubFoundation.add(self.waste.deal())
                    self.score += 10
                    return
                elif (self.waste[-1].suit == HEARTS) and ((card.value == "Ace") or ((self.heartFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.heartFoundation[-1].value] + 1)))):
                    self.heartFoundation.add(self.waste.deal())
                    self.score += 10
                    return
                elif (self.waste[-1].suit == SPADES) and ((card.value == "Ace") or ((self.spadeFoundation.size > 0) and (SOLITAIRE_RANK["values"][card.value] == (SOLITAIRE_RANK["values"][self.spadeFoundation[-1].value] + 1)))):
                    self.spadeFoundation.add(self.waste.deal())
                    self.score += 10
                    return
            self.deal()
            return