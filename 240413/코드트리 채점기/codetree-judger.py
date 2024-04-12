import sys
from collections import deque, defaultdict, Counter
from itertools import product,combinations
import bisect,math,heapq

Q = int(input())
N = 0
waiting_queue = defaultdict(list)
waiting_urls = defaultdict(list)
logs = defaultdict(tuple)
checking = defaultdict(int)
checker = defaultdict(str)
answer = 1

def request(t,p,u):
    global answer
    domain,id = u.split('/')
    if id in waiting_urls[domain]: return
    heapq.heappush(waiting_queue[domain], (p,t,u))
    answer += 1
    waiting_urls[domain].append(id)
    return


def try_check(t):
    temp = []
    for domain in list(waiting_queue.keys()):
        if not waiting_queue[domain]: continue
        if isChecking(domain) and checkTime(domain, t):
            heapq.heappush(temp, waiting_queue[domain][0])
    if not temp: return
    task = heapq.heappop(temp)
    start_check(t, task)
    return


def isChecking(domain):
    if checking[domain]: return False
    return True

def checkTime(domain, t): 
    if not logs[domain]: return True
    start, gap = logs[domain]
    if t < start + 3 * gap: return False
    return True
    
def start_check(t, task):
    global answer
    priority, time, url = task
    domain, id = url.split('/')
    for i in range(1, N + 1):
        if not checker[i]:
            checker[i] = domain
            checking[domain] = t
            heapq.heappop(waiting_queue[domain])
            waiting_urls[domain].remove(id)
            answer -= 1
            return

def finish(t, J_id):
    if not checker[J_id]: return
    domain = checker[J_id] 
    start = checking[domain]
    logs[domain] = (start, t - start)
    checker[J_id] = ''
    checking.pop(domain)
    return

for _ in range(Q):
    temp = list(input().split())
    inst = int(temp[0])
    if inst == 100:
        N,u0 = temp[1:]
        domain,id = u0.split('/')
        N = int(N)
        heapq.heappush(waiting_queue[domain], (1,0,u0))
        waiting_urls[domain].append(id)

    elif inst == 200:
        t,p,u = temp[1:]
        t,p = int(t), int(p)
        request(t,p,u)
        
    elif inst == 300:
        t = int(temp[1])
        try_check(t)
        
    elif inst == 400:
        t, J_id = map(int, temp[1:])
        finish(t, J_id)
    
    elif inst == 500:
        print(answer)