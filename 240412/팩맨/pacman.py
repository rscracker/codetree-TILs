import sys
from collections import deque, defaultdict, Counter
from itertools import product,combinations
import bisect,math,heapq

m,t = map(int, input().split())
n = 4
p_x,p_y = map(int, input().split())
p_x -= 1
p_y -= 1

monsters = [[[0] * 8 for _ in range(4)] for _ in range(4)]
eggs = deque()
dead = [[deque() for _ in range(n)] for _ in range(n)]

dx,dy = [-1,-1,0,1,1,1,0,-1],[0,-1,-1,-1,0,1,1,1]
pdx,pdy = [-1,0,1,0],[0,-1,0,1]

for _ in range(m):
    x,y,d = map(int, input().split())
    monsters[x-1][y-1][d-1] += 1

def copy_monster():
    for i in range(n):
        for j in range(n):
            for d in range(8):
                monster_cnt = monsters[i][j][d]
                eggs.append((i,j,d,monster_cnt))


def check_dead(x,y,round):
    if not dead[x][y]: return False
    for i in dead[x][y]:
        if i > round:
            return True
    return False
    
def move_monsters(round):
    global monsters
    new_monsters = [[[0] * 8 for _ in range(4)] for _ in range(4)]
    for x in range(n):
        for y in range(n):
            for d in range(8):
                if not monsters[x][y][d]: continue
                dir = d
                nx,ny = x + dx[dir], y + dy[dir]
                check = 0
                while 0 > nx or nx >= n or 0 > ny or ny >= n or (nx,ny) == (p_x,p_y) or check_dead(nx,ny,round):
                    dir += 1
                    dir %= 8
                    nx  = x + dx[dir]
                    ny = y + dy[dir]
                    check += 1
                    if check == 8:
                        break
                if check == 8:
                    new_monsters[x][y][d] = monsters[x][y][d]
                else:
                    new_monsters[nx][ny][dir] = monsters[x][y][d]
    monsters = new_monsters

def move_pack(round):
    global p_x, p_y
    eat = 0
    move = []
    for start in range(4):
        nx1,ny1 = p_x + pdx[start], p_y + pdy[start]
        if 0 > nx1 or nx1 >= n or 0 > ny1 or ny1 >= n: continue
        for mid in range(4):
            nx2,ny2 = nx1 + pdx[mid], ny1 + pdy[mid]
            if 0 > nx2 or nx2 >= n or 0 > ny2 or ny2 >= n: continue
            for end in range(4):
                nx3,ny3 = nx2 + pdx[end], ny2 + pdy[end]
                if 0 > nx3 or nx3 >= n or 0 > ny3 or ny3 >= n: continue
                cnt = 0
                visited = set([(nx1,ny1), (nx2,ny2), (nx3,ny3)])
                for i in range(8):
                    for visit in visited:
                        cnt += monsters[visit[0]][visit[1]][i]
                if cnt > eat:
                    move = [(nx1,ny1), (nx2,ny2), (nx3, ny3)]
                    eat = cnt
    p_x,p_y = move[2]
    for x,y in move:
        if any(monsters[x][y][i] for i in range(8)):
            dead[x][y].append((round + 2))
            monsters[x][y] = [0] * 8
        

def copy_complete():
    while eggs:
        x,y,d,cnt = eggs.popleft()
        monsters[x][y][d] += cnt

def count_monsters():
    answer = 0
    for i in range(n):
        for j in range(n):
            for d in range(8):
                answer += monsters[i][j][d]
    return answer

for round in range(t):
    copy_monster()
    move_monsters(round)
    move_pack(round)
    copy_complete()

print(count_monsters())