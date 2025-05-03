# 8_Puzzles_AI_Project
Kho lưu trữ này chứa dự án 8-Puzzle Solver with AI Algorithms – một ứng dụng giúp giải bài toán 8-puzzle cổ điển bằng nhiều thuật toán Trí tuệ Nhân tạo (AI) khác nhau. Dự án không chỉ triển khai các thuật toán tìm kiếm (uninformed & informed) mà còn hỗ trợ giao diện đồ họa thân thiện, giúp người dùng dễ dàng theo dõi quá trình giải và so sánh hiệu quả của các thuật toán.
## Mục lục
- [Cách sử dụng](#cách-sử-dụng)
- [Thuật toán](#thuật-toán)
  - [Tìm kiếm không thông tin (Uninformed Search)](#tìm-kiếm-không-thông-tin-uninformed-search)
    - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
    - [Depth-First Search (DFS)](#depth-first-search-dfs)
    - [Uniform Cost Search (UCS)](#uniform-cost-search-ucs)
    - [Iterative Deepening Search (IDS)](#iterative-deepening-search-ids)
  - [Tìm kiếm có thông tin (Informed Search)](#tìm-kiếm-có-thông-tin-informed-search)
    - [Greedy Best-First Search](#greedy-best-first-search)
    - [A* Search](#a-search)
    - [Iterative Deepening A* (IDA*)](#iterative-deepening-a-ida)
    - [Beam Search](#beam-search)
  - [Tìm kiếm cục bộ (Local Search)](#tìm-kiếm-cục-bộ-local-search)
    - [Biến thể Hill Climbing](#biến-thể-hill-climbing)
      - [Simple Hill Climbing](#simple-hill-climbing)
      - [Stochastic Hill Climbing](#stochastic-hill-climbing)
    - [Simulated Annealing](#simulated-annealing)
  - [Tìm kiếm không xác định (Non-deterministic Search)](#tìm-kiếm-không-xác-định-non-deterministic-search)
    - [AND-OR Search Algorithm](#and-or-search-algorithm)
- [Tính năng giao diện (GUI Features)](#tính-năng-giao-diện-gui-features)
- [Đóng góp](#đóng-góp)
## Cách sử dụng
1. Tải dự án bằng cách 

        git clone https://github.com/Nnguyen-dev2805/8_Puzzles_AI_Project.git

2. Đi đến thư mục dự án 

3. Chạy lệnh sau

        python main.py
## Thuật toán

Dự án triển khai một loạt thuật toán AI đa dạng, được phân loại thành các nhóm sau:

### Tìm kiếm không thông tin (Uninformed Search)

#### Breadth-First Search (BFS)
- **Mô tả**: BFS (Tìm kiếm theo chiều rộng) là một thuật toán tìm kiếm không thông tin, khám phá tất cả các trạng thái có thể có theo từng cấp độ độ sâu, từ trạng thái ban đầu đến trạng thái mục tiêu. Thuật toán này sử dụng hàng đợi (queue) để đảm bảo rằng các trạng thái được mở rộng theo thứ tự từ gần nhất đến xa nhất so với trạng thái ban đầu.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: BFS đảm bảo tìm ra con đường ngắn nhất đến trạng thái mục tiêu trong không gian tìm kiếm không có trọng số (unweighted graph), như bài toán 8-puzzle. Điều này xảy ra vì BFS khám phá tất cả các trạng thái ở độ sâu hiện tại trước khi đi sâu hơn.
  - **Hoạt động**: Bắt đầu từ trạng thái ban đầu, BFS mở rộng tất cả các trạng thái con ở độ sâu 1, sau đó độ sâu 2, và tiếp tục cho đến khi tìm thấy trạng thái mục tiêu. Ví dụ, với trạng thái ban đầu `826514037`, BFS sẽ tìm đường đi ngắn nhất đến `123456780`.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái, ngăn ngừa vòng lặp vô hạn.
![BFS](https://upload.wikimedia.org/wikipedia/commons/f/f5/BFS-Algorithm_Search_Way.gif)
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle: lên, xuống, trái, phải), và \( d \) là độ sâu của trạng thái mục tiêu. Với 8-puzzle, \( b \) thường là 2-3 (do một số di chuyển không hợp lệ), và \( d \) có thể lên đến 31 (độ sâu tối đa cho một số trạng thái).
  - **Bộ nhớ**: \( O(b^d) \), vì BFS phải lưu trữ tất cả các trạng thái ở độ sâu hiện tại trong hàng đợi. Điều này có thể dẫn đến tốn nhiều bộ nhớ nếu \( d \) lớn.
- **Hình ảnh minh họa**: ![GIF mô tả BFS](assets/gif_solve/BFS.gif)
- **Liên kết**: wikipedia -> https://en.wikipedia.org/wiki/Breadth-first_search
### Depth-First Search (DFS)
- **Mô tả**: DFS (Tìm kiếm theo chiều sâu) là một thuật toán tìm kiếm không thông tin, khám phá sâu nhất một nhánh trước khi quay lui và thử nhánh khác. Thuật toán này sử dụng ngăn xếp (stack) hoặc phương pháp đệ quy để quản lý các trạng thái cần mở rộng.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: DFS không đảm bảo tìm ra con đường ngắn nhất đến trạng thái mục tiêu trong không gian tìm kiếm không có trọng số, như bài toán 8-puzzle. Thay vào đó, nó có thể tìm một đường đi rất dài nếu nhánh đầu tiên không dẫn trực tiếp đến mục tiêu. Ví dụ, với trạng thái ban đầu `826514037`, DFS có thể tìm một đường đi dài hàng chục nghìn bước trước khi đạt `123456780`.
  - **Hoạt động**: Bắt đầu từ trạng thái ban đầu, DFS đi sâu vào một nhánh bằng cách chọn một hành động (lên, xuống, trái, phải) và tiếp tục cho đến khi gặp trạng thái không thể mở rộng hoặc đạt mục tiêu. Nếu không thành công, nó quay lui và thử nhánh khác. Quá trình này tiếp diễn cho đến khi tìm thấy giải pháp hoặc đã thử hết các nhánh.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái, ngăn ngừa vòng lặp vô hạn. Tuy nhiên, nếu không giới hạn độ sâu, DFS có thể dẫn đến tràn ngăn xếp (stack overflow).
  ![DFS](https://upload.wikimedia.org/wikipedia/commons/7/7f/Depth-First-Search.gif)
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^m) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle), và \( m \) là độ sâu tối đa của cây tìm kiếm (có thể bằng số trạng thái tối đa \( 9! = 362,880 \) nếu không cắt tỉa). Với 8-puzzle, \( m \) thường rất lớn nếu không có giới hạn độ sâu.
  - **Bộ nhớ**: \( O(bm) \), vì DFS chỉ lưu trữ các trạng thái trên nhánh hiện tại trong ngăn xếp, ít tốn bộ nhớ hơn BFS. Tuy nhiên, nếu \( m \) không được giới hạn, bộ nhớ vẫn có thể bị vượt quá do đệ quy sâu.
- **Hình ảnh minh họa**: ![GIF mô tả DFS](assets/gif_solve/DFS.gif)
- **Liên kết**: wikipedia -> https://en.wikipedia.org/wiki/Depth-first_search
### Uniform Cost Search (UCS)
- **Mô tả**: UCS (Tìm kiếm chi phí đồng nhất) là một thuật toán tìm kiếm không thông tin, mở rộng trạng thái dựa trên chi phí thấp nhất từ trạng thái ban đầu đến trạng thái hiện tại. Thuật toán này sử dụng hàng đợi ưu tiên (priority queue) để luôn chọn trạng thái có tổng chi phí thấp nhất để mở rộng trước.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: UCS đảm bảo tìm ra con đường có chi phí thấp nhất đến trạng thái mục tiêu, ngay cả trong không gian tìm kiếm có trọng số (weighted graph). Trong bài toán 8-puzzle, nơi mỗi di chuyển có chi phí 1, UCS hoạt động tương tự BFS, đảm bảo tìm đường đi ngắn nhất về số bước.
  - **Hoạt động**: Bắt đầu từ trạng thái ban đầu, UCS thêm tất cả trạng thái con vào hàng đợi ưu tiên, với chi phí là số bước từ trạng thái ban đầu. Nó luôn mở rộng trạng thái có chi phí thấp nhất trước. Ví dụ, với trạng thái ban đầu `826514037`, UCS sẽ tìm đường đi ngắn nhất đến `123456780`, tương tự BFS nhưng dựa trên chi phí.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái, nhưng cũng cần kiểm tra nếu một trạng thái được tìm thấy lại với chi phí thấp hơn (để cập nhật đường đi).
  ![UCS](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2003-04/intelligent-search/dijkstra.gif)
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^{C*/ε}) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle), \( C* \) là chi phí của đường đi tối ưu, và \( ε\) là chi phí nhỏ nhất của một bước (trong 8-puzzle, \( ε = 1 \), nên \( C*/ε \) tương đương với độ sâu tối ưu \( d \)). Do đó, độ phức tạp tương tự BFS: \( O(b^d) \).
  - **Bộ nhớ**: \( O(b^{C*/ε}) \), tương tự BFS, UCS phải lưu trữ tất cả các trạng thái trong hàng đợi ưu tiên, dẫn đến tốn nhiều bộ nhớ nếu không gian trạng thái lớn.
- **Hình ảnh minh họa**: ![GIF mô tả DFS](assets/gif_solve/UCS.gif)
- **Liên kết**: geeksforgeeks -> https://www.geeksforgeeks.org/uniform-cost-search-ucs-in-ai/
### Iterative Deepening Search(IDS)
- **Mô tả**: IDS (Tìm kiếm lặp sâu dần) là một thuật toán tìm kiếm không thông tin, kết hợp lợi ích của BFS và DFS. IDS thực hiện tìm kiếm theo chiều sâu (DFS) nhiều lần, mỗi lần với một giới hạn độ sâu tăng dần, cho đến khi tìm thấy trạng thái mục tiêu.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: IDS đảm bảo tìm ra con đường ngắn nhất đến trạng thái mục tiêu trong không gian tìm kiếm không có trọng số, tương tự BFS. Điều này xảy ra vì IDS lặp lại tìm kiếm với độ sâu tăng dần, đảm bảo tìm thấy trạng thái mục tiêu ở độ sâu nhỏ nhất.
  - **Hoạt động**: IDS bắt đầu với giới hạn độ sâu 0, thực hiện DFS với giới hạn này. Nếu không tìm thấy mục tiêu, tăng giới hạn lên 1 và lặp lại. Quá trình tiếp tục cho đến khi tìm thấy trạng thái mục tiêu. Ví dụ, với trạng thái ban đầu `826514037`, IDS sẽ tìm đường đi ngắn nhất đến `123456780` sau một số lần lặp.
  - **Quản lý vòng lặp**: Tương tự DFS, IDS sử dụng tập hợp `visited` để tránh lặp lại trạng thái trong mỗi lần lặp. Tuy nhiên, vì lặp lại nhiều lần, IDS có thể duyệt qua một số trạng thái nhiều lần.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), tương tự BFS, nhưng IDS có thể chậm hơn một chút do lặp lại nhiều lần. Tổng số trạng thái được duyệt qua là tổng của các lần lặp: \( (b^0 + b^1 + b^2 + \dots + b^d) \), nhưng hằng số ẩn lớn hơn BFS.
  - **Bộ nhớ**: \( O(bd) \), IDS chỉ lưu trữ các trạng thái trên nhánh hiện tại trong mỗi lần lặp, tương tự DFS, nên tiết kiệm bộ nhớ hơn BFS. Đây là lợi thế chính của IDS so với BFS.
- **Hình ảnh minh họa**: ![GIF mô tả DFS](assets/gif_solve/DFS.gif)
- **Liên kết**: geeksforgeeks -> https://www.geeksforgeeks.org/uniform-cost-search-ucs-in-ai/
### A*
Một thuật toán tìm kiếm và duyệt đồ thị tìm đường đi ngắn nhất từ ​​một nút bắt đầu đến một nút đích bằng cách kết hợp chi phí để đến nút đó và chi phí ước tính từ nút đến đích (sử dụng phương pháp tìm kiếm).
### Iterative Deepening A*

### Best First Search
