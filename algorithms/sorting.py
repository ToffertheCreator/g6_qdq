def bubble_sort(arr):
    """Bubble sort with step-by-step tracking"""
    n = len(arr)
    a = arr.copy()
    steps = []
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            steps.append({
                'arr': a.copy(),
                'active': [j, j + 1],
                'comp': comparisons,
                'swaps': swaps
            })
            
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                steps.append({
                    'arr': a.copy(),
                    'active': [j, j + 1],
                    'comp': comparisons,
                    'swaps': swaps
                })
    
    return steps


def selection_sort(arr):
    """Selection sort with step-by-step tracking"""
    n = len(arr)
    a = arr.copy()
    steps = []
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            steps.append({
                'arr': a.copy(),
                'active': [min_idx, j],
                'comp': comparisons,
                'swaps': swaps
            })
            
            if a[j] < a[min_idx]:
                min_idx = j
        
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            steps.append({
                'arr': a.copy(),
                'active': [i, min_idx],
                'comp': comparisons,
                'swaps': swaps
            })
    
    return steps

def insertion_sort(arr):
    """Insertion sort with step-by-step tracking"""
    a = arr.copy()
    steps = []
    comparisons = 0
    swaps = 0
    
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        
        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j + 1] = a[j]
            steps.append({
                'arr': a.copy(),
                'active': [j, j + 1],
                'comp': comparisons,
                'swaps': swaps
            })
            j -= 1
        
        a[j + 1] = key
        swaps += 1
        steps.append({
            'arr': a.copy(),
            'active': [j + 1],
            'comp': comparisons,
            'swaps': swaps
        })
    
    return steps

def merge_sort(arr):
    """Merge sort with step-by-step tracking"""
    steps = []
    comparisons = [0]
    swaps = [0]
    
    def merge_sort_helper(a, start, end):
        if end - start <= 1:
            return a[start:end]
        
        mid = (start + end) // 2
        left = merge_sort_helper(a, start, mid)
        right = merge_sort_helper(a, mid, end)
        
        return merge(a, left, right, start, comparisons, swaps, steps)
    
    a = arr.copy()
    merge_sort_helper(a, 0, len(a))
    return steps

def merge(arr, left, right, start, comparisons, swaps, steps):
    """Merge helper for merge sort"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        comparisons[0] += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        
        swaps[0] += 1
        # Update array for visualization
        for k, val in enumerate(result):
            arr[start + k] = val
        
        steps.append({
            'arr': arr.copy(),
            'active': [start + len(result) - 1],
            'comp': comparisons[0],
            'swaps': swaps[0]
        })
    
    while i < len(left):
        result.append(left[i])
        swaps[0] += 1
        arr[start + len(result) - 1] = left[i]
        steps.append({
            'arr': arr.copy(),
            'active': [start + len(result) - 1],
            'comp': comparisons[0],
            'swaps': swaps[0]
        })
        i += 1
    
    while j < len(right):
        result.append(right[j])
        swaps[0] += 1
        arr[start + len(result) - 1] = right[j]
        steps.append({
            'arr': arr.copy(),
            'active': [start + len(result) - 1],
            'comp': comparisons[0],
            'swaps': swaps[0]
        })
        j += 1
    
    return result

def quick_sort(arr):
    """Quick sort with step-by-step tracking"""
    steps = []
    comparisons = [0]
    swaps = [0]
    
    def quick_sort_helper(a, low, high):
        if low < high:
            pi = partition(a, low, high, comparisons, swaps, steps)
            quick_sort_helper(a, low, pi - 1)
            quick_sort_helper(a, pi + 1, high)
    
    a = arr.copy()
    quick_sort_helper(a, 0, len(a) - 1)
    return steps

def partition(arr, low, high, comparisons, swaps, steps):
    """Partition helper for quick sort"""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        comparisons[0] += 1
        steps.append({
            'arr': arr.copy(),
            'active': [j, high],
            'comp': comparisons[0],
            'swaps': swaps[0]
        })
        
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            swaps[0] += 1
            steps.append({
                'arr': arr.copy(),
                'active': [i, j],
                'comp': comparisons[0],
                'swaps': swaps[0]
            })
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    swaps[0] += 1
    steps.append({
        'arr': arr.copy(),
        'active': [i + 1, high],
        'comp': comparisons[0],
        'swaps': swaps[0]
    })
    
    return i + 1