import requests
import sys
def play_game():
	base_url = 'http://ec2-34-212-54-152.us-west-2.compute.amazonaws.com/'
	token = requests.post(base_url+'session', data={'uid':'005099109'})
	token = token.json()['token']
	info = requests.get(base_url+'game?token='+token)
	info = info.json()
	print(info)
	rows=info['size'][0]
	cols=info['size'][1]
	maze = [ [ '.' for i in range(cols) ] for j in range(rows) ]
	cur_X = info['cur_loc'][0]
	cur_Y = info['cur_loc'][1]

	dirs = ['up', 'right', 'down', 'left']
	dy = [0, 1, 0, -1]
	dx = [-1, 0, 1, 0]
	def printMaze(loc):
		for j in range(cols):
			for i in range(rows):
				if i == loc[0] and j == loc[1]:
					sys.stdout.write('P')
				else:
					sys.stdout.write(maze[i][j])
			print()
		print("\n\n")

	def dfs(loc): 
		maze[loc[0]][loc[1]] = 'v'
		
		for i in range(4):
			res = requests.post(base_url+'game?token='+token, data={'action':dirs[i]})
			res = res.json()['result']
			#print("{}, {}, {}".format(loc[0] + dy[i], loc[1] + dx[i], res, dirs[i]))
			if res == 'INVALID':
				break;
			elif res == -2 or res == -1:
				if loc[0] + dy[i] >= 0 and loc[0] + dy[i] < rows and loc[1] + dx[i] >= 0 and loc[1] + dx[i] < cols:
					maze[loc[0] + dy[i]][loc[1] + dx[i]] = 'X'
			elif res == 0:
				if loc[0] + dy[i] >= 0 and loc[0] + dy[i] < rows and loc[1] + dx[i] >= 0 and loc[1] + dx[i] < cols:
					if maze[loc[0] + dy[i]][loc[1] + dx[i]] == '.':
						if dfs([loc[0] + dy[i], loc[1] + dx[i]]):
							return True
				res = requests.post(base_url+'game?token='+token, data={'action':dirs[(i+2)%4]})
			else:
				# reset everything
				print("Found!")
				return True
			#printMaze(loc)
		return False

	print(dfs([cur_X, cur_Y]))

	info = requests.get(base_url+'game?token='+token)
	info = info.json()
	print(info['levels_completed'])
for i in range(5):
	play_game()
