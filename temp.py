# allows for time measurement of sorting
import time
# numerical python- number function
import numpy as np
# scientific python fucntions
import scipy as sp
# plot animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrackedArray():
    
    #when class is initialized,we give it array to track and call reset
    def __init__(self, self_arr):
        self.arr = np.copy(arr)
        self.reset()
        
    #resets arrays     
    #you can call self whatever you like, just has to be the first arg in every method
    #self points to the actual instance of the class
    
    def reset(self):
        #incidices accessed
        self.indices = []
        #values of above indicies
        self.values = []
        #get/set
        self.access_type = []
        #full copy of array at every point
        self.full_copies = []
       
        
    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))
        
    def GetActivity(self, idx = None):
        if(isinstance(idx, type(None))):
            #if index not passed in as argument, returns list of tuples containing idx that was accessed and whether its read/write
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else:
            return (self.indicies[idx], self.access_type[idx])
        
            
    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)
        
    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")
            
    def __len__(self):
        return self.arr.__len__()



# making plot size 12 inches by 8 inches
plt.rcParams["figure.figsize"] = (12,8)

plt.rcParams["font.size"] = 16

FPS = 60.0



N = 30
# Values go from 0 to 1000, 30 total values
arr = np.round(np.linspace(10,1000,N), 0)
np.random.seed(0)
np.random.shuffle(arr)
arr = TrackedArray(arr)

#############################################
#############################################
# Insertion sort- O(n)2
sorter = "Insertion"
t0 = time.perf_counter()
i = 1
while(i < len(arr)):
    j = i
    while((j > 0) and (arr[j - 1] > arr[j])):
        temp = arr[j - 1]
        arr[j - 1] = arr[j]
        arr[j] = temp
        j -= 1
    i+= 1
    
dt = time.perf_counter() - t0
#############################################
#############################################
#############################################
# sorter = "Quick"

# def quicksort(low, high, A):
#     if low < high:
#         p = partition(low, high, A)
#         quicksort(low, p - 1, A)
#         quicksort(p + 1, high, A)
    
    
# def partition(low, high, A):
#     pivot = A[high]
#     i = low
#     for j in range(low, high):
#         if(A[j] < pivot):
#             temp = A[i]
#             A[i] = A[j]
#             A[j] = temp
#             i += 1
    
#     temp = A[i]
#     A[i] = A[high]
#     A[high] = temp
#     return i

# t0 = time.perf_counter()
# quicksort(0, len(arr) - 1, arr)

# dt = time.perf_counter() - t0
#############################################
#############################################


#fast string. Tip the .1f meaning give measurement one decimal place
print(f"---------- {sorter} Sort ----------")
print(f"Array sorted in {dt*1000: .2f} ms")

fig, ax = plt.subplots()
container = ax.bar(np.arange(0, len(arr), 1), arr, align = "edge", width = 0.8)
ax.set_xlim([0, N])
ax.set(xlabel = "Index", ylabel = "Value", title = f"{sorter} Sort")


#current frame is passed in.
# container is the object that stores all the individual patches with each patch being the rectangle itself
# we also need to change the high of each rectangle depending on the value

def update(frame):
    for (rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("#1f77b4")
        #must return a tuple of the things that have been updated
    return (*container,)

# # of frames comes from the total 
#blit means only if something changes will animation be redrawn, and only at that location

animation = FuncAnimation(fig, update, frames = range(len(arr.full_copies)),
                          blit = True, interval = 750./FPS, repeat = False)
