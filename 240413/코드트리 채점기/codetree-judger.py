from collections import defaultdict, deque
import heapq

Q = int(input())
N = -1

checker = defaultdict(str)
checking = defaultdict(int)
waiting_queue = []
waiting_urls = defaultdict(list)
logs = defaultdict(list)

def request(priority, time ,url):
    if waiting_urls[url]: return
    push_waiting(priority, time, url)

def push_waiting(priority, time, url):
    heapq.heappush(waiting_queue, (priority, time, url))
    waiting_urls[url] = [priority, time]

def try_checking(t):
    if not waiting_queue: return
    temp = deque()
    priority, time, url = heapq.heappop(waiting_queue)
    domain, id = url.split('/')
    while waiting_queue and not check_possible(t, domain):
        temp.append((priority, time, url))
        priority, time, url = heapq.heappop(waiting_queue)
    if check_possible(t, domain):
        for i in range(1, N + 1):
            if not checker[i]:
                waiting_urls.pop(url)
                checking[url] = t
                checker[i] = url
                break
    else:
        heapq.heappush(waiting_queue, (priority, time, url))
    while temp:
        task = temp.popleft()
        heapq.heappush(waiting_queue, task)


def check_possible(t, domain):
    if checking[domain]: return False
    if logs[domain]:
        start, gap = logs[domain]
        if t < start + 3 * gap: return False
    return True

def finish(J_id, t):
    if not checker[J_id]: return
    url = checker[J_id]
    domain, id = url.split('/')
    checker[J_id] = ''
    start = checking[url]
    logs[domain] = (start, t - start)
    checking.pop(url)



for _ in range(Q):
    temp = list(input().split())
    inst = int(temp[0])
    if inst == 100:
        N, u0 = int(temp[1]), temp[2]
        push_waiting(1,0,u0)
    if inst == 200:
        t,p = map(int, temp[1:-1])
        u = temp[-1]
        request(p,t,u)
    if inst == 300:
        t = int(temp[1])
        try_checking(t)
    if inst == 400:
        t,J_id = map(int, temp[1:])
        finish(J_id, t)
    if inst == 500:
        print(len(waiting_queue))