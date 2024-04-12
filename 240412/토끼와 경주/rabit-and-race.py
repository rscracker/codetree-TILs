from collections import defaultdict
import heapq

Q = int(input())

points = defaultdict(int)
point_total = 0
distances = defaultdict(int)
infos = defaultdict(list)
rabbits = []
positions = []
n,m,p = -1,-1,-1
dx,dy = [-1,1,0,0],[0,0,-1,1]


def change_pos():
    global point_total
    rabbit = heapq.heappop(rabbits)
    jump, sum_pos, x, y, pid = rabbit
    pos = (-1,-1,-1,-1)
    for i in range(4):
        distance = distances[pid]
        if i <= 1:
            distance %= (2 * n - 2)
            nx, ny = find_pos(x,y,distance,i)
            if (nx+ny, nx, ny, pid) > pos:
                pos = (nx+ny, nx, ny, pid)
        else:
            distance %= (2 * m - 2)
            nx, ny = find_pos(x, y, distance, i)
            if (nx+ny, nx, ny, pid) > pos:
                pos = (nx+ny, nx, ny, pid)

    infos[pid] = [pos[1],pos[2],jump+1]
    heapq.heappush(rabbits, (jump+1, pos[0], pos[1], pos[2], pid))
    heapq.heappush(positions, (-pos[0],-pos[1],-pos[2],-pid, jump+1))
    # 포인트 추가
    point_total += pos[0] + 2
    points[pid] -= pos[0] + 2

def find_pos(x,y,distance, dir):
    while distance > 0:
        nx,ny = x+dx[dir], y+dy[dir]
        if 0 > nx or nx >= n or 0 > ny or ny >= m:
            dir = change_dir(dir)
        max_d = get_max_distance(x,y,dir)
        move = min(distance, max_d)
        distance -= move
        x += dx[dir] * move
        y += dy[dir] * move
    return (x,y)
def get_max_distance(x,y,dir):
    if dir == 0:
        return x
    elif dir == 1:
        return n - x - 1
    elif dir == 2:
        return y
    else:
        return m - y - 1

def change_dir(dir):
    if dir == 0:
        return 1
    elif dir == 1:
        return 0
    elif dir == 2:
        return 3
    else:
        return 2

def find_highest(s):
    sum_pos, x ,y, pid, jump = heapq.heappop(positions)
    while infos[-pid] != [-x,-y,jump]:
        sum_pos, x, y, pid, jump = heapq.heappop(positions)
    points[-pid] += s
    heapq.heappush(positions, (sum_pos, x ,y, pid, jump))

def highest_score():
    cnt = -1
    for pid in points.keys():
        score = point_total + points[pid]
        if score > cnt:
            cnt = score
    print(cnt)

for _ in range(Q):
    temp = list(map(int, input().split()))
    inst = temp[0]
    if inst == 100:
        n,m,p = temp[1:4]
        l = temp[4:]
        for i in range(p):
            pid = l[2*i]
            d = l[2*i+1]
            distances[pid] = d
            infos[pid] = [0,0,0]
            heapq.heappush(rabbits, (0, 0, 0, 0,pid))
    elif inst == 200:
        K,S = temp[1], temp[2]
        for _ in range(K):
            change_pos()
        find_highest(S)
    elif inst == 300:
        pid_t, L = temp[1], temp[2]
        distances[pid_t] *= L
    elif inst == 400:
        highest_score()