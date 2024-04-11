import sys

from collections import defaultdict
Q = int(input().rstrip())
n,m,p = 0,0,0
distances = []
pids = []
positions = []
jumps = []
points = []
dx,dy = [-1,1,0,0],[0,0,-1,1]
def ready(temp):
    global distances,pids,positions,jumps,points
    global n,m,p
    n,m,p = temp[:3]
    positions = [[0,0] for _ in range(p)]
    infos = temp[3:]
    distances = [0] * p
    points = [0] * p
    pids = [0] * p
    jumps = [0] * p
    for i in range(0,p):
        pids[i] = infos[2*i]
        distances[i] = infos[2*i+1]


def race(k,s):
    for _ in range(k):
        pick()
    last_pick(s)

def pick():
    rabbit = (float('inf'), float('inf'), float('inf'), float('inf'),float('inf'))
    rabbit_idx = -1
    for i in range(p):
        jump = jumps[i]
        pos = positions[i]
        pid = pids[i]
        me = (jump, sum(pos), pos[0], pos[1], pid)
        if me < rabbit:
            rabbit = me
            rabbit_idx = i
    jumps[rabbit_idx] += 1
    new_pos = (-1,-1,-1)
    x,y = rabbit[2], rabbit[3]
    d = distances[rabbit_idx]
    for i in range(4):
        nx,ny = move(x,y,d,i)
        if new_pos < (nx+ny, nx,ny):
            new_pos = (nx+ny,nx,ny)
    positions[rabbit_idx] = (new_pos[1], new_pos[2])
    for i in range(p):
        if i == rabbit_idx: continue
        points[i] += (new_pos[0] + 2)

def move(x,y,length,dir):
    if dir <= 1:
        length %= (2 * n - 2)
    else:
        length %= (2 * m - 2)

    while length > 0:
        distance = 0
        if dir == 0:
            distance = x
        elif dir == 1:
            distance = n - x - 1
        elif dir == 2:
            distance = y
        elif dir == 3:
            distance = m - y - 1
        x += dx[dir] * min(length, distance)
        y += dy[dir] * min(length, distance)
        length -= min(length, distance)
        if length > 0:
            dir = change_dir(dir)
        else:
            break
    return x,y
def change_dir(dir):
    if dir == 0:
        return 1
    if dir == 1:
        return 0
    if dir == 2:
        return 3
    if dir == 3:
        return 2
def last_pick(s):
    rabbit = (-1,-1,-1,-1)
    rabbit_idx = -1
    for i in range(p):
        if jumps[i] == 0: continue
        me = (sum(positions[i]), positions[i][0], positions[i][1], pids[i])
        if me > rabbit:
            rabbit = me
            rabbit_idx = i
    points[rabbit_idx] += s

def answer():
    cnt = 0
    for i in range(p):
        if points[i] > cnt:
            cnt = points[i]
    print(cnt)
def change_distance(pid, L):
    for i in range(p):
        if pids[i] == pid:
            distances[i] *= L
            break
def simulation():
    for _ in range(Q):
        temp = list(map(int, input().split()))
        inst = temp[0]
        if inst == 100:
            ready(temp[1:])
        if inst == 200:
            k,s = temp[1], temp[2]
            race(k,s)
        if inst == 300:
            pid_t,L = temp[1], temp[2]
            change_distance(pid_t,L)
        if inst == 400:
            answer()

simulation()