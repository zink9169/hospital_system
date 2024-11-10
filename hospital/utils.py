
import heapq
from .models import Location, Connection


def quick_sort_doctors(doctors, key=lambda x: x.years_of_experience):
    """Sorts a list of doctors using the Quick Sort algorithm based on a given attribute."""
    if len(doctors) <= 1:
        return doctors
    else:
        pivot = doctors[len(doctors) // 2]  # Middle element as pivot
        left = [x for x in doctors if key(x) < key(pivot)]
        middle = [x for x in doctors if key(x) == key(pivot)]
        right = [x for x in doctors if key(x) > key(pivot)]
        return quick_sort_doctors(left, key) + middle + quick_sort_doctors(right, key)
    


def merge_sort_workers(workers):
    if len(workers) <= 1:
        return workers

    mid = len(workers) // 2
    left_half = merge_sort_workers(workers[:mid])
    right_half = merge_sort_workers(workers[mid:])

    return merge(left_half, right_half)

# For the merge sort
def merge(left, right):
    sorted_list = []
    i = j = 0

    # Merge the two halves based on `years_of_experience`
    while i < len(left) and j < len(right):
        if left[i].years_of_experience <= right[j].years_of_experience:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # Append any remaining elements
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    
    return sorted_list


# For the Dijkstra's algorithm to find shortest path 

def dijkstra_shortest_path(start_id, end_id):
    # Step 1: Set up the distances dictionary and priority queue
    distances = {loc.id: float('inf') for loc in Location.objects.all()}
    previous_nodes = {loc.id: None for loc in Location.objects.all()}
    distances[start_id] = 0
    priority_queue = [(0, start_id)]
    
    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        # Step 2: Early exit if we reached the destination
        if current_location == end_id:
            break
        
        # Step 3: Explore neighboring nodes
        for connection in Connection.objects.filter(start_id=current_location):
            neighbor = connection.end.id
            new_distance = current_distance + connection.distance
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_location
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Step 4: Build the shortest path from end to start
    path = []
    total_distance = distances[end_id]
    while end_id is not None:
        path.append(end_id)
        end_id = previous_nodes[end_id]

    path.reverse()
    return path, total_distance
