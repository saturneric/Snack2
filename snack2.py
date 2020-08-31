import os
import time
import random as rand
import msvcrt
import time

os.system("color 17")
os.system("title '玩蛇'")

s_x = 50
s_y = 30
foods = []
ifmpy = 1
players = []
playctl = [["w","a","d","s"],["i","j","l","k"]]
s_playtime = time.clock()


def get_food(s_x,s_y,players,foods):
	m_food = {}
	ifcorrect = 0;
	fx = int(rand.random()*100%(s_x-2) + 1)
	fy = int(rand.random()*100%(s_x-2) + 1)
	while ifcorrect == 0:
		ifcorrect = 1;
		fx = int(rand.random()*100%(s_x-2) + 1)
		fy = int(rand.random()*100%(s_y-2) + 1)
		for player in players:
			if player[0]['x'] == fx and player[0]['y'] == fy:
				ifcorrect = 0
				continue
			for item in player[1]:
				if item['x'] == fx and item['y'] == fy:
					ifcorrect = 0
					continue
			for food in foods:
				if fx == food['x'] and fy == food['y']:
					ifcorrect = 0
					continue
	m_food['x'] = fx
	m_food['y'] = fy
	return m_food

def build_screen(s_x,s_y,heads,snacks,plyhead,plysnack,foods):
	screen = []
	for y in range(s_y):
		screen.append("")
		for x in range(s_x):
			ifblank = 1
			if x == 0 or x == s_x-1:
				screen[y] += '#'
				ifblank = 0
			elif y == 0 or y == s_y-1:
				screen[y] += '#'
				ifblank = 0
			hdnum = 0
			for head in heads:
				if y == head['y'] and x == head['x']:
					screen[y] += plyhead[hdnum]
					ifblank = 0
				hdnum += 1
			snnum = 0
			for snack in snacks:
				for item in snack:
					if x == item['x'] and y == item['y']:
						if ifblank != 0:
							screen[y]+=plysnack[snnum]
							ifblank = 0
				snnum += 1
			for food in foods:
				if ifblank != 0:
					if food['x'] == x and food['y'] == y:
						screen[y]+='o'
						ifblank = 0
			if ifblank == 1:
			 screen[y] += '.'
	return screen
def flash_screen(screen):	
	for line in screen:
		print(line)

def if_eat_food(head,m_foods):
	del_foods = []
	ifeat = 0
	for food in m_foods:
		if head['dir'] == 0 and head['y'] -1 == food['y'] and head['x'] == food['x']:
			m_foods.remove(food)
			del_foods.append(food)
			ifeat = 1
		if head['dir'] == -1 and head['x'] +1 == food['x'] and head['y'] == food['y']:
			m_foods.remove(food)
			del_foods.append(food)
			ifeat = 1
		if head['dir'] == 1 and head['x'] -1 == food['x'] and head['y'] == food['y']:
			m_foods.remove(food)
			del_foods.append(food)
			ifeat = 1
		if head['dir'] == -2 and head['y'] +1 == food['y'] and head['x'] == food['x']:
			m_foods.remove(food)
			del_foods.append(food)
			ifeat = 1
			
		if head['y'] == food['y'] and head['x'] == food['x']:
			m_foods.remove(food)
			del_foods.append(food)
			ifeat = 1
	return [ifeat,del_foods]
	
def recover_snack(t_player,players):
	ifcorrect = 0
	fx = int(rand.random()*100%(s_x-2) + 1)
	fy = int(rand.random()*100%(s_x-2) + 1)
	while ifcorrect == 0:
		ifcorrect = 1;
		fx = int(rand.random()*100%(s_x-2) + 1)
		fy = int(rand.random()*100%(s_y-2) + 1)
		for player in players:
			if player != t_player:
				if player[0]['x'] == fx and fy - 1 == player[0]['y']:
					ifcorrect = 0
					continue
				if player[0]['x'] == fx and player[0]['y'] == fy:
					ifcorrect = 0
					continue
				for item in player[1]:
					if item['x'] == fx and item['y'] == fy:
						ifcorrect = 0
						continue
					if item['x'] == fx and item['y'] == fy - 1:
						ifcorrect = 0
						continue
				for food in foods:
					if player[0]['x'] == fx and fy-1 == food['y']:
						ifcorrect = 0
						continue
					if fx == food['x'] and fy == food['y']:
						ifcorrect = 0
						continue
	t_player[0] = {}
	t_player[0]['x'] = fx
	t_player[0]['y'] = fy
	t_player[0]['dir'] = 0
	t_player[1] = []
	
	t_player[2] = "ALIVE"
	for x in range(2):
		t_player[1].append({'x':fx,'y':fy+x})
	players.append(t_player)

def if_eat_snack(t_player,players):
	head = t_player[0]
	for m_player in players:
		if m_player != t_player:
			for item in m_player[1]:
				if head['y'] == item['y'] and head['x'] == item['x']:
					return 1
	 
def if_eat_it(head,snack):
	for item in snack:
		if head['dir'] == 0 and head['y'] -1 == item['y'] and head['x'] == item['x']:
			return 1
		elif head['dir'] == -1 and head['x'] +1 == item['x'] and head['y'] == item['y']:
			return 1
		elif head['dir'] == 1 and head['x'] -1 == item['x'] and head['y'] == item['y']:
			return 1
		elif head['dir'] == -2 and head['y'] +1 == item['y'] and head['x'] == item['x']:
			return 1
		else:
			pass
			
def if_out(head,s_x,s_y):
	ifout = 0
	if head['dir'] == 0 and head['y'] <= 1:
		head['y'] = s_y-2
		ifout = 1
	elif head['dir'] == -1 and head['x'] +2 >= s_x:
		head['x'] = 1
		ifout = 1
	elif head['dir'] == 1 and head['x'] <= 1:
		head['x'] = s_x-2
		ifout = 1
	elif head['dir'] == -2 and head['y'] +2 >= s_y:
		head['y'] = 1
		ifout = 1
	else:
		pass
	return ifout
def eat_food(head,snack,food):
	snack.insert(0,{'x':head['x'],'y':head['y']})
	head['x'] = food['x']
	head['y'] = food['y']
		
def move(head,snack,speed):
	lsnk = len(snack)
	for num in range(len(snack)):
		d_num = lsnk - num - 1
		if d_num == 0:
			snack[d_num]['x'] = head['x']
			snack[d_num]['y'] = head['y']
		else:
			snack[d_num]['x'] = snack[d_num-1]['x']
			snack[d_num]['y'] = snack[d_num-1]['y']
	if head['dir'] == 0:
		head['y'] -= speed
	elif head['dir'] == -1:
		head['x'] += speed
	elif head['dir'] == 1:
		head['x'] -= speed
	elif head['dir'] == -2:
		head['y'] += speed
	else:
		pass

def get_crl(heads,ctls):
	doctl = []
	line = ""
	if msvcrt.kbhit()!=0:
		lnnum = 0
		if msvcrt.kbhit()!=0:
			line = msvcrt.getch()
		try:
			line = str(line, encoding = "utf-8")
		except UnicodeDecodeError:
			pass
			
	ispeed = 1
	num = 0
	for ctl in ctls:
		head = heads[num]
		if line == ctl[0]:
			if head['dir'] != -2:
				if head['dir'] == 0 and ifmpy == 0:
					ispeed = 2
				head['dir'] = 0
		elif line == ctl[1]:
			if head['dir'] != -1:
				if head['dir'] == 1 and ifmpy == 0:
					ispeed = 2
				head['dir'] = 1
		elif line == ctl[2]:
			if head['dir'] != 1:
				if head['dir'] == -1 and ifmpy == 0:
					ispeed = 2
				head['dir'] = -1
		elif line == ctl[3]:
			if head['dir'] != 0:
				if head['dir'] == -2 and ifmpy == 0:
					ispeed = 2
				head['dir'] = -2
		else:
			pass
		num += 1
	if line == "r":
		s_playtime = time.clock()
		doctl.append("STPT")
	return doctl

fsnack = []
fhead = []

ssnack = []
shead = []

fplayer = []
fhead = {'x':10,'y':10,'dir':0}
fsnack.append({'x':10,'y':11})
fsnack.append({'x':10,'y':12})

fplayer.append(fhead) #0
fplayer.append(fsnack) #1
fplayer.append("ALIVE") #2
fplayer.append("Player1") #3
fplayer.append(["w","a","d","s"]) #4
fplayer.append("@") #5
fplayer.append("&") #6

splayer = []
shead = {'x':5,'y':5,'dir':0}
ssnack.append({'x':5,'y':6})
ssnack.append({'x':5,'y':7})
splayer.append(shead) #0
splayer.append(ssnack) #1
splayer.append("ALIVE") #2
splayer.append("Player2") #3
splayer.append(["i","j","l","k"]) #4
splayer.append("@") #5

tsnack = []
thead = []

tplayer = []
thead = {'x':15,'y':15,'dir':0}
tsnack.append({'x':15,'y':16})
tsnack.append({'x':15,'y':17})
tplayer.append(thead) #0
tplayer.append(tsnack) #1
tplayer.append("ALIVE") #2
tplayer.append("Player3") #3
tplayer.append(["8","4","6","5"]) #4
tplayer.append("@") #5
tplayer.append("%") #6

splayer.append("$") #6

players.append(fplayer)
players.append(splayer)
#players.append(tplayer)

for x in range(100):
	foods.append(get_food(s_x,s_y,players,foods))

plyhed = []
plysnk = []
plyctl = []
plyhead = []
plysnack = []

fp = open("snack.log","a")
fp.write("New Game\n")
fp.write("s_x: "+str(s_x)+" s_y: "+str(s_y)+" ifmpy: "+str(ifmpy)+"\n")
fp.write("food:"+str(foods)+"\n")
fp.close()

ifinit = 0

time.clock()

while True:
	jif_eat_food = 0
	fp = open("snack.log","w")
	flash_t = 0.05
	start = time.clock()
	gdoctl = get_crl(plyhed,plyctl)	
	for item in gdoctl:
		if item == "STPT":
			s_playtime = time.clock()
	if ifinit == 0:
		ifinit = 1
		plyhed = []
		plysnk = []
		plyctl = []
		plyhead = []
		plysnack = []
		for player in players:
			if player[2] != "DEAD":
				plyhed.append(player[0])
				plysnk.append(player[1])
				plyctl.append(player[4])
				plyhead.append(player[5])
				plysnack.append(player[6])
	
	for player in players:
		jif_eat_food = 0
		if player[2] == "DEAD":
			continue
		
		speed = 1
		head = player[0]
		snack = player[1]
		if if_out(head,s_x,s_y) == 1:
			jif_eat_food = 1
			
		if if_eat_it(head,snack) == 1:
			player[2] = "DEAD"
			fp.write(str(player[3])+" Dead:Eat it\n")
			ifinit = 0
			for item in player[1]:
				foods.append({'x':item['x'],'y':item['y']})
			players.remove(player)
			recover_snack(player,players)
		
		if if_eat_snack(player,players) == 1:
			player[2] = "DEAD"
			fp.write(str(player[3])+" Dead:Eat Snack\n")
			ifinit = 0
			for item in player[1]:
				foods.append({'x':item['x'],'y':item['y']})
			player[1] = []
			player[0] = {}
			players.remove(player)
			recover_snack(player,players)
			
		frtn = if_eat_food(head,foods)
		if frtn[0] == 1:
			jif_eat_food = 1
			fp.write(str(player[3])+" Eating Foods:\n")
			fp.write("Head: "+str(head)+"\n")
			for f_item in frtn[1]:
				fp.write(" Eat Food:"+str(f_item)+"\n")
				fp.write("Eat Foods End Total: "+str(len(frtn[1]))+"\n")
				eat_food(head,snack,f_item)
				#foods.remove(f_item)
				if len(foods) < 10:
					foods.append(get_food(s_x,s_y,players,foods))
		
		if jif_eat_food == 0:	
			move(head,snack,1)
		
		fp.write("Foods: "+str(foods)+"\n")
		fp.write(str(player[3])+" Head:"+str(player[0])+"\n")
		fp.write(str(player[3])+" Snack:"+str(player[1])+"\n")
		
		if speed == 2:
			move(head,snack,1)
			if_out(head,s_x,s_y)
			if if_eat_it(head,snack) == 1:
				player[2] = "DEAD"
			if if_eat_food(head,foods) == 1:
				eat_food(head,snack)
				food = get_food(s_x,s_y,players,foods)
			screen = build_screen(s_x,s_y,plyhed,plysnk)
			flash_screen(screen)
			move(head,snack,1)
			flash_t = 0.08
			
	screen = build_screen(s_x,s_y,plyhed,plysnk,plyhead,plysnack,foods)
	for line in screen:
		fp.write(line+"\n")
		
	end = time.clock()
	
	if end-start < flash_t:
		time.sleep(flash_t+start-end)
	os.system("cls")
	fstart = time.clock()
	flash_screen(screen)
	maxlen = 0
	maxplayer = []
	for player in players:
		if len(player[1]) > maxlen:
			maxplayer = player
			maxlen = len(player[1])
	print("################")
	print("(No1)",maxplayer[3]+": ")
	#print("Status:",maxplayer[2])
	print("Score(s):",len(maxplayer[1])+1)
	print("################")
	ifshow = 0
	for player in players:
		if player != maxplayer and ifshow == 0:
			print(player[3]+": ")
			#print("Status:",player[2])
			print("Score(s):",len(player[1])+1)
			ifshow = 1
		
	fend = time.clock()
	print("########################")
	n_playtime = time.clock()
	timer = 180-int(n_playtime-s_playtime)
	print("Timer:",timer,"s")
	print("Real Flash Hz",1/(fend-start))
	fp.close()
	if timer <= 0:
		print("########################")
		print(maxplayer[3],"Win!")
		break;
input()
