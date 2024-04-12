from collections import defaultdict
import heapq

n,k = map(int, input().split())

nums = list(map(int, input().split()))
dx,dy = [-1,1,0,0],[0,0,-1,1]
def put():
    num = min(nums)
    for i in range(n):
        if nums[i] == num:
            nums[i] += 1


def roll():
    global nums
    temp = [[nums[0]], nums[1:]]
    width = len(temp[0])
    height = len(temp)
    while width + height <= len(temp[-1]):
        temp = cut(width, height,temp)
        width = len(temp[0])
        height = len(temp)
    nums = temp
def cut(width,height,temp):
    new_temp = []
    for i in range(height):
        new_temp.append(temp[i][:width])
    new_temp = list(map(list, zip(*new_temp[::-1])))
    return [*new_temp, temp[-1][width:]]

def push():
    global nums
    cnt = [[0] * len(nums[i]) for i in range(len(nums))]
    for i in range(len(nums)):
        for j in range(len(nums[i])):
            for idx in range(4):
                nx,ny = i + dx[idx], j + dy[idx]
                if 0 <= nx < len(nums) and 0 <= ny < len(nums[nx]):
                    diff = (nums[i][j] - nums[nx][ny]) // 5
                    if diff > 0:
                        cnt[i][j] -= diff
                        cnt[nx][ny] += diff

    for i in range(len(nums)):
        for j in range(len(nums[i])):
            nums[i][j] += cnt[i][j]
    return

def spread():
    global nums
    new_nums = []
    for j in range(len(nums[-1])):
        for i in range(len(nums) -1, -1, -1):
            if 0 <= j < len(nums[i]):
                new_nums.append(nums[i][j])
    nums = new_nums

def fold_twice():
    global nums
    temp = fold(nums)
    left,right = fold(temp[0]), fold(temp[1])
    new_nums = [right[0], *left, right[1]]
    nums = new_nums

def fold(temp):
    return [temp[:len(temp)//2][::-1], temp[len(temp)//2:]]

def check():
    if max(nums) - min(nums) <= k:
        return True
    return False

def simulation():
    put()
    roll()
    push()
    spread()
    fold_twice()
    push()
    spread()

answer = 1
while True:
    simulation()
    if check(): break
    answer += 1

print(answer)