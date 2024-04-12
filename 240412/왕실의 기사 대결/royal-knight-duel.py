from collections import defaultdict, deque
import heapq

L,N,Q = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(L)]

positions = [[0] * L for _ in range(L)]
knights = defaultdict(list)
dx,dy = [-1,0,1,0],[0,1,0,-1]
answer = 0
damages = [0] * (N + 1)
moves = set()

for i in range(N):
    r,c,h,w,k = map(int, input().split())
    for x in range(r,r+h):
        for y in range(c,c+w):
            positions[x-1][y-1] = i + 1
    knights[i+1] = [r-1,c-1,h,w,k]
def knight_move(idx, dir):
    global moves
    if not knights[idx]: return False
    r,c,h,w,k = knights[idx]
    for x in range(r, r + h):
        for y in range(c, c + w):
            nx,ny = x + dx[dir] , y + dy[dir]
            if 0 > nx or nx >= L or 0 > ny or ny >= L: return False
            if board[nx][ny] == 2: return False
            if positions[nx][ny] and positions[nx][ny] != idx:
                if not knight_move(positions[nx][ny], dir):
                    return False
    moves.add((idx,r + dx[dir],c + dy[dir],h,w,k))
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
    global positions
    new = [[0] * L for _ in range(L)]
    for i in range(1, N+1):
        if not knights[i]: continue
        r,c,h,w,k = knights[i]
        for x in range(r,r+h):
            for y in range(c,c+w):
                new[x][y] = i
    positions = new

def check(init_idx):
    for move in moves:
        idx,r,c,h,w,k = move
        knights[idx] = [r,c,h,w,k]
        if idx != init_idx:
            damage(idx)

def answer():
    cnt = 0
    for i in range(1, N + 1):
        if knights[i]:
            cnt += damages[i]
    print(cnt)

for _ in range(Q):
    a,b = map(int, input().split())
    if knight_move(a, b):
        check(a)
        new_board()
    moves = set()

answer()