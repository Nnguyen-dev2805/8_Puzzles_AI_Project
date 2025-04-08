# 8_Puzzles_AI_Project
Kho lưu trữ này chứa dự án 8-Puzzle Solver with AI Algorithm! Dự án này triển khai nhiều thuật toán AI khác nhau để giải bài toán 8-puzzle cổ điển. Ngoài ra, dự án còn hỗ trợ giao diện hiển thị cho người dùng dễ quan sát và đánh giá thuật toán.
## Cách sử dụng
1. Sao chép dự án bằng cách 

        git clone https://github.com/Nnguyen-dev2805/8_Puzzles_AI_Project.git

2. Đi đến thư mục dự án 

3. Chạy lệnh sau

        python main.py
## Thuật toán
### Breadth-First Search (BFS)
BFS khám phá tất cả các trạng thái có thể có theo từng cấp độ, đảm bảo tìm ra con đường ngắn nhất đến mục tiêu.
![GIF mô tả](assets/gif_solve/BFS.gif)
### Depth-First Search (DFS)
DFS khám phá các trạng thái bằng cách đi sâu vào một nhánh đến khi không thể tiếp tục, sau đó quay lại (backtrack) để thử nhánh khác, không đảm bảo tìm ra con đường ngắn nhất nhưng sử dụng ít bộ nhớ hơn.
### Uniform Cost Search (UCS)
UCS là phiên bản tổng quát của Breadth-First Search (BFS), nhưng thay vì mở rộng theo tầng, nó mở rộng node theo chi phí nhỏ nhất đến hiện tại
Nó sử dụng hàng đợi ưu tiên dựa trên chi phí 
Luôn chọn node có chi phí thấp nhất để mở rộng trước
Độ phức tạp thời gian: O(b^d)
Độ phức tạp không gian: O(b^d)
Với b: số nhánh mở rộng  d: độ sâu
Nguyên lý hoạt động:
1. Đưa trạng thái bắt đầu vào hàng đợi ưu tiên với cost = 0
2. Lặp:
        Lấy node có chi phí thấp nhất ra
        Nếu là goal -> trả kết quả
        Nếu chưa, mở rộng các node con, cộng chi phí,thêm vào queue
        Nếu node đã từng được duyệt với chi phí thấp hơn -> bỏ qua
### A*
Một thuật toán tìm kiếm và duyệt đồ thị tìm đường đi ngắn nhất từ ​​một nút bắt đầu đến một nút đích bằng cách kết hợp chi phí để đến nút đó và chi phí ước tính từ nút đến đích (sử dụng phương pháp tìm kiếm).
### Iterative Deepening A*

### Best First Search
