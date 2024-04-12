from collections import defaultdict
import heapq

L,N,Q = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(L)]

positions = [[0] * L for _ in range(L)]
knights = defaultdict(list)
dx,dy = [-1,0,1,0],[0,1,0,-1]
answer = 0
damages = [0] * (N + 1)

for i in range(N):
    r,c,h,w,k = map(int, input().split())
    for x in range(r,r+h):
        for y in range(c,c+w):
            positions[x-1][y-1] = i + 1
    knights[i+1] = [r-1,c-1,h,w,k]
def knight_move(init_idx, idx, dir):
    if not knights[idx]: return False
    r,c,h,w,k = knights[idx]
    for x in range(r, r + h):
        for y in range(c, c + w):
            nx,ny = x + dx[dir] , y + dy[dir]
            if 0 > nx or nx >= L or 0 > ny or ny >= L: return False
            if board[nx][ny] == 2: return False
            if positions[nx][ny] and positions[nx][ny] != idx:
                if not knight_move(init_idx, positions[nx][ny], dir):
                    return False
    nr, nc = r + dx[dir], c + dy[dir]
    knights[idx] = [nr, nc, h, w, k]
    if idx != init_idx:
        damage(idx)
    return True

def damage(idx):
    global answer
    r, c, h, w, k = knights[idx]
    cnt = 0
    for x in range(r, r+h):
        for y in range(c, c+w):
            if board[x][y] == 1:
                cnt += 1
    damages[idx] += min(k, cnt)
    k -= min(k, cnt)
    if k <= 0:
        knights.pop(idx)
    else:
        knights[idx][4] = k

def new_board():
    for key in knights.keys():
        r,c,h,w,k = knights[key]
        for x in range(r,r+h):
            for y in range(c,c+w):
                positions[x][y] = key

def answer():
    cnt = 0
    for key in knights.keys():
        cnt += damages[key]
    print(cnt)

for _ in range(Q):
    a,b = map(int, input().split())
    knight_move(a, a, b)
    new_board()

answer()