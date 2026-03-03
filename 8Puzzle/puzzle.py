import numpy as np
import heapq
# initial_state = np.random.permutation(9).reshape(3, 3)
initial_state = np.array(
[
    [1,2,3],
    [4,0,6],
    [7,5,8]
])

destination_state = np.array(
[
    [1,2,3],
    [4,5,6],
    [7,8,0]
])
def h1_distance(state): # Hàm tính heuristic kiểu 1 (misplaced tiles heuristic)
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, 3)
                distance += 1 if i == goal_x and j== goal_y else 0
    return 8-distance 

def h2_distance(state): # Hàm tính heuristic kiểu 2 (Manhattan distance)
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, 3)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance 
def change_state(state):
    x, y = np.argwhere(state == 0)[0]
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = state.copy()
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def state_to_tuple(state):
    return tuple(map(tuple, state))

def a_star(start,mode): # Thuật toán A*
    frontier = []
    counter = 0
    if mode == 0:
        h_start = h2_distance(start)
    else: 
        h_start = h1_distance(start)
    # Path now stores tuples of (state, f, g, h)
    heapq.heappush(frontier, (h_start, 0, counter, start, []))
    visited = set()
    visited_states = []  # Lưu lại các trạng thái đã duyệt để in ra
    while frontier:
        f, g, _, state, path = heapq.heappop(frontier)
        if np.array_equal(state, destination_state):
            if mode==0:
                h = h2_distance(state)
            else: 
                h = h1_distance(state)
            return path + [(state, f, g, h)], visited_states
        state_key = state_to_tuple(state)
        if state_key in visited:
            continue
        visited.add(state_key)
        if mode == 0:
            current_h = h2_distance(state)
        else:
            current_h = h1_distance(state)
        visited_states.append((state, f, g, current_h))  # Lưu trạng thái đã duyệt
        current_path_item = (state, f, g, current_h)

        for neighbor in change_state(state):
            if state_to_tuple(neighbor) not in visited:
                new_g = g + 1
                if mode == 0:
                    h_neighbor = h2_distance(neighbor)
                else:
                    h_neighbor = h1_distance(neighbor)
                new_f = new_g + h_neighbor
                counter += 1
                heapq.heappush(frontier, (new_f, new_g, counter, neighbor, path + [current_path_item]))
    return None, visited_states

def print_path(path, visited_states):
    if path is None:
        print("Không tìm được lời giải!")
        return
    
    print(f"=== ĐƯỜNG ĐI GIẢI PHÁP (Số bước: {len(path) - 1}) ===\n")
    for step, (state, f, g, h) in enumerate(path):
        print(f"Bước {step}: f(n)={f}, g(n)={g}, h(n)={h}")
        for row in state:
            print("  ", row)
        print()
    
    # print(f"=== CÁC TRẠNG THÁI ĐÃ DUYỆT (Tổng: {len(visited_states)}) ===\n")
    # for i, (state, f, g, h) in enumerate(visited_states):
    #     print(f"Trạng thái đã duyệt {i+1}: f(n)={f}, g(n)={g}, h(n)={h}")
    #     for row in state:
    #         print("  ", row)
    #     print()
if __name__=='__main__':
    path, visited_states = a_star(initial_state,0)
    print_path(path, visited_states)



