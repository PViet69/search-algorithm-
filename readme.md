# Giải quyết bài toán 8-Puzzle bằng thuật toán A*

Đây là một đoạn mã Python để giải quyết bài toán 8-puzzle kinh điển bằng thuật toán tìm kiếm A* (A-star).

## Giới thiệu

8-puzzle là một bài toán trượt ô vuông bao gồm một khung 3x3 với 8 ô được đánh số và một ô trống. Mục tiêu là sắp xếp các ô từ trạng thái ban đầu (initial state) về trạng thái đích (goal state) bằng cách trượt các ô vào vị trí trống.

Dự án này sử dụng thuật toán A* kết hợp với heuristic **khoảng cách Manhattan** để tìm ra con đường ngắn nhất từ trạng thái ban đầu đến trạng thái đích.


Chương trình sẽ in ra số bước cần thiết và từng bước di chuyển để giải quyết bài toán.

## Giải thích mã nguồn

### 1. Khai báo ban đầu

```python
import numpy as np
import heapq

initial_state = np.array(...)
destination_state = np.array(...)
```

- **`numpy`**: Được sử dụng để làm việc với ma trận (grid) một cách hiệu quả.
- **`heapq`**: Cung cấp một cấu trúc dữ liệu hàng đợi ưu tiên (priority queue), là thành phần cốt lõi của thuật toán A*.
- **`initial_state`**: Trạng thái bắt đầu của bài toán.
- **`destination_state`**: Trạng thái mục tiêu cần đạt được.

### 2. `manhattan_distance(state)`

```python
def manhattan_distance(state): # Hàm tính heuristic (Manhattan distance)
    # ...
```

Đây là hàm heuristic `h(n)`         toán A*. Nó tính tổng khoảng cách Manhattan của tất cả các ô (trừ ô trống) đến vị trí đúng của chúng trong trạng thái đích.

- **Khoảng cách Manhattan**: Là tổng của khoảng cách theo chiều ngang và chiều dọc giữa hai điểm. Ví dụ, khoảng cách từ ô ở vị trí `(i, j)` đến vị trí đích `(goal_x, goal_y)` là `|i - goal_x| + |j - goal_y|`.
- Heuristic này được chấp nhận (admissible) vì nó không bao giờ đánh giá quá cao chi phí thực tế để đến đích (số lần di chuyển thực tế luôn lớn hơn hoặc bằng khoảng cách Manhattan).

### 3. `change_state(state)`

```python
def change_state(state):
    # ...
```

Hàm này tìm tất cả các trạng thái "hàng xóm" (các bước đi hợp lệ tiếp theo) từ một trạng thái hiện tại.

- Nó tìm vị trí của ô trống (số `0`).
- Sau đó, nó tạo ra các trạng thái mới bằng cách hoán đổi ô trống với các ô liền kề (trên, dưới, trái, phải), miễn là các nước đi đó không đi ra ngoài lưới 3x3.

### 4. `state_to_tuple(state)`

```python
def state_to_tuple(state):
    return tuple(map(tuple, state))
```

Một hàm phụ trợ quan trọng. Các đối tượng `numpy.array` không thể được thêm vào một `set` (tập hợp). Hàm này chuyển đổi một mảng numpy 2D thành một tuple lồng nhau, có thể được thêm vào `set` `visited` để theo dõi các trạng thái đã được duyệt qua.

### 5. `a_star(start)`

```python
def a_star(start): # Thuật toán A*
    # ...
```

Đây là nơi triển khai thuật toán A*.

- **`frontier`**: Một hàng đợi ưu tiên (min-heap) lưu trữ các trạng thái cần khám phá. Các trạng thái được sắp xếp theo giá trị `f(n)`.
- **`visited`**: Một `set` để lưu trữ các trạng thái đã được khám phá để tránh lặp lại và chu trình vô hạn.
- **`f(n) = g(n) + h(n)`**:
    - `g(n)`: Chi phí thực tế từ trạng thái bắt đầu đến trạng thái hiện tại (số bước đã đi).
    - `h(n)`: Chi phí ước tính từ trạng thái hiện tại đến đích (tính bằng `manhattan_distance`).
- **Vòng lặp chính**:
    1. Lấy trạng thái có giá trị `f` nhỏ nhất từ `frontier`.
    2. Nếu đó là trạng thái đích, trả về đường đi.
    3. Nếu không, đánh dấu nó là đã truy cập.
    4. Tạo ra tất cả các trạng thái hàng xóm.
    5. Đối với mỗi hàng xóm chưa được truy cập, tính toán giá trị `f` mới của nó và đẩy nó vào `frontier`.
- **`counter`**: Được sử dụng như một yếu tố phá vỡ sự cân bằng. Nếu hai trạng thái có cùng giá trị `f`, `heapq` sẽ so sánh phần tử tiếp theo. `counter` đảm bảo luôn có một giá trị duy nhất để so sánh, tránh lỗi khi so sánh hai mảng numpy.

### 6. `print_path(path)`

```python
def print_path(path):
    # ...
```

Một hàm tiện ích để định dạng và in ra đường đi giải pháp một cách rõ ràng, hiển thị từng bước từ đầu đến cuối.