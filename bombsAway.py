import random, pygame

pygame.init()

xy = 600
rows = 30
blockcount = 0
spaceBtwn = xy // rows
blocks = {}
antpos = []
clock = pygame.time.Clock()
bLimit = 7
keys = []

win = pygame.display.set_mode((xy, xy))
pygame.display.set_caption("Bombs Away!")

RED = (255, 0, 0)
GREEN = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def numberBlocks():
    global blocks
    global blockcount
    rowx = 0
    y = 0
    while y <= xy - spaceBtwn:
        for r in range(rowx, xy, spaceBtwn):
            blocks[blockcount] = [rowx, y, 0]
            rowx += spaceBtwn
            blockcount += 1
        y += spaceBtwn
        rowx = 0


numberBlocks()

# Make list of keys in blocks
for key in blocks.keys():
    keys.append(key)


def drawGrid(win, rows, xy):
    """Draw the grid the players and bombs will move in"""
    x = 0
    y = 0
    for l in range(rows):
        pygame.draw.line(win, (0, 0, 0), (x, 0), (x, xy))
        pygame.draw.line(win, (0, 0, 0), (0, y), (xy, y))

        x = x + spaceBtwn
        y = y + spaceBtwn


def redrawGameWindow():
    # Redraw Window
    win.fill(WHITE)
    ant.drawOnScreen()

    bombs = 0
    while bombs < bLimit:
        dropBomb()
        bombs += 1

    ant.update()
    ant.findMostSecure()

    # ant2.drawOnScreen()
    # ant2.update()
    # ant2.findMostSecure()

    drawGrid(win, rows, xy)
    resetDanger()
    pygame.display.update()


def yn(a, c):
    # decide if something, whether float or int is the same number
    b = a // c
    bb = a / c
    if b - bb == 0:
        return True
    else:
        return False


def findNeighbour(tag=0):
    global keys

    udlr = [tag + rows, tag - rows]

    # Don't allow for far right blocks to have right neighbours
    if not yn(tag + 1, rows):
        udlr.append(tag + 1)
        udlr.append(tag - rows + 1)
        udlr.append(tag + rows + 1)

    # Don't allow for far left blocks to have left neighbours
    if not yn(tag, rows):
        udlr.append(tag - 1)
        udlr.append(tag - rows - 1)
        udlr.append(tag + rows - 1)

    return udlr


class Ant:
    global blocks

    def __init__(self):
        self.blockn = chooseBlock(rows * 3, blockcount - (rows * 3))
        antpos.append(self.blockn)
        self.rect = (blocks[self.blockn][0], blocks[self.blockn][1], spaceBtwn, spaceBtwn)
        self.rectangle = pygame.Rect(self.rect)
        self.bls = []

    def get_danger(self):
        # reads what the danger level of the current block is
        danger = blocks[self.blockn][2]
        return danger

    def findMostSecure(self):
        a = 0
        for bl in findNeighbour(self.blockn):
            if blocks[bl][2] < self.get_danger() and 869 > bl > 30:
                self.blockn = bl

    def update(self):
        self.rect = (blocks[self.blockn][0], blocks[self.blockn][1], spaceBtwn, spaceBtwn)

    def drawOnScreen(self):
        self.update()
        draw(self.rect, BLACK)
        # Mark neighbour blocks as grey
        for bl in findNeighbour(self.blockn):
            self.bls.append(bl)
            draw((blocks[bl][0], blocks[bl][1], spaceBtwn, spaceBtwn), (220, 220, 220))


def chooseBlock(start, k):
    return random.randint(start, k)


def draw(rect, color):
    global win, spaceBtwn
    r = pygame.Rect(rect)
    pygame.draw.rect(win, color, r)


ant = Ant()


# ant2 = Ant()

def dropBomb():
    a = chooseBlock(0, blockcount)
    while a == blocks[ant.blockn]:
        a = chooseBlock(rows, blockcount)
    draw((blocks[a][0], blocks[a][1], spaceBtwn, spaceBtwn), RED)
    bs = findNeighbour(a)
    blocks[a][2] += 1
    for b in bs:
        draw((blocks[b][0], blocks[b][1], spaceBtwn, spaceBtwn), (247, 152, 98))
        if blocks[b][2] < 3:
            blocks[b][2] += 1


def resetDanger():
    for n in range(0, blockcount):
        blocks[n][2] = 0


# main loop
def main():
    global ant
    run = True
    pygame.time.get_ticks()

    while run:
        clock.tick(1.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        try:
            redrawGameWindow()
        except:
            pass

        print('The current Level of Danger is:  ' + str(blocks[ant.blockn][2]))


print(findNeighbour(ant.blockn))
main()

# finished by Timothee B. on 20th of Oktober 2020.
