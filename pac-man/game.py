import pygame
from math import *

def inLine(v1,v2,position):
	if v1[0]==v2[0]:
		if position[0]==v1[0] and (position[1]-v1[1])*(position[1]-v2[1])<=0:
			return True
	else:
		if position[1]==v1[1] and (position[0]-v1[0])*(position[0]-v2[0])<=0:
			return True
	return False

class Graph:
	def __init__(self,vertices,edges):
		self.vertices = vertices
		self.edges = edges
	def display(self,win):
		for edge in self.edges:
			v1 = self.vertices[edge[0]]
			v2 = self.vertices[edge[1]]
			pygame.draw.line(win,(0,255,0),v1,v2,1)
			pygame.draw.circle(win,(255,0,0),v1,10)
			pygame.draw.circle(win,(255,0,0),v2,10)

class Player:
	def __init__(self,position):
		self.position = position
		self.points = 0
		self.image = pygame.image.load("pac-man-sprites/r0.png")
		self.rimageList = [pygame.image.load("pac-man-sprites/r0.png"),pygame.image.load("pac-man-sprites/r1.png"),pygame.image.load("pac-man-sprites/r2.png"),pygame.image.load("pac-man-sprites/r3.png"),pygame.image.load("pac-man-sprites/r4.png")]
		self.limageList = [pygame.image.load("pac-man-sprites/l0.png"),pygame.image.load("pac-man-sprites/l1.png"),pygame.image.load("pac-man-sprites/l2.png"),pygame.image.load("pac-man-sprites/l3.png"),pygame.image.load("pac-man-sprites/l4.png")]
		self.uimageList = [pygame.image.load("pac-man-sprites/u0.png"),pygame.image.load("pac-man-sprites/u1.png"),pygame.image.load("pac-man-sprites/u2.png"),pygame.image.load("pac-man-sprites/u3.png"),pygame.image.load("pac-man-sprites/u4.png")]
		self.dimageList = [pygame.image.load("pac-man-sprites/d0.png"),pygame.image.load("pac-man-sprites/d1.png"),pygame.image.load("pac-man-sprites/d2.png"),pygame.image.load("pac-man-sprites/d3.png"),pygame.image.load("pac-man-sprites/d4.png")]
		self.rcount = 0
		self.lcount = 0
		self.ucount = 0
		self.dcount = 0
		self.ri = 0
		self.li = 0
		self.ui = 0
		self.di = 0

	def setGraph(self,graph):
		self.graph = graph

	def display(self,win):
		win.blit(self.image,(self.position[0]-20,self.position[1]-20))

	def pathDisplay(self,win):
		pos1 = self.position
		graph = self.graph
		vindex = 0
		for edge in graph.edges:
			v1 = graph.vertices[edge[0]]
			v2 = graph.vertices[edge[1]]
			if inLine(v1,v2,pos1):
				if length(v1,pos1)<length(v2,pos1):
					vindex = edge[0]
				else:
					vindex = edge[1]
		spt = shortestPathTree(vindex,graph)
		for edge in spt:
			v1 = graph.vertices[edge[0]]
			v2 = graph.vertices[edge[1]]
			pygame.draw.line(win,(0,0,255),v1,v2,1)


	def translatex(self,x):
		pos1 = [self.position[0]+x,self.position[1]]
		graph = self.graph
		val = False
		for edge in graph.edges:
			v1 = graph.vertices[edge[0]]
			v2 = graph.vertices[edge[1]]
			if inLine(v1,v2,pos1):
				val = True
		if val:
			if x>0:
				self.rcount += 1
				if self.rcount > 10:
					self.ri = (self.ri+1)%5
					self.image = self.rimageList[self.ri]
					self.rcount = 0

			else:
				self.lcount += 1
				if self.lcount > 10:
					self.li = (self.li+1)%5
					self.image = self.limageList[self.li]
					self.lcount = 0
			self.position = pos1

	def translatey(self,y):
		pos1 = [self.position[0],self.position[1]+y]
		graph = self.graph
		val = False
		for edge in graph.edges:
			v1 = graph.vertices[edge[0]]
			v2 = graph.vertices[edge[1]]
			if inLine(v1,v2,pos1):
				val = True
		if val:
			if y>0:
				self.dcount += 1
				if self.dcount > 10:
					self.di = (self.di+1)%5
					self.image = self.dimageList[self.di]
					self.dcount = 0
			else:
				self.ucount += 1
				if self.ucount > 10:
					self.ui = (self.ui+1)%5
					self.image = self.uimageList[self.ui]
					self.ucount = 0
			self.position = pos1

class Vertex:
	def __init__(self,v,dist):
		self.v = v
		self.dist = dist
	def __str__(self):
		return "("+str(self.v[0])+","+str(self.v[1])+","+str(self.dist)+")"

def length(u,v):
	return sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2)

def shortestPathTree(vindex,graph):
	vertices = []
	edges = graph.edges.copy()
	for vertice in graph.vertices:
		vertices.append(Vertex(vertice,0))
	source = vertices[vindex]
	S = set()
	S.add(source)
	spt = set()

	while len(S)!=len(graph.vertices):
		mindist = 1000000
		minu = 0
		minw = 0
		minedge = 0
		for edge in edges:
			if vertices[edge[0]] in S and vertices[edge[1]] not in S:
				u,w,e = vertices[edge[0]], vertices[edge[1]], edge
				if (u.dist + length(u.v,w.v)<mindist):
					minu = u
					minw = w
					minedge = e
					mindist = u.dist + length(u.v,w.v)
			elif vertices[edge[1]] in S and vertices[edge[0]] not in S:
				u,w,e = vertices[edge[1]], vertices[edge[0]], edge
				if (u.dist + length(u.v,w.v)<mindist):
					minu = u
					minw = w
					minedge = e
					mindist = u.dist + length(u.v,w.v)

		minw.dist = mindist
		S.add(minw)
		spt.add(tuple(minedge))
	return spt

class Enemy:
	def __init__(self,curindex,graph,player,dmap):
		self.graph = graph
		self.player = player
		self.dmap = dmap
		self.curindex = curindex
		self.curpos = self.graph.vertices[self.curindex].copy()
		self.nexindex = 0
		self.boolfind = True
		self.image = pygame.image.load("enemy3.png")

	def display(self,win):
		win.blit(self.image,(self.curpos[0]-20,self.curpos[1]-20))

	def translate(self):
		cur = self.curpos
		nex = self.nexpos
		if cur[0] == nex[0] and cur[1] == nex[1]:
			self.boolfind = True
			self.curindex = self.nexindex
		elif cur[1] == nex[1]:
			if nex[0] > cur[0]:
				cur[0] = cur[0] + 1
			else:
				cur[0] = cur[0] - 1
		elif cur[0] == nex[0]:
			if nex[1] > cur[1]:
				cur[1] = cur[1] + 1
			else:
				cur[1] = cur[1] - 1


	def run(self):
		if self.boolfind == False:
			self.translate()
		else:
			self.findNexIndex()

	def findNexIndex(self):
		pos1 = self.player.position
		graph = self.graph
		pindex = 0
		for edge in graph.edges:
			v1 = graph.vertices[edge[0]]
			v2 = graph.vertices[edge[1]]
			if inLine(v1,v2,pos1):
				if length(v1,pos1)<length(v2,pos1):
					pindex = edge[0]
				else:
					pindex = edge[1]

		parent = self.curindex
		d = self.dmap[self.curindex]
		for child in d[self.curindex]:
			if func(parent,child,pindex,d):
				self.nexindex = child
				self.boolfind = False
				self.curpos = self.graph.vertices[self.curindex].copy()
				self.nexpos = self.graph.vertices[self.nexindex].copy()
				break

	def catchPlayer(self):
		if length(self.curpos,self.player.position) <= 20:
			return True
		return False

def func(parent,child,pindex,d):
	if child == pindex:
		return True
	count = 0
	for node in d[child]:
		if node != parent:
			count+=1
	if count == 0:
		return False
	val = False
	for node in d[child]:
		if node!= parent:
			if func(child,node,pindex,d):
				return True
	return False


class MushRooms:
	def __init__(self,file):
		self.mushset = set()
		self.initiate(file)
		self.number = len(self.mushset)

	def initiate(self,file):
		s = file.read()
		l = s.split("\n")
		for j in range(len(l)):
			for i in range(len(l[j])):
				if l[j][i]=="." :
					x,y = (60+i*40,60+j*40)
					self.mushset.add((x,y))
		file.close()

	def display(self,win):
		for i in self.mushset:
			pygame.draw.circle(win,(255,255,255),i,5)

	def update(self,player):
		ptopleftx, ptoplefty = player.position[0]-20, player.position[1]-20
		pbottomrightx , pbottomrighty = player.position[0]+20, player.position[1]+20
		temp = []
		for x,y in self.mushset:
			if ptopleftx<=x<=pbottomrightx and ptoplefty<=y<=pbottomrighty:
				temp.append((x,y))
		for x,y in temp:
			self.mushset.remove((x,y))
			self.number -= 1
			player.points += 1

class Button:
	def __init__(self,text,textsize,fg,bg,center):
		self.text = text
		self.textsize = textsize
		self.fg = fg
		self.bg = bg
		self.center = center
		self.font = pygame.font.Font('freesansbold.ttf',32)
		self.textObject = self.font.render(text,True,fg,bg)
		self.rectObject = self.textObject.get_rect()
		self.rectObject.center = center

	def onClick(self):
		x,y = pygame.mouse.get_pos()
		if self.rectObject.collidepoint((x,y)):
			return True
		return False

	def display(self,win):
		win.blit(self.textObject,self.rectObject)

def loseMenu(win,player):
	backbutton = Button("     Back     ",32, (0,255,0), (0,0,255), (50,500))
	font = pygame.font.Font('freesansbold.ttf',32)
	text1 = font.render("   YOU LOSE !   ",True,(255,0,0),(255,255,0))
	textrect1 = text1.get_rect()
	textrect1.center = (300,300)

	text2 = font.render(" YOUR SCORE :- "+str(player.points),True,(255,0,0),(255,255,0))
	textrect2 = text2.get_rect()
	textrect2.center = (300,350)

	run = True
	while run:
		win.fill((0,0,0))
		win.blit(text1,textrect1)
		win.blit(text2,textrect2)
		backbutton.display(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if backbutton.onClick():
					run = False

		pygame.display.update()


def winMenu(win,player):
	backbutton = Button("     Back     ",32, (0,255,0), (0,0,255), (50,500))
	font = pygame.font.Font('freesansbold.ttf',32)
	text = font.render("   YOU WIN !   ",True,(255,0,0),(255,255,0))
	textrect = text.get_rect()
	textrect.center = (300,300)

	run = True
	while run:
		win.fill((0,0,0))
		win.blit(text,textrect)
		backbutton.display(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if backbutton.onClick():
					run = False

		pygame.display.update()



def gamePlay(win):
	image = pygame.image.load("maze1.png")
	graph = Graph(vertices=[[20,300],[60,300],[60,220],[100,220],[140,220],[140,300],[140,380],[100,380],[60,380],[100,460],[140,460],[140,500],[140,540],[60,540],[60,460],[100,140],[60,140],[60,60],[140,60],[140,100],[140,140],[220,140],[220,100],[220,60],[300,60],[380,60],[380,100],[380,140],[300,140],[460,100],[460,60],[540,60],[540,140],[500,140],[460,140],[500,220],[540,220],[540,300],[540,380],[500,380],[460,380],[460,300],[460,220],[500,460],[540,460],[540,540],[460,540],[460,500],[460,460],[380,500],[380,540],[300,540],[220,540],[220,500],[220,460],[300,460],[380,460],[220,380],[220,300],[220,220],[300,220],[380,220],[380,300],[380,380],[300,380],[300,300],[300,20],[580,300],[300,580]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,1],[7,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,9],[3,15],[15,16],[16,17],[17,18],[18,19],[19,20],[20,15],[19,22],[22,23],[23,24],[24,25],[25,26],[26,27],[27,28],[28,21],[21,22],[26,29],[29,30],[30,31],[31,32],[32,33],[33,34],[34,29],[33,35],[35,36],[36,37],[37,38],[38,39],[39,40],[40,41],[41,42],[42,35],[39,43],[43,44],[44,45],[45,46],[46,47],[47,48],[48,43],[47,49],[49,50],[50,51],[51,52],[52,53],[53,54],[54,55],[55,56],[56,49],[53,11],[28,60],[41,62],[55,64],[5,58],[59,60],[60,61],[61,62],[62,63],[63,64],[64,57],[57,58],[58,59],[58,65],[60,65],[62,65],[64,65],[24,66],[37,67],[51,68]])
	player = Player([20,300])
	player.setGraph(graph)

	dmap = {}
	for i in range(len(graph.vertices)):
		spt = list(shortestPathTree(i,graph))
		d = {}
		for j in range(len(graph.vertices)):
			d[j] = []
		for edge in spt:
			v1 = edge[0]
			v2 = edge[1]
			if v2 not in d[v1]:
				d[v1].append(v2)
			if v1 not in d[v2]:
				d[v2].append(v1)
		dmap[i] = d

	enemy = Enemy(67,graph,player,dmap)
	mushrooms = MushRooms(open("mush.txt","r"))

	winbool = True

	run = True
	pathbool = False
	while run:
		pygame.time.delay(6)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			player.translatex(-1)
		if keys[pygame.K_d]:
			player.translatex(1)
		if keys[pygame.K_w]:
			player.translatey(-1)
		if keys[pygame.K_s]:
			player.translatey(1)
		if keys[pygame.K_n]:
			pathbool = False
		if keys[pygame.K_y]:
			pathbool = True
		if keys[pygame.K_p]:
			print(player.points)

		win.blit(image,(0,0))
		mushrooms.display(win)
		mushrooms.update(player)
		player.display(win)
		enemy.display(win)
		enemy.run()

		if enemy.catchPlayer():
			run = False
			winbool = False

		elif player.points == 113:
			run = False
			winbool = True

		pygame.display.update()

	if winbool == False:
		loseMenu(win,player)
	elif winbool == True:
		winMenu(win,player)


def mainMenu(win):
	playbutton = Button("     Play     ",32,(0,255,0), (0,0,255), (300,250))
	helpbutton = Button("     Help     ",32,(0,255,0), (0,0,255), (300,300))
	quitbutton = Button("     Quit     ",32,(0,255,0), (0,0,255), (300,350))

	run = True
	while run:
		win.fill((0,0,0))
		playbutton.display(win)
		helpbutton.display(win)
		quitbutton.display(win)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if playbutton.onClick():
					gamePlay(win)
				if helpbutton.onClick():
					print("help in progress!")
				if quitbutton.onClick():
					run = False

		pygame.display.update()



pygame.init()
display = (600,600)

win = pygame.display.set_mode(display)
pygame.display.set_caption("PAC-MAN")
mainMenu(win)
