import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrackedArray():
    
   
    def __init__(self, self_arr):
        self.arr = np.copy(arr)
        self.reset()
    

    def reset(self):
        self.indices = []
        self.values = []      
        self.access_type = [] 
        self.full_copies = []
       
        
    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))
        
    def GetActivity(self, idx = None):
        if(isinstance(idx, type(None))):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indices[idx], self.access_type[idx])
        
            
    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)
        
    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")
            
    def __len__(self):
        return self.arr.__len__()



plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams["font.size"] = 16
FPS = 60.0



N = 50
arr = np.round(np.linspace(10,1000,N), 0)
np.random.seed(0)
np.random.shuffle(arr)
arr = TrackedArray(arr)


#############################################
# sorter = "Insertion"
# t0 = time.perf_counter()
# i = 1
# while(i < len(arr)):
#     j = i
#     while((j > 0) and (arr[j - 1] > arr[j])):
#         temp = arr[j - 1]
#         arr[j - 1] = arr[j]
#         arr[j] = temp
#         j -= 1
#     i+= 1
    
# dt = time.perf_counter() - t0

#############################################
sorter = "Quick"

def quicksort(low, high, A):
    if low < high:
        p = partition(low, high, A)
        quicksort(low, p - 1, A)
        quicksort(p + 1, high, A)
    
    
def partition(low, high, A):
    pivot = A[high]
    i = low
    for j in range(low, high):
        if(A[j] < pivot):
            temp = A[i]
            A[i] = A[j]
            A[j] = temp
            i += 1
    
    temp = A[i]
    A[i] = A[high]
    A[high] = temp
    return i

t0 = time.perf_counter()
quicksort(0, len(arr) - 1, arr)

dt = time.perf_counter() - t0
#############################################

print(f"---------- {sorter} Sort ----------")
print(f"Array sorted in {dt*1000: .2f} ms")

fig, ax = plt.subplots()
container = ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
ax.set_xlim([0, N])
ax.set(xlabel = "Index", ylabel = "Value", title = f"{sorter} Sort")
text = ax.text(0, 1000, "")

def update(frame):
    text.set_text(f"Accesses = {frame}")
    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("#1f77b4")
     
        
        
    idx, op = arr.GetActivity(frame)
    if op == "get":
        container.patches[idx].set_color("green")
    elif op == "set":
        container.patches[idx].set_color("red")
        
    return (*container, text)

animation = FuncAnimation(fig, update, frames = range(len(arr.full_copies)),
                          blit = True, interval = 750./FPS, repeat = False)