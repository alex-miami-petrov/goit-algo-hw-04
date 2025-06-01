import timeit
import random
import copy


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    return merge(left_sorted, right_sorted)

def merge(left, right):
    merged = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1
    while left_idx < len(left):
        merged.append(left[left_idx])
        left_idx += 1
    while right_idx < len(right):
        merged.append(right[right_idx])
        right_idx += 1
    return merged


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def generate_random_data(size):
    return [random.randint(0, size * 10) for _ in range(size)]

def generate_sorted_data(size):
    return list(range(size))

def generate_reverse_sorted_data(size):
    return list(range(size - 1, -1, -1))

def generate_nearly_sorted_data(size, num_swaps=10):
    data = list(range(size))
    for _ in range(num_swaps):
        idx1, idx2 = random.randrange(size), random.randrange(size)
        data[idx1], data[idx2] = data[idx2], data[idx1]
    return data


def run_tests():
    data_sizes = [100, 1000, 10000, 50000, 100000, 500000, 1000000] 

    results = {}

    for size in data_sizes:
        print(f"\n--- Тестування для розміру масиву: {size} ---")
        results[size] = {}

       
        random_data = generate_random_data(size)
        sorted_data = generate_sorted_data(size)
        reverse_sorted_data = generate_reverse_sorted_data(size)
        nearly_sorted_data = generate_nearly_sorted_data(size, num_swaps=int(size * 0.01)) 

        data_sets = {
            "Випадкові": random_data,
            "Відсортовані": sorted_data,
            "Обернено відсортовані": reverse_sorted_data,
            "Майже відсортовані": nearly_sorted_data
        }

        for data_type, original_data in data_sets.items():
            print(f"\nНабір даних: {data_type}")
            results[size][data_type] = {}

            
            stmt = "merge_sort(data.copy())" 
            setup = f"from __main__ import merge_sort; data = {original_data}"
            try:
                if size <= 1000000: # Обмеження для великих розмірів через O(N log N)
                    time_taken = timeit.timeit(stmt, setup, number=1)
                    print(f"  Merge Sort: {time_taken:.6f} секунд")
                    results[size][data_type]["Merge Sort"] = time_taken
                else:
                    print("  Merge Sort: Пропущено для дуже великих розмірів (може бути повільним)")
                    results[size][data_type]["Merge Sort"] = "N/A"
            except MemoryError:
                print(f"  Merge Sort: Помилка пам'яті для розміру {size}")
                results[size][data_type]["Merge Sort"] = "Memory Error"


            
            stmt = "insertion_sort(data.copy())"
            setup = f"from __main__ import insertion_sort; data = {original_data}"
            try:
                
                if size <= 10000: 
                    time_taken = timeit.timeit(stmt, setup, number=1)
                    print(f"  Insertion Sort: {time_taken:.6f} секунд")
                    results[size][data_type]["Insertion Sort"] = time_taken
                else:
                    print("  Insertion Sort: Пропущено для великих розмірів (дуже повільний)")
                    results[size][data_type]["Insertion Sort"] = "N/A"
            except MemoryError:
                print(f"  Insertion Sort: Помилка пам'яті для розміру {size}")
                results[size][data_type]["Insertion Sort"] = "Memory Error"

           
            stmt = "sorted(data.copy())"
            setup = f"data = {original_data}"
            try:
                time_taken = timeit.timeit(stmt, setup, number=1)
                print(f"  Timsort (sorted()): {time_taken:.6f} секунд")
                results[size][data_type]["Timsort"] = time_taken
            except MemoryError:
                print(f"  Timsort (sorted()): Помилка пам'яті для розміру {size}")
                results[size][data_type]["Timsort"] = "Memory Error"

    return results

if __name__ == "__main__":
    test_results = run_tests()
    print("\n\n--- Зведені результати ---")
    for size, data_types in test_results.items():
        print(f"\nРозмір масиву: {size}")
        for data_type, alg_results in data_types.items():
            print(f"  Набір даних: {data_type}")
            for algorithm, time_taken in alg_results.items():
                print(f"    {algorithm}: {time_taken} секунд")



# Цей аналіз і емпіричні дані демонструють, що розумний гібридний підхід, як у Timsort, може значно покращити продуктивність сортування, особливо для різноманітних реальних наборів даних.