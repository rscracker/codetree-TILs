from collections import defaultdict, deque
import heapq

rdx,rdy = [-1,-1,-1,0,0,1,1,1],[-1,0,1,-1,1,-1,0,1]
sdx,sdy = [-1,0,1,0],[0,1,0,-1]

N,M,P,C,D = map(int ,input().split())

points = [0] * (P+1)
stop = [0] * (P+1)
positions = [[-1,-1] for _ in range(P+1)]
board = [[0] * (N) for _ in range(N)]

r,c = map(int, input().split())
r -= 1
c -= 1

for _ in range(P):
    p,sr,sc = map(int, input().split())
    board[sr-1][sc-1] = p
    positions[p] = [sr-1, sc-1]

def calDistance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return (x2-x1)**2+(y2-y1)**2

def findSanta():
    santa = (float('inf'), N + 1, N + 1)
    santa_idx = -1
    for i in range(1,P+1):
        if positions[i] == [-1,-1]: continue
        d = calDistance(positions[i],(r,c))
        if (d, -positions[i][0], -positions[i][1]) < santa:
            santa = (d, -positions[i][0], -positions[i][1])
            santa_idx = i
    return santa_idx

def move_r():
    global r,c
    distance = float('inf')
    santa_idx = findSanta()
    sx,sy = positions[santa_idx]
    x,y,dir = (0,0,0)
    for i in range(8):
        nx,ny = r + rdx[i], c + rdy[i]
        if 0 <= nx < N and 0 <= ny < N:
            d = calDistance((nx,ny), (sx,sy))
            if d < distance:
                distance = d
                x,y,dir = nx,ny,i
    if board[x][y]:
        collision(0, santa_idx, rdx[dir], rdy[dir])
    r,c = x,y

def moveSantas():
    for i in range(1,P+1):
        if stop[i] or positions[i] == [-1,-1]: continue
        moveSanta(i)


def moveSanta(idx):
    santa = positions[idx]
    distance = calDistance(santa, (r,c))
    move_x,move_y = -1,-1
    x,y = santa
    dir = 0
    for i in range(4):
        nx,ny = x + sdx[i], y + sdy[i]
        if 0 <= nx < N and 0 <= ny < N:
            if board[nx][ny] > 0: continue
            d = calDistance((nx,ny), (r,c))
            if d < distance:
                distance = d
                move_x,move_y = nx,ny
                dir = i
    if move_x == -1 and move_y == -1:
        return
    board[x][y] = 0
    board[move_x][move_y] = idx
    positions[idx] = [move_x, move_y]
    if move_x == r and move_y == c:
        collision(1,idx, -sdx[dir], -sdy[dir])


def collision(type, santa_idx, nx, ny):
    if type == 0:
        points[santa_idx] += C
        collisionSanta(nx,ny,C,santa_idx)
    elif type == 1:
        points[santa_idx] += D
        collisionSanta(nx,ny,D,santa_idx)

def collisionSanta(nx,ny,k,santa_idx):
    x, y = positions[santa_idx]
    sx = x + k * nx
    sy = y + k * ny
    if 0 > sx or sx >= N or 0 > sy or sy >= N:
        board[x][y] = 0
        positions[santa_idx] = [-1,-1]
    else:
        board[x][y] = 0
        stop[santa_idx] = 2
        inter(sx,sy,nx,ny,santa_idx)

def inter(x,y,nx,ny,santa_idx):
    if 0 > x or x >= N or 0 > y or y >= N:
        positions[santa_idx] = [-1,-1]
        return

    if not board[x][y]:
        board[x][y] = santa_idx
        positions[santa_idx] = [x,y]
    else:
        inter(x + nx, y + ny, nx, ny, board[x][y])
        board[x][y] = santa_idx
        positions[santa_idx] = [x, y]

def remove_break():
    for i in range(1,P+1):
        if stop[i] > 0:
            stop[i] -= 1

def end_game():
    cnt = 0
    for i in range(1,P+1):
        if positions[i] != [-1,-1]:
            points[i] += 1
            cnt += 1
    return cnt == 0

for _ in range(M):
    remove_break()
    move_r()
    moveSantas()
    if end_game():
        break


print(*points[1:])