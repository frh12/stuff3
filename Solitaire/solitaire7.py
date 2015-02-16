# -*- coding: 1252 -*-
import pygame
import sys
import random
from pygame.locals import *
import pygame.mixer

WINDOWWIDTH = 1100
WINDOWHEIGHT = 600

cardimage = pygame.image.load('cards.bmp')
cardimageBack = pygame.image.load('back.bmp')
cardwidth = 73
cardheight = 98
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
backgroundImage = pygame.image.load('cat2.bmp')
background = pygame.Surface(screen.get_size())
heartimage = pygame.image.load('heart.bmp')
spadeimage = pygame.image.load('spade.bmp')
cloverimage = pygame.image.load('clover.bmp')
diamondimage = pygame.image.load('diamond.bmp')
newgameimage = pygame.image.load('newgame.bmp')
quitimage = pygame.image.load('quitgame.bmp')
instructionsimage = pygame.image.load('instructions.bmp')

# Card klasinn heldur utan um spilin
# Öll spilin eru búin til á sama punkti og eru öll á hvolfi
class Card:
    suits = {'C': 0, 'S': 1, 'H': 2, 'D': 3}
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.faceUp = False
        self.pos = (1000, 1000)
        self.image = pygame.Surface((cardwidth, cardheight))
        self.image.blit(cardimageBack, self.getCardImagePos())
        self.rect = self.image.get_rect()

    # sýnir framhlið spilsins self
    def showFace(self):
        self.image.blit(cardimage, self.getCardImagePos())
        self.render(screen)
        self.faceUp = True

    # sýnir bakhlið spilsins self    
    def showBack(self):
        self.image.blit(cardimageBack, self.getCardImagePos())
        self.render(screen)
        self.faceUp = False
        
    # skilar True ef self og card eru ekki sami litur
    def legalSuit(self, card):
        red = ['H', 'D']
        black = ['C', 'S']
        if (self.suit in red and card.suit in black) or (self.suit in black and card.suit in red):
            return True
        else:
            return False

    # endurskilgreinir staðsetningu spilsins self, nýja staðsetningin er pos
    # pos er tuple með x og y hniti
    def setPos(self, pos):
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
    # skilar x og y hniti self.image
    def getPos(self):
        return (self.rect.x, self.rect.y)
    
    # teiknar spilið self efst á screen
    def render(self, screen):
        screen.blit(self.image, self.pos)

    # þetta er fallið sem köttar spilin út úr myndinni cardimage
    def getCardImagePos(self):
        x = (self.rank-1) * cardwidth
        y = Card.suits[self.suit] * cardheight
        return (-x, -y)

    # tekur inn músarhnit, skilar True ef verið er að ýta á spil
    def isCardClick(self, mouse):
        return self.rect.collidepoint(mouse)

    # tekur inn rel sem er tuple með x og y hniti og skilgreinir hversu ...
    # skilgreinir nýja staðsetningu fyrir self spilið
    def changePos(self, rel):
        newPos = (self.pos[0] + rel[0], self.pos[1] + rel[1])
        self.setPos(newPos)


        
#Deck klasinn heldur utan um öll spilin, pushDeck og popDeck og allar raðirnar        
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for rank in range(1, 14) for suit in ['C', 'S', 'H', 'D']]
        random.shuffle(self.deck)
        self.popDeck = []
        self.pushDeck = []
        
        self.popDeckRect = pygame.Rect(20, 20, cardwidth, cardheight)
        self.pushDeckRect = pygame.Rect(120, 20, cardwidth, cardheight)
        self.render(screen, self.popDeckRect)
        self.render(screen, self.pushDeckRect)

        self.newsolitairegamebutton = pygame.Rect(790, 260, 120, 50)
        self.render(screen, self.newsolitairegamebutton)

        self.quitbutton = pygame.Rect(920, 260, 120, 50)
        self.render(screen, self.quitbutton)

        self.row = Row()
        self.render(screen, self.row.row1Rect)
        self.render(screen, self.row.row2Rect)
        self.render(screen, self.row.row3Rect)
        self.render(screen, self.row.row4Rect)
        self.render(screen, self.row.row5Rect)
        self.render(screen, self.row.row6Rect)
        self.render(screen, self.row.row7Rect)


    # tekur inn rectangle hlut og skilar staðsetningu hans
    def getPos(self, rect):
        return (rect[0], rect[1])
    
    # tekur inn obj og teiknar hann efst á screen
    def render(self, screen, obj):
        screen.blit(background, self.getPos(obj), obj)

    # setur fyrstu 24 spilin í self.deck í popDeck
    def fillDeck(self):
        for i in range(24):
            self.popDeck.append(self.deck[i])
        for card in self.popDeck:
            card.setPos((20, 20))

    # setur restina af spilunum í self.deck í raðirnar
    def fillRows(self):
        i = 0
        rowdeck = self.deck[24:]
        for i in range(7):
            for x in range(i+1):
                self.row.all_rows[i].append(rowdeck.pop(0))
            offset = 0
            for card in self.row.all_rows[i]:
                card.setPos(self.row.getPos((self.row.all_rowsRect[i][0], self.row.all_rowsRect[i][1] + offset)))
                offset += 20
            self.row.all_rows[i][-1].showFace()

    # skilar spilinu sem er verið að ýta á
    def whichFaceUpCard(self, mouse):
        for row in self.row.all_rows:
            for card in reversed(row):
                if card.faceUp and card.isCardClick(mouse):
                    return card

        for card in self.deck:
            if card.faceUp and card.isCardClick(mouse):
                return card
        return None

    # ef popDeck er ekki tómur þá poppar þetta efsta spilinu af popDeck yfir á pushDeck
    # ef popDeck er tómur þá er öllum spilunum í pushDeck poppað aftur yfir í popDeck
    def pushCardToDeck(self):
        if len(self.popDeck) > 0:
            card = self.popDeck.pop(0)
            self.pushDeck.append(card)
            card.setPos(self.getPos(self.pushDeckRect))
            card.showFace()
            
        else:
            length = len(self.pushDeck)
            for i in range(length):
                card = self.pushDeck.pop(0)
                self.popDeck.append(card)
                card.setPos(self.getPos(self.popDeckRect))
                card.showBack()


#þetta er highscore glugginn, sýnir efstu 10 highscorin og stigin sem leikmaður fékk í seinasta leik
#býður upp á að hefja nýjan leik eða hætta að spila
def win(points):
    screen = pygame.display.set_mode((600, 600))
    pygame.init()
    pygame.display.set_caption('Win!')
    bgcolor = (105, 5, 180)
    black = (0, 0, 0)
    text = []

    scoresfont = pygame.font.SysFont(None, 40)
    highscoresfont = pygame.font.SysFont(None, 60)
    
    scorestext = highscoresfont.render('Highscores:', True, black) 
    yourscore = scoresfont.render('Your score: %d' % points, True, black)

    newsolitairegamebutton = pygame.Rect(180, 490, 120, 50)
    quitbutton = pygame.Rect(310, 490, 120, 50)

    #nýjasta scoreinu bætt við scores.txt skrána sem heldur utan um öll scorein
    scorelist = open('scores.txt', 'a')
    scorelist.write(str(points) + '\n')
    scorelist.close()

    #hér eru öll scorein lesin úr skránni scores.txt yfir í listann highscores
    scorelist = open('scores.txt', 'r')
    highscores = []
    for line in scorelist:
        highscores.append(int(line))
    scorelist.close

    #highscores raðað í vaxandi röð
    highscores.sort()
    topten = []

    #topten listinn inniheldur 10 lægstu scorein
    if len(highscores) < 10:
        i = 0
        while i <= (len(highscores) - 1):
            s = highscores[i]
            topten.append(int(s))
            i += 1
    else:
        i = 0
        while i != 10:
            s = highscores[i]
            topten.append(int(s))
            i += 1
    
    j = 1
    for scores in topten:
        text.append(scoresfont.render((("%d. - ") % j) + str(scores), True, black))
        j += 1
            
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                #ýtt er á newgame takka
                if newsolitairegamebutton.collidepoint(mouse):
                    main()

                #ýtt er á quit takka
                elif quitbutton.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        
        screen.fill(bgcolor)
        screen.blit(scorestext, (180, 20))
        screen.blit(yourscore, (215, 430))
        
        screen.blit(background, (180, 490), newsolitairegamebutton)
        screen.blit(newgameimage, (180, 490))

        screen.blit(background, (310, 490), quitbutton)
        screen.blit(quitimage, (310, 490))
        
        i = 0
        for score in text:
            screen.blit(score, (265, 100 + i))
            i += 30
        pygame.display.flip()
        pygame.time.delay(0)


# eyðir spilum úr öllum röðunum, winningplace, pushDeck og popDeck
# núllstillir stigin og tímann
# setur ný spil í popDeck og raðirnar
def newsolitairegame(deck, winning, points):
    points = 0
    
    for row in deck.row.all_rows:
        for card in row:
            del card
    for card in deck.pushDeck:
        del card
    for card in deck.popDeck:
        del card
    for card in winning.all_cards:
        del card
    
    deck.fillDeck()
    deck.fillRows()


# winningPlace klasinn heldur utan um öll spil sem eru í einhverjum af winningPlace stöðunum
class winningPlace:
    def __init__(self):
        self.clover = [Card('C', 0)]
        self.spade = [Card('S', 0)]
        self.heart = [Card('H', 0)]
        self.diamond = [Card('D', 0)]

        self.cloverRect = pygame.Rect(320, 20, cardwidth, cardheight)
        self.spadeRect = pygame.Rect(420, 20, cardwidth, cardheight)
        self.heartRect = pygame.Rect(520, 20, cardwidth, cardheight)
        self.diamondRect = pygame.Rect(620, 20, cardwidth, cardheight)

        self.all_cards = [self.clover, self.spade, self.heart, self.diamond]
        self.all_placesRect = [self.cloverRect, self.spadeRect, self.heartRect, self.diamondRect]
        self.all_suits = ['C', 'S', 'H', 'D']

    # skilar staðsetningu rect
    def getPos(self, rect):
        return (rect[0], rect[1])

    # bætir currentCard í winning staðinn sem spilið er yfir
    def addToWinningPlace(self, currentCard, currentRow, winningPos, allCards):
        if currentCard.suit == allCards[-1].suit:
            currentCard.setPos(winningPos)
            allCards.append(currentCard)
            currentRow.remove(currentCard)
            #currentCard.render(screen)


# þessi klasi heldur utan um öll spilin sem eru í röðunum á borðinu
class Row:
    def __init__(self):
        self.row1 = []
        self.row2 = []
        self.row3 = []
        self.row4 = []
        self.row5 = []
        self.row6 = []
        self.row7 = []
        self.row1Rect = pygame.Rect(20, 140, cardwidth, cardheight)
        self.row2Rect = pygame.Rect(120, 140, cardwidth, cardheight)
        self.row3Rect = pygame.Rect(220, 140, cardwidth, cardheight)
        self.row4Rect = pygame.Rect(320, 140, cardwidth, cardheight)
        self.row5Rect = pygame.Rect(420, 140, cardwidth, cardheight)
        self.row6Rect = pygame.Rect(520, 140, cardwidth, cardheight)
        self.row7Rect = pygame.Rect(620, 140, cardwidth, cardheight)
        self.all_rows = [self.row1, self.row2, self.row3, self.row4, self.row5, self.row6, self.row7]
        self.all_rowsRect = [self.row1Rect, self.row2Rect, self.row3Rect, self.row4Rect, self.row5Rect, self.row6Rect, self.row7Rect]
        

    # skilar staðsetningu rect
    def getPos(self, rect):
        return (rect[0], rect[1])    


    # stafla spilum á borði
    def addCard(self, currentCard, currentRow, newRow, newRowRect):

        #þetta ef röðin sem verið er að reyna að stafla ofan á hefur engin spil
        if len(newRow) == 0 or newRow == []:
            i = 0
            if len(currentCard) == 1:
                currentCard[0].setPos(self.getPos(newRowRect))
                newRow.append(currentCard[0])
                currentRow.remove(currentCard[0])
            elif len(currentCard) > 1:
                for card in currentCard:
                    if i == 0:
                        card.setPos(self.getPos(newRowRect))
                        newRow.append(currentCard[0])
                        currentRow.remove(currentCard[0])
                        i += 1
                    else:
                        card.setPos(self.getPos((newRow[-1].rect[0], newRow[-1].rect[1] + 20)))
                        newRow.append(card)
                        currentRow.remove(card)

        #þetta ef verið er að stafla spilum ofan á spil
        else:           
            for card in currentCard:
                card.setPos(self.getPos((newRow[-1].rect[0], newRow[-1].rect[1] + 20)))
                newRow.append(card)
                currentRow.remove(card)


def main():
    pygame.init()

    pygame.display.set_caption('Solitaire')
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    deck = Deck()    
    winning = winningPlace()
    points = 0
    
    newsolitairegame(deck, winning, points)

    currentCard = []
    currentRow = None
    oldPos = []

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    frame_count = 0
    frame_rate = 60

    autocompletebutton = pygame.Rect(800, 20, 150, 50)
    
    while True:
        for event in pygame.event.get():            
            mouse = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


            if event.type == MOUSEMOTION:       
                rel = event.rel
                if len(currentCard) == 1:          
                    currentCard[0].changePos(rel)
                elif len(currentCard) > 1:
                    
                    for card in currentCard:
                        card.changePos(rel)

                        
            '''_________________________________________________________________________________________'''

            if event.type == MOUSEBUTTONDOWN:

                #newgame takki
                if deck.newsolitairegamebutton.collidepoint(mouse):
                    points = 0
                    deck = Deck()
                    winning = winningPlace()
                    newsolitairegame(deck, winning, points)
                    frame_count = 0
                    frame_rate = 60
                    total_seconds = frame_count // frame_rate

                #quit takki
                elif deck.quitbutton.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

                #ef maður ýtir á popDeckRect þá poppast spil af þeim lista yfir á pushDeck
                elif deck.popDeckRect.collidepoint(mouse):
                    deck.pushCardToDeck()


                elif len(currentCard) == 0:
                    
                    mouse = pygame.mouse.get_pos()
                    card = deck.whichFaceUpCard(mouse)

                    #detectar hvort verið sé að ýta á spil, má ekki vera í winningPlace
                    if card != None and card.rect not in winning.all_placesRect: 
                        currentCard.append(card)
                        oldPos.append(currentCard[0].pos)

                        #ef það er verið að ýta á pushDeck spil
                        if currentCard[0].getPos() == (deck.getPos(deck.pushDeckRect)):
                            currentCard = []
                            currentCard.append(deck.pushDeck[-1])
                            currentRow = (deck.pushDeck)

                        #ef það er verið að ýta á spil í röð
                        else:
                            for row in deck.row.all_rows:
                                for card in row:
                                    if currentCard[0].getPos() == card.getPos():
                                        if len(row) != 0:
                                            currentCard = []
                                            currentCard.append(deck.whichFaceUpCard(mouse))
                                            currentRow = row
                            for card in currentRow:
                                if card.faceUp and currentRow.index(card) > currentRow.index(currentCard[0]):
                                    currentCard.append(card)
                                    oldPos.append(card.pos)
                                    

            '''_____________________________________________________________________________________________________'''
            

            if event.type == MOUSEBUTTONUP:
                if currentCard != [] and currentRow:

                    #ef currentCard er yfir e-m winningRect
                    winningPos = None
                    all_cards = None
                    #winningcards = winning.all_cards

                    #tékka yfir hvaða winningRect spilið er statt
                    i = 0
                    for places in winning.all_placesRect:
                        if places.colliderect(currentCard[0].rect):
                            winningPos = places
                            all_cards = winning.all_cards[i]
                        else:
                            i += 1

                    
                    if winningPos != None and winningPos.colliderect(currentCard[0].rect):
                        if currentRow[-1] == currentCard[0]:
                            if (currentCard[0].suit == all_cards[-1].suit) and (currentCard[0].rank == (all_cards[-1].rank)+1):
                                winning.addToWinningPlace(currentCard[0], currentRow, winningPos, all_cards)
                                currentCard = []
                                currentRow = None
                                winningPos = None
                                all_cards = None
								

                                #tékkar hvort öll spilin séu komin í winningPlace  
                                cardcount = 0
                                for cards in winning.all_cards:
                                    if len(cards) == 14:
                                        cardcount += 13

                                #ef svo er þá eru highscorin birt
                                if cardcount == 52:
                                    win(points)

                    '''_____________________________________________________________________________________'''

                    #ef currentCard er yfir e-u rowRect
                    if currentCard != []: # and currentRow != None:
					
                        newRow = []
                        newRowRect = None
                        i = 0
                        lastCard = None
						
                        #leita í öllum röðunum hvort currentCard collidei við þær                        
                        for row in deck.row.all_rows:
                            if row == [] or len(row) == 0:
                                if row != currentRow and currentCard[0].rect.colliderect(deck.row.all_rowsRect[i]):
                                    newRowRect = deck.row.all_rowsRect[i]
                                    newRow = row
                                    break
                                else:
                                    i += 1
                            else:
                                lastCard = row[-1]
                                if row != currentRow and currentCard[0].rect.colliderect(lastCard):
                                    newRowRect = deck.row.all_rowsRect[i]
                                    newRow = row
                                    lastCard = newRow[-1]
                                    break
                                else:
                                    i += 1

                        #ef röðin sem við erum að reyna að setja spilið í er tóm, þá má bara setja kóng þangað
                        if len(newRow) == 0 and newRowRect != None:
                            if currentCard[0].rank == 13:
                                deck.row.addCard(currentCard, currentRow, newRow, newRowRect)
                                currentCard = []
                                oldPos = []
                                currentRow = None
                                newRow = []
                                newRowRect = None
                                points += 1

                        #ef hún er ekki tóm verður efsta spilið í currentCard að vera af annarri sort og einu lægra rank en neðsta spilið í newRow
                        elif (newRow != [] or len(newRow) != 0 or newRow != None) and newRowRect != None:
                            if lastCard.legalSuit(currentCard[0]) and lastCard.rank == ((currentCard[0].rank)+1):
                                deck.row.addCard(currentCard, currentRow, newRow, newRowRect)
                                currentCard = []
                                oldPos = []
                                currentRow = None
                                newRow = []
                                newRowRect = None
                                points += 1

                    '''_____________________________________________________________________________________'''
                                
    
                    #ef spilið er ekki staðsett á neinum leyfilegum rect þá fer það aftur á sama stað
                    if currentCard != [] and currentRow != None:
                        i = 0
                        for card in currentCard:
                            card.setPos(oldPos[i])
                            i += 1
                        currentCard = []
                        oldPos = []
                        currentRow = None

                currentCard = []
                currentRow = None
                oldPos = []
                

        screen.blit(backgroundImage, (0, 0))
        
        total_seconds = frame_count // frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        time = font.render(output_string, True, (255, 255, 255))
        screen.blit(time, [750, 80])

        frame_count += 1
        clock.tick(frame_rate)
        
        score = font.render("Score: " + str(points), True, (255, 255, 255))
        screen.blit(score, (750, 20))
        
        screen.blit(background, winning.getPos(winning.cloverRect), winning.cloverRect)
        screen.blit(cloverimage, winning.getPos(winning.cloverRect))
        screen.blit(background, winning.getPos(winning.spadeRect), winning.spadeRect)
        screen.blit(spadeimage, winning.getPos(winning.spadeRect))
        screen.blit(background, winning.getPos(winning.heartRect), winning.heartRect)
        screen.blit(heartimage, winning.getPos(winning.heartRect))
        screen.blit(background, winning.getPos(winning.diamondRect), winning.diamondRect)
        screen.blit(diamondimage, winning.getPos(winning.diamondRect))

        screen.blit(newgameimage, (790, 260))
        screen.blit(quitimage, (920, 260))
        screen.blit(instructionsimage, (750, 325))
        
        for card in deck.deck:
            card.render(screen)

        for i in range(7):
            for card in deck.row.all_rows[i]:
                if not deck.row.all_rows[i][-1].faceUp:
                    deck.row.all_rows[i][-1].showFace()
                card.render(screen)

        for i in range(4):
            for card in winning.all_cards[i]:
                card.render(screen)
        
        if currentCard != []:
            for card in currentCard:
                card.render(screen)

        pygame.display.flip()

if __name__ == '__main__':
    main()



















        
