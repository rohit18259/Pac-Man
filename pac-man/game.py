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

	def setGraph(self,graph):
		self.graph = graph

	def display(self,win):
		pygame.draw.circle(win,(255,255,0),self.position,17)

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
			self.position = pos1


pygame.init()

image = pygame.image.load("maze1.png")

display = (600,600)

win = pygame.display.set_mode(display)
pygame.display.set_caption("PAC-MAN")

#graph = Graph(vertices=[[100,400],[300,400],[300,250],[450,250],[450,400]],edges=[[0,1],[1,2],[1,4],[2,3],[3,4]])
#player = Player([100,400])

graph = Graph(vertices=[[20,300],[60,300],[60,220],[100,220],[140,220],[140,300],[140,380],[100,380],[60,380],[100,460],[140,460],[140,500],[140,540],[60,540],[60,460],[100,140],[60,140],[60,60],[140,60],[140,100],[140,140],[220,140],[220,100],[220,60],[300,60],[380,60],[380,100],[380,140],[300,140],[460,100],[460,60],[540,60],[540,140],[500,140],[460,140],[500,220],[540,220],[540,300],[540,380],[500,380],[460,380],[460,300],[460,220],[500,460],[540,460],[540,540],[460,540],[460,500],[460,460],[380,500],[380,540],[300,540],[220,540],[220,500],[220,460],[300,460],[380,460],[220,380],[220,300],[220,220],[300,220],[380,220],[380,300],[380,380],[300,380],[300,300],[300,20],[580,300],[300,580]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,1],[7,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,9],[3,15],[15,16],[16,17],[17,18],[18,19],[19,20],[20,15],[19,22],[22,23],[23,24],[24,25],[25,26],[26,27],[27,28],[28,21],[21,22],[26,29],[29,30],[30,31],[31,32],[32,33],[33,34],[34,29],[33,35],[35,36],[36,37],[37,38],[38,39],[39,40],[40,41],[41,42],[42,35],[39,43],[43,44],[44,45],[45,46],[46,47],[47,48],[48,43],[47,49],[49,50],[50,51],[51,52],[52,53],[53,54],[54,55],[55,56],[56,49],[53,11],[28,60],[41,62],[55,64],[5,58],[59,60],[60,61],[61,62],[62,63],[63,64],[64,57],[57,58],[58,59],[58,65],[60,65],[62,65],[64,65],[24,66],[37,67],[51,68]])
player = Player([20,300])
player.setGraph(graph)

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
		d = dmap[self.curindex]
		for child in d[self.curindex]:
			if func(parent,child,pindex,d):
				self.nexindex = child
				self.boolfind = False
				self.curpos = self.graph.vertices[self.curindex].copy()
				self.nexpos = self.graph.vertices[self.nexindex].copy()
				break

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

enemy = Enemy(67,graph,player,dmap)

run = True
pathbool = False
while run:
	pygame.time.delay(5)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

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

	win.blit(image,(0,0))
	#graph.display(win)
	player.display(win)
	enemy.display(win)
	enemy.run()
	if pathbool:
		player.pathDisplay(win)
	pygame.display.update()

pygame.quit()