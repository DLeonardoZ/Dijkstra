import pygame as pg
import numpy as np

class MapaNode:
  def __init__(self, position, cost, parent = None):
    self.position = position
    self.cost = cost
    self.parent = parent

  def __eq__(self, other): 
    return self.position[0] == other.position[0] and self.position[1] == other.position[1]

class Dijkstra(object):
  def run(self, mapa, start, end):
    mapa = mapa.astype(np.float)

    unique, counts = np.unique(mapa, return_counts = True)
    nodosEnUno = counts[1]
    
    path = []
    vectorOfvisited = []
    vectorOflabeled = []
    
    mapaRows, mapaCols = np.shape(mapa)
    visited = np.zeros(mapa.shape)
    costs = np.zeros(mapa.shape)

    vectorOflabeled.append(MapaNode(start[::-1], 0))
    endNode = MapaNode(end[::-1], 0)

    while(len(vectorOfvisited) != nodosEnUno):
      currentNode = vectorOflabeled.pop(0)
      
      movements = ([[-1, -1, 1.4],
                    [0, -1, 1],
                    [1, -1, 1.4],
                    [-1, 0, 1],
                    [-1, 1, 1.4],
                    [0, 1, 1],
                    [1, 1, 1.4]])

      for movement in movements:
        newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
        adjacentNode = MapaNode(newPosition, currentNode.cost + movement[2], currentNode)

#Limite del mapa para nodos nuevos
        if newPosition[0] < 0 or newPosition[1] < 0 or newPosition [1] >= mapaCols or newPosition[0] >= mapaRows:
          continue
        elif mapa[newPosition[0]][newPosition[1]] == 0:
          continue
        elif visited[newPosition[0]][newPosition[1]] == 1:
          continue
        else:
          #Buscar si esta ya esta etiquetado
          encontrado = False
          for labeled in vectorOflabeled:
            if (labeled == adjacentNode):
              encontrado = True
              if(labeled.cost > adjacentNode.cost):
                labeled.cost = adjacentNode.cost
                costs[newPosition[0]][newPosition[1]] = adjacentNode.cost
                labeled.parent = currentNode
          if not encontrado:
            vectorOflabeled.append(adjacentNode)
            costs[newPosition[0]][newPosition[1]] = adjacentNode.cost
            
      vectorOfvisited.append(currentNode)
      if(currentNode == endNode):
        break
          
      visited[currentNode.position[0]][currentNode.position[1]] = 1
      vectorOflabeled = sorted(vectorOflabeled, key = lambda x: x.cost)

    for visitedNode in vectorOfvisited:
      if visitedNode == endNode:
        endNode = visitedNode
        break

    while endNode is not None:
      path.append(endNode.position)
      endNode = endNode.parent
    return path, visited, costs

pg.init()
mapaAlg = np.load("mapa.npy")
width, height = mapaAlg.shape

BLACK = pg.Color("black")
WHITE = pg.Color("White")
GREEN = pg.Color("green")
RED = pg.Color("red")
BLUE = pg.Color("blue")

color_light = (80, 80, 80)
color_dark = (50, 50, 50)

smallfont = pg.font.SysFont("Roboto", 30)
text = smallfont.render("Buscar", True, WHITE)
tile_size = 20

start = [1, 1]
goal = [14, 14]
topPadding = 50

search = Dijkstra()
screen = pg.display.set_mode((width*tile_size, height*tile_size + topPadding))
background = pg.Surface((width*tile_size, height*tile_size))
button = pg.Surface((width*tile_size, topPadding))

#Creador de cuadros
for y in range (0, height):
  for x in range (0, width):
    rect = (x*tile_size, y*tile_size, tile_size, tile_size)
    if(mapaAlg[y, x] == 0):
      color = BLACK
    else:
      color = WHITE
      if x == start[0] and y == start[1]:
        color = GREEN
      if x == goal[0] and y == goal[1]:
        color = RED
      pg.draw.rect(background, color, rect)

game_exit = False
while not game_exit:
  mouse = pg.mouse.get_pos()
  for event in pg.event.get():
    if event.type == pg.QUIT:
      game_exit = True
    if event.type == pg.MOUSEBUTTONDOWN:
      if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40:
        camino, mapavisited, costos = search.run(mapaAlg, start, goal)
        for point in camino:
          rect = (point[1]*tile_size, point[0]*tile_size, tile_size, tile_size)
          pg.draw.rect(background, BLUE, rect)

  if 0 <= mouse[0] <= 140 and 10 <= mouse[1] <= 40:
    pg.draw.rect(button, color_light, [10, 10, 140, 30])
  
  else:
    pg.draw.rect(button, color_dark, [10, 10, 140, 30])

  screen.fill((0, 0, 0))
  screen.blit(button, (0, 0))
  screen.blit(background, (0, topPadding))
  screen.blit(text, (45, 16))
  pg.display.flip()
pg.display.quit()