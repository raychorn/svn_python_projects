def Parent(i): return i/2
def Left(i): return 2*i
def Right(i): return 2*i+1

def Heapify(A, i, n): # A is "almost a heap" (except root); fix it so all of A is a heap 
    l = Left(i)
    r = Right(i)
    if l <= n and A[l] > A[i]: largest = l
    else: largest = i
    if r <= n and A[r] > A[largest]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        Heapify(A, largest, n)

def HeapLength(A): return len(A)-1
def BuildHeap(A): # build a heap A from an unsorted array
    n = HeapLength(A)
    for i in range(n/2,0,-1):
        Heapify(A,i,n)

def HeapSort(A): # use a heap to build sorted array from the end 
    BuildHeap(A)
    HeapSize=HeapLength(A)
    for i in range(HeapSize,1,-1):
        A[1],A[i]=A[i],A[1] # largest element is a root of heap, put it at the end of array
        HeapSize=HeapSize-1 # shrink heap size by 1 to get next largest element
        Heapify(A,1,HeapSize)

