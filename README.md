<div align="center">

# 8-Puzzle Visualizer with AI Algorithms  
## Đồ án cá nhân Trí tuệ nhân tạo

### Sinh viên thực hiện  
**Họ và tên:** Trương Nhất Nguyên  
**MSSV:** 23110273  
**Giảng viên hướng dẫn:** TS. Phan Thị Huyền Trang

</div>

## Mục lục

1. [Mục tiêu](#1-mục-tiêu)  
2. [Nội dung dự án](#2-nội-dung-dự-án)  
3. [Thuật toán](#3-thuật-toán)  
   - 3.1. [Tìm kiếm không thông tin (Uninformed Search)](#31-tìm-kiếm-không-thông-tin-uninformed-search)  
     - 3.1.1. [Thành phần chính của bài toán và lời giải](#311-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.1.2. [Breadth-First Search (BFS)](#312-breadth-first-search-bfs)  
     - 3.1.3. [Depth-First Search (DFS)](#313-depth-first-search-dfs)  
     - 3.1.4. [Uniform Cost Search (UCS)](#314-uniform-cost-search-ucs)  
     - 3.1.5. [Iterative Deepening Search (IDS)](#315-iterative-deepening-search-ids)  
     - 3.1.6. [So sánh các thuật toán Uninformed Search](#316-so-sánh-các-thuật-toán-uninformed-search)  
   - 3.2. [Tìm kiếm có thông tin (Informed Search)](#32-tìm-kiếm-có-thông-tin-informed-search)  
     - 3.2.1. [Thành phần chính của bài toán và lời giải](#321-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.2.2. [Greedy Best-First Search](#322-greedy-best-first-search)  
     - 3.2.3. [A* Search](#323-a-search)  
     - 3.2.4. [Iterative Deepening A* (IDA*)](#324-iterative-deepening-a-ida)  
     - 3.2.5. [So sánh các thuật toán Informed Search](#325-so-sánh-các-thuật-toán-informed-search)  
   - 3.3. [Tìm kiếm cục bộ (Local Search)](#33-tìm-kiếm-cục-bộ-local-search)  
     - 3.3.1. [Thành phần chính của bài toán và lời giải](#331-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.3.2. [Simple Hill Climbing](#332-simple-hill-climbing)  
     - 3.3.3. [Stochastic Hill Climbing](#333-stochastic-hill-climbing)  
     - 3.3.4. [Simulated Annealing](#334-simulated-annealing)  
     - 3.3.5. [Genetic Search](#335-genetic-search)  
     - 3.3.6. [Beam Search](#336-beam-search)  
     - 3.3.7. [So sánh các thuật toán Local Search](#337-so-sánh-các-thuật-toán-local-search)  
   - 3.4. [Tìm kiếm trong môi trường phức tạp (Complex Environment Search)](#34-tìm-kiếm-trong-môi-trường-phức-tạp-complex-environment-search)  
     - 3.4.1. [Thành phần chính của bài toán và lời giải](#341-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.4.2. [AND-OR Search Algorithm](#342-and-or-search-algorithm)  
     - 3.4.3. [Partially Observable Search](#343-partially-observable-search)  
     - 3.4.4. [No Observation Search](#344-no-observation-search)  
   - 3.5. [Tìm kiếm có điều kiện ràng buộc (Constraint Satisfaction Problem)](#35-tìm-kiếm-có-điều-kiện-ràng-buộc-constraint-satisfaction-problem)  
     - 3.5.1. [Thành phần chính của bài toán và lời giải](#351-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.5.2. [Tìm kiếm kiểm thử (Constraint Testing)](#352-tìm-kiếm-kiểm-thử-constraint-testing)  
     - 3.5.3. [Backtracking CSP](#353-backtracking-csp)  
     - 3.5.4. [Backtracking AC-3](#354-backtracking-ac-3)  
   - 3.6. [Học tăng cường (Reinforcement Learning)](#36-học-tăng-cường-reinforcement-learning)  
     - 3.6.1. [Thành phần chính của bài toán và lời giải](#361-thành-phần-chính-của-bài-toán-và-lời-giải)  
     - 3.6.2. [Q-Learning](#362-q-learning)  
4. [Kết luận](#4-kết-luận)
5. [Video demo](#5-video-demo)  

## 1. Mục tiêu

- **Triển khai các thuật toán AI**: Ứng dụng nhiều thuật toán tìm kiếm (uninformed, informed, local search, non-deterministic, constraint satisfaction, reinforcement learning, và complex environment search) để giải bài toán 8-puzzle, giúp người dùng hiểu rõ cách hoạt động và hiệu suất của từng thuật toán.
- **So sánh hiệu suất**: Phân tích và so sánh hiệu quả của các thuật toán về thời gian chạy, bộ nhớ sử dụng, và tính tối ưu của đường đi để hiểu rõ ưu/nhược điểm của từng thuật toán.
- **Trực quan hóa**: Cung cấp giao diện đồ họa (GUI) để người dùng có thể theo dõi quá trình giải bài toán một cách trực quan.

## 2. Nội dung dự án

Dự án **8-Puzzle Solver with AI Algorithms** triển khai bài toán 8-puzzle, một bài toán cổ điển trong Trí tuệ Nhân tạo, với mục tiêu sắp xếp các ô số từ trạng thái ban đầu về trạng thái mục tiêu thông qua việc di chuyển ô trống. Dự án tích hợp **sáu nhóm thuật toán** tìm kiếm, bao gồm:

- **Tìm kiếm không thông tin (Uninformed Search)**: Các thuật toán khám phá không dựa trên heuristic như BFS, DFS, UCS, và IDS.
- **Tìm kiếm có thông tin (Informed Search)**: Các thuật toán sử dụng heuristic như Greedy Best-First Search, A*, và IDA*.
- **Tìm kiếm cục bộ (Local Search)**: Các phương pháp tối ưu cục bộ như Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Genetic Search, và Beam Search.
- **Tìm kiếm trong môi trường phức tạp (Complex Environment Search)**: Các thuật toán xử lý tình huống không xác định như AND-OR Search, Partially Observable Search, và No Observation Search.
- **Tìm kiếm có điều kiện ràng buộc (Constraint Satisfaction Problem)**: Các phương pháp như Constraint Testing, Backtracking CSP, và Backtracking AC-3.
- **Học tăng cường (Reinforcement Learning)**: Ứng dụng Q-Learning để học từ kinh nghiệm.
- **Tích hợp trực quan hóa**: Sử dụng GUI để hiển thị trạng thái ban đầu, quá trình giải, và trạng thái mục tiêu, cùng với các thông số hiệu suất (thời gian chạy, số bước, số trạng thái duyệt).

Mỗi nhóm được trình bày chi tiết với:
- **Thành phần chính của bài toán và lời giải**: Mô tả trạng thái, hành động, kiểm tra mục tiêu, hàm heuristic (nếu có), và cách tạo ra lời giải.
- **GIF minh họa**: Hình ảnh động thể hiện quá trình giải của từng thuật toán.
- **So sánh hiệu suất**: Bảng so sánh thời gian thực thi, số bước, và số trạng thái duyệt của các thuật toán.
- **Nhận xét**: Phân tích ưu điểm, nhược điểm và hiệu quả khi áp dụng vào bài toán 8-puzzle.

## 3. Thuật toán

Dự án triển khai một loạt thuật toán AI đa dạng, được phân loại thành sáu nhóm chính:

### 3.1. Tìm kiếm không thông tin (Uninformed Search)

#### 3.1.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái**: Một tuple 9 phần tử được hiển thị dưới dạng 3x3, với các số hợp lệ từ 0 - 8 (0 là ô trống).
  - **Hành động**: Di chuyển ô trống theo 4 hướng: lên, xuống, trái, phải để tạo ra các trạng thái tiếp theo.
  - **Kiểm tra mục tiêu**: So sánh trạng thái hiện tại với trạng thái mục tiêu, thường là: (1, 2, 3, 4, 5, 6, 7, 8, 0).
  - **Hàm chi phí**: Mỗi hành động di chuyển có chi phí là 1.
  - **Đặc điểm**: Không sử dụng hàm heuristic, dựa hoàn toàn vào không gian trạng thái.
- **Lời giải**:
  - Lời giải là một danh sách các trạng thái, biểu diễn chuỗi các bước di chuyển hợp lệ từ trạng thái ban đầu đến trạng thái mục tiêu. Trong mỗi thuật toán, nếu tìm thấy trạng thái mục tiêu, kết quả trả về sẽ bao gồm đường đi và số trạng thái đã duyệt qua. Nếu không tìm thấy, kết quả sẽ là danh sách rỗng.

#### 3.1.2. Breadth-First Search (BFS)
- **Mô tả**: BFS (Tìm kiếm theo chiều rộng) khám phá tất cả các trạng thái theo từng cấp độ độ sâu, từ trạng thái ban đầu đến trạng thái mục tiêu, sử dụng hàng đợi (queue).
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo tìm ra con đường ngắn nhất trong không gian tìm kiếm không có trọng số.
  - **Hoạt động**: Mở rộng tất cả trạng thái ở độ sâu hiện tại trước khi đi sâu hơn.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái.
- **Ưu điểm**:
  - Đảm bảo tính tối ưu và hoàn chỉnh.
- **Nhược điểm**:
  - Tiêu tốn nhiều bộ nhớ.
  - Thời gian chạy chậm nếu độ sâu lớn.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), với \( b \) là nhánh trung bình (2-4), \( d \) là độ sâu mục tiêu.
  - **Bộ nhớ**: \( O(b^d) \).
- **Hình ảnh minh họa**: ![GIF mô tả BFS](assets/gif_solve/BFS.gif)
- **Hình ảnh bổ sung**: ![BFS](https://upload.wikimedia.org/wikipedia/commons/f/f5/BFS-Algorithm_Search_Way.gif)
- **Liên kết**: [Wikipedia - Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- **Nhận xét**: BFS lý tưởng khi cần giải pháp tối ưu, nhưng tốn bộ nhớ và chậm với độ sâu lớn.

#### 3.1.3. Depth-First Search (DFS)
- **Mô tả**: DFS (Tìm kiếm theo chiều sâu) khám phá sâu nhất một nhánh trước khi quay lui, sử dụng ngăn xếp (stack) hoặc đệ quy.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo đường đi ngắn nhất.
  - **Hoạt động**: Đi sâu vào một nhánh, quay lui nếu không tìm thấy mục tiêu.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp.
- **Ưu điểm**:
  - Tiết kiệm bộ nhớ.
  - Nhanh nếu nhánh đầu chứa mục tiêu.
- **Nhược điểm**:
  - Không tối ưu, có nguy cơ tràn ngăn xếp.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \).
  - **Bộ nhớ**: \( O(d) \).
- **Hình ảnh minh họa**: ![GIF mô tả DFS](assets/gif_solve/DFS.gif)
- **Hình ảnh bổ sung**: ![DFS](https://upload.wikimedia.org/wikipedia/commons/7/7f/Depth-First-Search.gif)
- **Liên kết**: [Wikipedia - Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search)
- **Nhận xét**: DFS phù hợp khi bộ nhớ hạn chế, nhưng không hiệu quả nếu cần đường đi tối ưu.

#### 3.1.4. Uniform Cost Search (UCS)
- **Mô tả**: UCS mở rộng trạng thái dựa trên chi phí thấp nhất từ trạng thái ban đầu, sử dụng hàng đợi ưu tiên.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo đường đi ngắn nhất trong không gian có trọng số.
  - **Hoạt động**: Chọn trạng thái có chi phí thấp nhất để mở rộng.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` và cập nhật nếu tìm thấy chi phí thấp hơn.
- **Ưu điểm**:
  - Đảm bảo tính tối ưu và hoàn chỉnh.
- **Nhược điểm**:
  - Tiêu tốn nhiều bộ nhớ, tương tự BFS.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^{C*/ε}) \), với \( C* \) là chi phí tối ưu, \( ε = 1 \).
  - **Bộ nhớ**: \( O(b^{C*/ε}) \).
- **Hình ảnh minh họa**: ![GIF mô tả UCS](assets/gif_solve/UCS.gif)
- **Hình ảnh bổ sung**: ![UCS](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2003-04/intelligent-search/dijkstra.gif)
- **Liên kết**: [GeeksforGeeks - Uniform Cost Search](https://www.geeksforgeeks.org/uniform-cost-search-ucs-in-ai/)
- **Nhận xét**: UCS hiệu quả khi cần giải pháp tối ưu, nhưng không vượt trội so với BFS trong 8-puzzle do chi phí đồng nhất.

#### 3.1.5. Iterative Deepening Search (IDS)
- **Mô tả**: IDS kết hợp BFS và DFS, thực hiện DFS với giới hạn độ sâu tăng dần.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo đường đi ngắn nhất trong không gian không có trọng số.
  - **Hoạt động**: Lặp DFS với độ sâu tăng dần cho đến khi tìm thấy mục tiêu.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` trong mỗi lần lặp.
- **Ưu điểm**:
  - Tối ưu và tiết kiệm bộ nhớ hơn BFS.
- **Nhược điểm**:
  - Chậm hơn BFS do lặp lại nhiều lần.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), chậm hơn BFS do lặp.
  - **Bộ nhớ**: \( O(bd) \).
- **Hình ảnh minh họa**: ![GIF mô tả IDS](assets/gif_solve/IDS.gif)
- **Liên kết**: [GeeksforGeeks - Iterative Deepening Search](https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/)
- **Nhận xét**: IDS cân bằng giữa tính tối ưu và bộ nhớ, nhưng chậm hơn BFS.

#### 3.1.6. So sánh các thuật toán Uninformed Search
- **Hình ảnh so sánh hiệu suất**: ![So sánh hiệu suất Uninformed Search](assets/UninformedSearchCMP.jpg)
- **Nhận xét**: BFS và UCS đảm bảo tính tối ưu nhưng tốn bộ nhớ; DFS tiết kiệm bộ nhớ nhưng không tối ưu; IDS cân bằng nhưng chậm hơn.

### 3.2. Tìm kiếm có thông tin (Informed Search)

#### 3.2.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái**: Một tuple 9 phần tử được hiển thị dưới dạng 3x3, với các số hợp lệ từ 0 - 8 (0 là ô trống).
  - **Hành động**: Di chuyển ô trống theo 4 hướng: lên, xuống, trái, phải để tạo ra các trạng thái tiếp theo.
  - **Kiểm tra mục tiêu**: So sánh trạng thái hiện tại với trạng thái mục tiêu, thường là: (1, 2, 3, 4, 5, 6, 7, 8, 0).
  - **Hàm heuristic**: Sử dụng **Mahattan Distance** để đánh giá, cung cấp thông tin để ước tính "độ gần" từ trạng thái hiện tại đến trạng thái mục tiêu.
  - **Hàm chi phí**: Mỗi hành động di chuyển có chi phí là 1.
  - **Đặc điểm**: Sử dụng hàm heuristic để hướng dẫn tìm kiếm không gian trạng thái.
- **Lời giải**:
  - Lời giải là một danh sách các trạng thái tối ưu, dựa trên tổng chi phí đường đi \( g(n) \) và giá trị heuristic \( h(n) \).
    - Greedy chỉ sử dụng chi phí ước lượng => \( f(n) = h(n) \).
    - A* và IDA* sử dụng chi phí thực sự và chi phí ước lượng => \( f(n) = g(n) + h(n) \).

#### 3.2.2. Greedy Best-First Search
- **Mô tả**: Chọn trạng thái có giá trị heuristic thấp nhất để mở rộng, sử dụng hàng đợi ưu tiên.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo đường đi ngắn nhất.
  - **Hàm heuristic**: Khoảng cách Manhattan.
  - **Hoạt động**: Ưu tiên trạng thái có heuristic thấp nhất.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited`.
- **Ưu điểm**:
  - Nhanh hơn uninformed search.
  - Tiết kiệm bộ nhớ nếu heuristic tốt.
- **Nhược điểm**:
  - Không tối ưu, phụ thuộc vào heuristic.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \).
  - **Bộ nhớ**: \( O(b^d) \).
- **Hình ảnh minh họa**: ![GIF mô tả GBFS](assets/gif_solve/GBFS.gif)
- **Hình ảnh bổ sung**: ![Greedy Best-First Search](https://media.geeksforgeeks.org/wp-content/uploads/20240919162457/Greedy-best-First-Search-in-AI.png)
- **Liên kết**: [GeeksforGeeks - Greedy Best-First Search](https://www.geeksforgeeks.org/greedy-best-first-search-algorithm/)

#### 3.2.3. A* Search
- **Mô tả**: Kết hợp chi phí đã đi \( g \) và heuristic \( h \), chọn trạng thái có \( f = g + h \) thấp nhất.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo đường đi ngắn nhất nếu heuristic admissible và consistent.
  - **Hàm heuristic**: Khoảng cách Manhattan.
  - **Hoạt động**: Mở rộng trạng thái có \( f \) thấp nhất.
  - **Quản lý vòng lặp**: Cập nhật đường đi nếu tìm thấy \( f \) thấp hơn.
- **Ưu điểm**:
  - Tối ưu và hiệu quả hơn BFS.
- **Nhược điểm**:
  - Tốn bộ nhớ.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), nhanh hơn BFS.
  - **Bộ nhớ**: \( O(b^d) \).
- **Hình ảnh minh họa**: ![GIF mô tả A*](assets/gif_solve/AStar.gif)
- **Hình ảnh bổ sung**: ![A* Search](https://upload.wikimedia.org/wikipedia/commons/5/5d/Astar_progress_animation.gif)
- **Liên kết**: [GeeksforGeeks - A* Search Algorithm](https://www.geeksforgeeks.org/a-search-algorithm/)

#### 3.2.4. Iterative Deepening A* (IDA*)
- **Mô tả**: Kết hợp IDS và A*, sử dụng ngưỡng \( f = g + h \) tăng dần.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo nếu heuristic admissible và consistent.
  - **Hoạt động**: Thực hiện DFS với ngưỡng \( f \), tăng ngưỡng nếu không tìm thấy mục tiêu.
- **Ưu điểm**:
  - Tối ưu, tiết kiệm bộ nhớ hơn A*.
- **Nhược điểm**:
  - Chậm hơn A* do lặp lại.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \).
  - **Bộ nhớ**: \( O(d) \).
- **Hình ảnh minh họa**: ![GIF mô tả IDA*](assets/gif_solve/IDAStar.gif)
- **Liên kết**: [GeeksforGeeks - Iterative Deepening A*](https://www.geeksforgeeks.org/iterative-deepening-a-algorithm-ida-artificial-intelligence/)

#### 3.2.5. So sánh các thuật toán Informed Search
- **Hình ảnh so sánh hiệu suất**: ![So sánh hiệu suất Informed Search](assets/InformedSearch.jpg)

### 3.3. Tìm kiếm cục bộ (Local Search)

#### 3.3.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái**: Một tuple 9 phần tử được hiển thị dưới dạng 3x3, với các số hợp lệ từ 0 - 8 (0 là ô trống).
  - **Hành động**: Di chuyển ô trống theo 4 hướng: lên, xuống, trái, phải để tạo ra các trạng thái tiếp theo.
  - **Kiểm tra mục tiêu**: So sánh trạng thái hiện tại với trạng thái mục tiêu, thường là: (1, 2, 3, 4, 5, 6, 7, 8, 0).
  - **Hàm heuristic**: Sử dụng **Mahattan Distance** để đánh giá, cung cấp thông tin để ước tính "độ gần" từ trạng thái hiện tại đến trạng thái mục tiêu.
  - **Hàm chi phí**: Mỗi hành động di chuyển có chi phí là 1.
  - **Đặc điểm**:
    - Simple Hill Climbing chọn trạng thái lân cận đầu tiên có giá trị heuristic thấp hơn trạng thái hiện tại.
    - Stochastic Hill Climbing chọn ngẫu nhiên một trạng thái lân cận tốt hơn (heuristic thấp hơn) để mở rộng.
    - Simulated Annealing chấp nhận trạng thái tệ hơn với xác suất giảm dần theo nhiệt độ, giúp thoát khỏi cực trị cục bộ.
    - Genetic Algorithm sử dụng quần thể trạng thái, áp dụng lai ghép và đột biến để tạo ra trạng thái tốt hơn qua các thế hệ.
    - Beam Search giữ lại một số lượng cố định (beam_width) trạng thái tốt nhất ở mỗi bước, thay vì mở rộng toàn bộ trạng thái lân cận (\( f(n) = g(n) + h(n) \)).
- **Lời giải**:
  - Lời giải là một chuỗi các trạng thái, mỗi trạng thái cải thiện giá trị hàm đánh giá so với trạng thái trước, dẫn đến trạng thái mục tiêu.

#### 3.3.2. Simple Hill Climbing
- **Mô tả**: Chọn trạng thái con có heuristic tốt hơn trạng thái hiện tại.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo, dễ mắc kẹt tại cực trị cục bộ.
  - **Hoạt động**: Di chuyển theo hướng tăng heuristic.
- **Ưu điểm**:
  - Nhanh, tiết kiệm bộ nhớ.
- **Nhược điểm**:
  - Dễ mắc kẹt, không tối ưu.
- **Độ phức tạp**:
  - **Thời gian**: Phụ thuộc vào số lần lặp.
  - **Bộ nhớ**: \( O(1) \).
- **Hình ảnh minh họa**: ![GIF mô tả Hill Climbing](assets/gif_solve/SimpleHillClimbing.gif)
- **Liên kết**: [GeeksforGeeks - Hill Climbing](https://www.geeksforgeeks.org/introduction-hill-climbing-artificial-intelligence/)
- **Nhận xét**: Đối với bài toán 8 puzzle không gian trạng thái lớn, thuật toán Simple Hill Climbing dễ bị mắc kẹt, rơi vào cực tiểu. Nên chỉ phù hợp với những bài toán đơn giản và không gian trạng thái nhỏ.

#### 3.3.3. Stochastic Hill Climbing
- **Mô tả**: Chọn trạng thái con ngẫu nhiên, ưu tiên trạng thái tốt hơn.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo, nhưng tránh cực trị cục bộ tốt hơn.
  - **Hoạt động**: Chấp nhận trạng thái con ngẫu nhiên nếu tốt hơn.
- **Ưu điểm**:
  - Thoát cực trị cục bộ tốt hơn Simple Hill Climbing.
- **Nhược điểm**:
  - Không tối ưu, phụ thuộc vào ngẫu nhiên.
- **Độ phức tạp**:
  - **Thời gian**: Phụ thuộc vào số lần lặp.
  - **Bộ nhớ**: \( O(1) \).
- **Hình ảnh minh họa**: ![GIF mô tả Stochastic Hill Climbing](assets/gif_solve/StochasticHillClimbing.gif)
- **Liên kết**: [Wikipedia - Stochastic Hill Climbing](https://en.wikipedia.org/wiki/Hill_climbing#Variants)
- **Nhận xét**: Cũng tương tự Simple Hill Climbing, thuật toán Stochastic Hill Climbing dễ bị mắc kẹt, rơi vào cực tiểu. Nên chỉ phù hợp với những bài toán đơn giản và không gian trạng thái nhỏ.

#### 3.3.4. Simulated Annealing
- **Mô tả**: Chấp nhận trạng thái con tệ hơn với xác suất giảm dần, mô phỏng làm nguội kim loại.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Có thể tối ưu nếu lịch làm nguội chậm.
  - **Hoạt động**: Chọn trạng thái con ngẫu nhiên, chấp nhận dựa trên nhiệt độ.
- **Ưu điểm**:
  - Thoát cực trị cục bộ, linh hoạt.
- **Nhược điểm**:
  - Phụ thuộc vào lịch làm nguội.
- **Độ phức tạp**:
  - **Thời gian**: Phụ thuộc vào số lần lặp.
  - **Bộ nhớ**: \( O(1) \).
- **Hình ảnh minh họa**: ![GIF mô tả Simulated Annealing](assets/gif_solve/SimulatedAnnealing.gif)
- **Liên kết**: [Wikipedia - Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
- **Nhận xét**: Thuật toán này rất phù hợp với bài toán 8 Puzzle nhờ khả năng thoát khỏi cực tiểu địa phương.

#### 3.3.5. Genetic Search
- **Mô tả**: Mô phỏng tiến hóa sinh học, sử dụng quần thể giải pháp, lai ghép, và đột biến.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo, nhưng tìm giải pháp gần tối ưu.
  - **Hoạt động**: Lựa chọn cá thể tốt, lai ghép, đột biến, thay thế quần thể.
- **Ưu điểm**:
  - Khám phá không gian giải pháp lớn.
  - Thoát cực trị cục bộ.
- **Nhược điểm**:
  - Tốn tài nguyên, phụ thuộc vào tham số.
- **Độ phức tạp**:
  - **Thời gian**: \( O(G.F.P) \), với \( G \) là số thế hệ, \( F \) là độ phức tạp fitness, \( P \) là kích thước quần thể.
  - **Bộ nhớ**: \( O(P.L) \), với \( L \) là độ dài chromosome.
- **Hình ảnh minh họa**: ![GIF mô tả Genetic Search](assets/gif_solve/GeneticSearch.gif)
- **Liên kết**: [GeeksforGeeks - Genetic Algorithms](https://www.geeksforgeeks.org/genetic-algorithms/)
- **Nhận xét**: Thuật toán này rất phù hợp với bài toán 8 Puzzle nhờ khả năng thoát khỏi cực tiểu địa phương.

#### 3.3.6. Beam Search
- **Mô tả**: Giới hạn số trạng thái giữ lại tại mỗi bước (beam width), chọn \( k \) trạng thái tốt nhất dựa trên heuristic.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo, có thể bỏ qua đường đi tốt nhất.
  - **Hoạt động**: Mở rộng \( k \) trạng thái tốt nhất, giữ lại \( k \) trạng thái con tốt nhất.
  - **Quản lý vòng lặp**: Giới hạn số trạng thái để tránh lặp vô hạn.
- **Ưu điểm**:
  - Tiết kiệm bộ nhớ, nhanh nếu \( k \) nhỏ.
  - Linh hoạt điều chỉnh \( k \).
- **Nhược điểm**:
  - Không tối ưu, phụ thuộc vào \( k \) và heuristic.
- **Độ phức tạp**:
  - **Thời gian**: \( O(kbd) \), với \( b \) là nhánh, \( d \) là độ sâu.
  - **Bộ nhớ**: \( O(k) \).
- **Hình ảnh minh họa**: ![GIF mô tả Beam Search](assets/gif_solve/BeamSearch.gif)
- **Hình ảnh bổ sung**: ![Beam Search](https://upload.wikimedia.org/wikipedia/commons/2/23/Beam_search.gif)
- **Liên kết**: [GeeksforGeeks - Beam Search](https://www.geeksforgeeks.org/introduction-to-beam-search-algorithm/)
- **Nhận xét**: Beam Search phù hợp khi cần cân bằng giữa tốc độ và chất lượng, nhưng không đảm bảo giải pháp tối ưu trong 8-puzzle.

#### 3.3.7. So sánh các thuật toán Local Search
- **Hình ảnh so sánh hiệu suất**: ![So sánh hiệu suất Local Search](assets/LocalSearch.jpg)

### 3.4. Tìm kiếm trong môi trường phức tạp (Complex Environment Search)

#### 3.4.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái**: Một tuple 9 phần tử được hiển thị dưới dạng 3x3, với các số hợp lệ từ 0 - 8 (0 là ô trống). Với bài toán không quan sát (No Observation) hoặc bài toán xác suất (Partially Observable), không gian trạng thái được mở rộng thành tập hợp các belief states (phân phối xác suất trên các trạng thái vật lý).
  - **Hành động**: Di chuyển ô trống theo 4 hướng: lên, xuống, trái, phải để tạo ra các trạng thái tiếp theo.
  - **Kiểm tra mục tiêu**: So sánh trạng thái hiện tại với trạng thái mục tiêu, thường là: (1, 2, 3, 4, 5, 6, 7, 8, 0). Trong No Observation/Partially Observable, trạng thái mục tiêu là tập hợp trạng thái với xác suất cao nhất nằm trong các trạng thái mục tiêu.
  - **Đặc điểm**: Môi trường không xác định hoặc quan sát không đầy đủ, yêu cầu xử lý nhiều trạng thái cùng lúc.
    - Search with No Observation & Search with Partial Observation cần đầu vào một tập trạng thái.
    - AND-OR Search đầu vào chỉ cần 1 trạng thái.
- **Lời giải**:
  - Lời giải là một chuỗi các hành động dẫn tập hợp trạng thái ban đầu đến tập hợp chứa trạng thái mục tiêu.

#### 3.4.2. AND-OR Search Algorithm
- **Mô tả**: Xử lý bài toán với nhánh AND/OR, xây dựng cây tìm kiếm thỏa mãn điều kiện phức tạp.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Phụ thuộc vào triển khai, không luôn tối ưu.
  - **Hoạt động**: Xây dựng cây với nút AND (tất cả điều kiện con đúng) và OR (một điều kiện con đúng).
  - **Quản lý vòng lặp**: Kiểm tra trạng thái để tránh lặp.
- **Ưu điểm**:
  - Phù hợp với bài toán không xác định.
- **Nhược điểm**:
  - Phức tạp, tốn tài nguyên nếu không gian lớn.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \).
  - **Bộ nhớ**: \( O(b^d) \).
- **Hình ảnh minh họa**: ![GIF mô tả AND-OR Search](assets/gif_solve/AndOrSearch.gif)
- **Liên kết**: [Wikipedia - AND-OR Search](https://en.wikipedia.org/wiki/AND%E2%80%93OR_search_algorithm)
- **Nhận xét**: AND-OR Search phù hợp cho các bài toán phức tạp, nhưng ít hiệu quả trong 8-puzzle do tính chất xác định của bài toán.

#### 3.4.3. Partially Observable Search
- **Mô tả**: Xử lý bài toán 8-puzzle trong môi trường chỉ quan sát được một phần (ví dụ: không biết trạng thái đầy đủ của bảng).
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo do thiếu thông tin.
  - **Hoạt động**: Sử dụng mô hình niềm tin (belief state) để ước lượng trạng thái thực tế, chọn hành động dựa trên xác suất.
  - **Quản lý vòng lặp**: Cập nhật niềm tin sau mỗi hành động và quan sát.
- **Ưu điểm**:
  - Phù hợp với môi trường không xác định.
  - Có thể mô phỏng các tình huống thực tế hơn.
- **Nhược điểm**:
  - Phức tạp, tốn tài nguyên để duy trì niềm tin.
  - Không hiệu quả trong 8-puzzle do bài toán thường xác định.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d.|B|) \), với \( B \) là không gian niềm tin.
  - **Bộ nhớ**: \( O(|B|) \).
- **Hình ảnh minh họa**: ![GIF mô tả Partially Observable Search](assets/gif_solve/PartiallyObservableSearch.gif)
- **Liên kết**: [Wikipedia - Partially Observable Markov Decision Process](https://en.wikipedia.org/wiki/Partially_observable_Markov_decision_process)
- **Nhận xét**: Partially Observable Search phù hợp cho các bài toán thực tế hơn, nhưng không cần thiết trong 8-puzzle do môi trường xác định.

#### 3.4.4. No Observation Search
- **Mô tả**: Xử lý bài toán 8-puzzle mà không có quan sát trực tiếp, dựa trên chiến lược cố định hoặc hành động ngẫu nhiên.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo, gần như không khả thi.
  - **Hoạt động**: Thực hiện chuỗi hành động cố định hoặc ngẫu nhiên, kiểm tra trạng thái mục tiêu khi có thể.
  - **Quản lý vòng lặp**: Giới hạn số bước để tránh lặp vô hạn.
- **Ưu điểm**:
  - Đơn giản, không cần quản lý trạng thái phức tạp.
- **Nhược điểm**:
  - Hầu như không hiệu quả trong 8-puzzle do thiếu thông tin.
  - Phụ thuộc vào may mắn.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), nhưng thường không tìm được giải pháp.
  - **Bộ nhớ**: \( O(1) \).
- **Hình ảnh minh họa**: ![GIF mô tả No Observation Search](assets/gif_solve/NoObservationSearch.gif)
- **Nhận xét**: No Observation Search không thực tế cho 8-puzzle, chỉ mang tính lý thuyết.

### 3.5. Tìm kiếm có điều kiện ràng buộc (Constraint Satisfaction Problem)

#### 3.5.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái (State):** Gồm 9 biến từ \( X_1 \) đến \( X_9 \), tương ứng với 9 ô trong ma trận 3x3 (đọc từ trái qua phải, từ trên xuống dưới).
  - **Miền giá trị (Domains):** Mỗi biến có thể nhận một giá trị trong khoảng từ 0 đến 8, đại diện cho các ô số trong trò chơi. Tại mỗi thời điểm, mỗi số xuất hiện đúng một lần — không có sự trùng lặp giá trị giữa các ô.
  - **Ràng buộc (Constraints):**
    - Ràng buộc không trùng lặp giá trị: Mỗi số từ 0 đến 8 chỉ xuất hiện đúng một lần.
    - Ràng buộc hàng ngang: Với hai ô liền kề trong cùng một hàng (như \( X_1 \) và \( X_2 \)), nếu ô bên trái không chứa số 0, thì ô bên phải phải mang giá trị lớn hơn ô bên trái đúng 1 đơn vị.
    - Ràng buộc hàng dọc: Với hai ô nằm thẳng hàng theo chiều dọc (ví dụ \( X_1 \) và \( X_4 \)), nếu ô phía trên không phải là 0, thì ô phía dưới phải lớn hơn ô phía trên đúng 3 đơn vị.
    - Những ràng buộc này giúp đảm bảo trạng thái ban đầu là hợp lệ và có thể giải được bằng các thuật toán tìm kiếm.
- **Lời giải**:
  - Lời giải là một chuỗi các hành động (di chuyển hợp lệ của ô trống) dẫn tập hợp trạng thái ban đầu đến tập hợp chứa trạng thái mục tiêu, thỏa mãn tất cả các ràng buộc.

#### 3.5.2. Tìm kiếm kiểm thử (Constraint Testing)
- **Mô tả**: Kiểm tra các trạng thái của 8-puzzle để đảm bảo thỏa mãn các ràng buộc, như mỗi ô chỉ chứa một số duy nhất và ô trống có thể di chuyển hợp lệ.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Đảm bảo trạng thái hợp lệ, nhưng không đảm bảo đường đi tối ưu.
  - **Hoạt động**: Kiểm tra từng trạng thái con để đảm bảo các số từ 0-8 xuất hiện đúng một lần và các di chuyển (lên, xuống, trái, phải) hợp lệ.
  - **Quản lý vòng lặp**: Sử dụng tập hợp trạng thái đã kiểm tra để tránh lặp.
- **Ưu điểm**:
  - Đơn giản, dễ triển khai để kiểm tra tính hợp lệ.
  - Hỗ trợ các thuật toán khác bằng cách loại bỏ trạng thái không hợp lệ.
- **Nhược điểm**:
  - Không trực tiếp tìm lời giải, chỉ hỗ trợ kiểm tra.
  - Có thể tốn thời gian nếu số trạng thái lớn.
- **Độ phức tạp**:
  - **Thời gian**: \( O(1) \) cho mỗi kiểm tra trạng thái, nhưng tổng thời gian phụ thuộc vào số trạng thái.
  - **Bộ nhớ**: \( O(1) \) cho mỗi kiểm tra.
- **Hình ảnh minh họa**: ![GIF mô tả Constraint Testing](assets/gif_solve/ConstraintTesting.gif)
- **Liên kết**: [GeeksforGeeks - Constraint Satisfaction Problems](https://www.geeksforgeeks.org/constraint-satisfaction-problems-csp-in-artificial-intelligence/)
- **Nhận xét**: Constraint Testing hữu ích để đảm bảo tính hợp lệ của trạng thái trong 8-puzzle, nhưng cần kết hợp với các thuật toán tìm kiếm khác để tìm lời giải.

#### 3.5.3. Backtracking CSP
- **Mô tả**: Sử dụng tìm kiếm quay lui để gán giá trị cho các ô trong 8-puzzle, đảm bảo thỏa mãn các ràng buộc (mỗi số xuất hiện một lần, di chuyển hợp lệ).
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo đường đi ngắn nhất, nhưng đảm bảo trạng thái hợp lệ.
  - **Hoạt động**: Gán giá trị cho từng ô, quay lui nếu vi phạm ràng buộc, tiếp tục cho đến khi đạt trạng thái mục tiêu.
  - **Quản lý vòng lặp**: Quay lui tự động tránh lặp trạng thái không hợp lệ.
- **Ưu điểm**:
  - Hiệu quả trong việc tìm trạng thái hợp lệ.
  - Có thể kết hợp với heuristic để cải thiện tốc độ.
- **Nhược điểm**:
  - Chậm nếu không gian trạng thái lớn.
  - Không tối ưu về số bước di chuyển.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), với \( b \) là số giá trị có thể gán, \( d \) là số ô.
  - **Bộ nhớ**: \( O(d) \) cho ngăn xếp quay lui.
- **Hình ảnh minh họa**: ![GIF mô tả Backtracking CSP](assets/gif_solve/BacktrackingCSP.gif)
- **Liên kết**: [GeeksforGeeks - Backtracking CSP](https://www.geeksforgeeks.org/constraint-satisfaction-problems-csp-in-artificial-intelligence/)
- **Nhận xét**: Backtracking CSP phù hợp để kiểm tra tính khả thi, nhưng không hiệu quả trong việc tìm đường đi tối ưu cho 8-puzzle.

#### 3.5.4. Backtracking AC-3
- **Mô tả**: Kết hợp Backtracking CSP với thuật toán AC-3 để duy trì tính nhất quán cung (arc consistency), giảm không gian tìm kiếm bằng cách loại bỏ các giá trị không hợp lệ trước khi quay lui.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Không đảm bảo đường đi ngắn nhất.
  - **Hoạt động**: Sử dụng AC-3 để loại bỏ các giá trị không thỏa mãn ràng buộc, sau đó áp dụng quay lui để gán giá trị.
  - **Quản lý vòng lặp**: AC-3 giảm số trạng thái cần kiểm tra.
- **Ưu điểm**:
  - Hiệu quả hơn Backtracking CSP nhờ giảm không gian tìm kiếm.
  - Đảm bảo tính hợp lệ của trạng thái.
- **Nhược điểm**:
  - Phức tạp hơn Backtracking CSP.
  - Vẫn không tối ưu về số bước.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), nhưng nhanh hơn Backtracking CSP nhờ AC-3.
  - **Bộ nhớ**: \( O(d) \).
- **Hình ảnh minh họa**: ![GIF mô tả Backtracking AC-3](assets/gif_solve/BacktrackingAC3.gif)
- **Liên kết**: [Wikipedia - AC-3 Algorithm](https://en.wikipedia.org/wiki/AC-3_algorithm)
- **Nhận xét**: Backtracking AC-3 cải thiện hiệu suất so với Backtracking CSP, nhưng vẫn không lý tưởng cho 8-puzzle do không tối ưu đường đi.

### 3.6. Học tăng cường (Reinforcement Learning)

#### 3.6.1. Thành phần chính của bài toán và lời giải
- **Thành phần chính của bài toán**:
  - **Trạng thái ban đầu (Initial State):** Puzzle 3x3 với các số từ 0 đến 8 (0 là ô trống), do người dùng nhập vào, đảm bảo thỏa mãn các ràng buộc hợp lệ.
  - **Trạng thái mục tiêu (Goal State):** Trạng thái cuối cùng mà bài toán yêu cầu tìm ra, thường là: (1, 2, 3, 4, 5, 6, 7, 8, 0).
  - **Không gian trạng thái (State Space):** Bao gồm tất cả các trạng thái có thể từ trạng thái ban đầu đến trạng thái mục tiêu, được sinh ra bằng cách thực hiện các hành động hợp lệ (di chuyển ô trống).
  - **Tập hợp các hành động (Actions):** Các hành động hợp lệ bao gồm di chuyển ô trống: `UP`, `DOWN`, `LEFT`, `RIGHT`.
  - **Hàm thưởng (Reward Function):** Đánh giá hành động dựa trên:
    - **Thưởng:** +100 nếu trạng thái mới trùng với trạng thái mục tiêu.
    - **Phạt/Thưởng tương đối:** Dựa trên khoảng cách Manhattan giữa trạng thái hiện tại và trạng thái mục tiêu, thưởng cao hơn nếu khoảng cách giảm, phạt nếu tăng.
  - **Hàm Q-Value (Q-Function):** Lưu trữ giá trị kỳ vọng của việc thực hiện một hành động trong một trạng thái nhất định.
    - Q-value được cập nhật dựa trên công thức:
     ```
     Q[s][a] += α * (r + γ * max(Q[s'][a']) - Q[s][a])
     ```
     - α (alpha): Tốc độ học.
     - γ (gamma): Hệ số chiết khấu.
     - r: Thưởng nhận được.
     - max(Q[s'][a']): Giá trị Q lớn nhất có thể đạt được từ trạng thái tiếp theo. 
  - **Chính Sách Hành Động (Policy):**  
   - Sử dụng chiến lược **epsilon-greedy**:  
     - Với xác suất \( Ɛ \), chọn hành động ngẫu nhiên (khám phá).  
     - Với xác suất \( 1 - Ɛ \), chọn hành động có Q-value lớn nhất (khai thác).  
  - **Hàm Heuristic (Heuristic Function):**  
   - Sử dụng **khoảng cách Manhattan** để đánh giá mức độ gần giữa trạng thái hiện tại và trạng thái mục tiêu, hỗ trợ tính toán thưởng/phạt.
  - **Lời giải**:
   - Lời giải là một chuỗi các hành động tối ưu (di chuyển ô trống) được học thông qua Q-Learning, dẫn từ trạng thái ban đầu đến trạng thái mục tiêu, tối ưu hóa tổng giá trị thưởng tích lũy.
#### 3.6.2. Q-Learning
- **Mô tả**: Q-Learning là một thuật toán học tăng cường, học cách chọn hành động tối ưu thông qua thử-và-sai, dựa trên bảng Q lưu trữ giá trị hành động-trạng thái.
- **Phân tích lý thuyết**:
- **Tính tối ưu**: Có thể đạt giải pháp tối ưu nếu học đủ lâu và tham số được điều chỉnh tốt.
- **Hoạt động**: Cập nhật bảng Q dựa trên phần thưởng (ví dụ: -1 cho mỗi bước, +100 khi đạt mục tiêu). Chọn hành động dựa trên giá trị Q cao nhất hoặc ngẫu nhiên (epsilon-greedy).
- **Quản lý vòng lặp**: Tránh lặp vô hạn bằng cách giới hạn số bước hoặc sử dụng epsilon decay.
- **Ưu điểm**:
- Học từ kinh nghiệm, không cần mô hình môi trường.
- Có thể thích nghi với các trạng thái mới.
- **Nhược điểm**:
- Chậm để hội tụ trong không gian trạng thái lớn (8-puzzle có \( 9! = 362,880 \) trạng thái).
- Phụ thuộc vào tham số (\( α\), \( γ \), \( Ɛ \)).
- **Độ phức tạp**:
- **Thời gian**: Phụ thuộc vào số lần lặp và kích thước không gian trạng thái.
- **Bộ nhớ**: \( O(|S|.|A|) \), với \( S \) là số trạng thái, \( A \) là số hành động.
- **Hình ảnh minh họa**: ![GIF mô tả Q-Learning](assets/gif_solve/QLearning.gif)
- **Liên kết**: [GeeksforGeeks - Q-Learning](https://www.geeksforgeeks.org/q-learning-in-python/)
- **Nhận xét**: Q-Learning phù hợp cho các bài toán cần học dài hạn, nhưng không hiệu quả trong 8-puzzle do không gian trạng thái lớn và yêu cầu tính tối ưu nhanh.
- **Hình ảnh hiệu suất Q-learning**: ![Hình ảnh hiệu suất Q-Learning](assets/Q_Learning.jpg)
## 4. Kết luận
Dự án 8-Puzzle Visualizer with AI Algorithms đã xây dựng thành công một hệ thống giải bài toán 8-Puzzle bằng nhiều thuật toán trí tuệ nhân tạo hiện đại, từ các phương pháp tìm kiếm truyền thống (BFS, DFS, UCS, IDS, A*, IDA*, v.v.) đến các thuật toán học tăng cường như Q-Learning, cũng như các kỹ thuật giải quyết bài toán trong môi trường phức tạp và có ràng buộc. Việc triển khai đa dạng này không chỉ giúp giải quyết hiệu quả bài toán 8-Puzzle mà còn tạo điều kiện thuận lợi để so sánh, đánh giá hiệu suất của từng thuật toán dựa trên các tiêu chí như thời gian chạy, số bước di chuyển, số trạng thái duyệt và bộ nhớ sử dụng.

Một điểm nổi bật của dự án là giao diện trực quan hóa bằng Tkinter, cho phép người dùng dễ dàng nhập trạng thái ban đầu, lựa chọn thuật toán và quan sát trực tiếp từng bước giải của thuật toán thông qua hình ảnh động và bảng trạng thái. Công cụ này không chỉ giúp minh họa rõ ràng cách hoạt động của từng thuật toán mà còn tăng tính tương tác, hỗ trợ người học và người dùng hiểu sâu hơn về bản chất của các phương pháp AI.

Kết quả thực nghiệm cho thấy mỗi thuật toán đều có ưu, nhược điểm riêng: các thuật toán tìm kiếm không thông tin đảm bảo tính tối ưu nhưng tốn bộ nhớ, các thuật toán heuristic giúp tăng tốc độ tìm kiếm, trong khi các phương pháp học tăng cường như Q-Learning lại phù hợp với các bài toán cần khả năng thích nghi và học hỏi từ kinh nghiệm. Ngoài ra, việc tích hợp các thuật toán cho môi trường phức tạp và ràng buộc càng làm tăng tính ứng dụng thực tiễn của dự án.

Tổng thể, dự án không chỉ là một công cụ học tập hữu ích cho sinh viên và người nghiên cứu AI mà còn là nền tảng để mở rộng, phát triển các thuật toán mới hoặc áp dụng cho các bài toán tương tự trong lĩnh vực trí tuệ nhân tạo. Việc kết hợp giữa lý thuyết, thực nghiệm và trực quan hóa đã tạo nên một sản phẩm hoàn chỉnh, góp phần nâng cao hiệu quả học tập và nghiên cứu về AI.

## 5. Video demo

Xem video demo tại đây: [YouTube Demo](https://www.youtube.com/watch?v=sj3jgI3YAgc)

---

> © 2025 – Trương Nhất Nguyên – HCMUTE
