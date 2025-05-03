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
  - **Thời gian**: \( O(b^d) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle), và \( d \) là độ sâu tối đa của cây tìm kiếm (có thể bằng số trạng thái tối đa \( 9! = 362,880 \) nếu không cắt tỉa). Với 8-puzzle, \( d \) thường rất lớn nếu không có giới hạn độ sâu.
  - **Bộ nhớ**: \( O(d) \), vì DFS chỉ lưu trữ các trạng thái trên nhánh hiện tại trong ngăn xếp, ít tốn bộ nhớ hơn BFS. Tuy nhiên, nếu \( d \) không được giới hạn, bộ nhớ vẫn có thể bị vượt quá do đệ quy sâu.
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
- **Hình ảnh minh họa**: ![GIF mô tả IDS]()
- **Liên kết**: geeksforgeeks -> https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/
### Tìm kiếm có thông tin (Informed Search)

#### Greedy Best-First Search
- **Mô tả**: Greedy Best-First Search là một thuật toán tìm kiếm có thông tin, sử dụng hàm heuristic để định hướng tìm kiếm, ưu tiên mở rộng trạng thái có giá trị heuristic thấp nhất (ước lượng chi phí từ trạng thái hiện tại đến mục tiêu). Thuật toán này sử dụng hàng đợi ưu tiên (priority queue) để chọn trạng thái tiếp theo dựa trên giá trị heuristic.
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: Greedy Best-First Search **không đảm bảo** tìm ra con đường ngắn nhất đến trạng thái mục tiêu, ngay cả trong không gian tìm kiếm không có trọng số như bài toán 8-puzzle. Điều này xảy ra vì thuật toán chỉ dựa vào giá trị heuristic (ước lượng chi phí còn lại), mà không xem xét chi phí đã đi từ trạng thái ban đầu. Ví dụ, với trạng thái ban đầu `217304865`, Greedy Best-First Search có thể tìm một đường đi dài hơn (kết quả tối ưu của BFS), nếu nó đi theo nhánh có heuristic thấp nhưng không phải là đường đi ngắn nhất.
  - **Hàm heuristic**: Trong dự án này, Greedy Best-First Search sử dụng **khoảng cách Manhattan** làm hàm heuristic. Khoảng cách Manhattan tính tổng khoảng cách thẳng (theo hàng và cột) của mỗi ô từ vị trí hiện tại đến vị trí mục tiêu, bỏ qua ô trống. Ví dụ, với trạng thái `217304865`, ô số 1 ở vị trí (0, 1), trong khi vị trí mục tiêu của nó là (0, 0), nên khoảng cách Manhattan của ô 1 là \( |0-0| + |1-0| = 1 \). Tổng khoảng cách Manhattan là tổng của tất cả các ô.
  - **Hoạt động**: Bắt đầu từ trạng thái ban đầu, Greedy Best-First Search tính giá trị heuristic cho các trạng thái con và chọn trạng thái có giá trị heuristic thấp nhất để mở rộng. Quá trình này tiếp tục cho đến khi tìm thấy trạng thái mục tiêu. Ví dụ, với trạng thái ban đầu `217304865`, thuật toán có thể ưu tiên di chuyển ô trống để giảm khoảng cách Manhattan, nhưng có thể bỏ qua các đường đi ngắn hơn nếu chúng có giá trị heuristic cao hơn tại thời điểm đó.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái, ngăn ngừa vòng lặp vô hạn. Tuy nhiên, nếu heuristic không tốt (ví dụ: không nhất quán), thuật toán có thể bị mắc kẹt trong các trạng thái không dẫn đến mục tiêu.
  ![UCS](https://media.geeksforgeeks.org/wp-content/uploads/20240919162457/Greedy-best-First-Search-in-AI.png)
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle), và \( d \) là độ sâu tối đa của cây tìm kiếm (có thể lên đến \( 9! = 362,880 \) nếu không cắt tỉa). Độ phức tạp thực tế phụ thuộc vào chất lượng của hàm heuristic: nếu heuristic tốt, thuật toán có thể nhanh hơn; nếu không, nó có thể tệ hơn cả DFS.
  - **Bộ nhớ**: \( O(b^d) \), vì Greedy Best-First Search phải lưu trữ tất cả các trạng thái trong hàng đợi ưu tiên. Trong trường hợp xấu nhất, bộ nhớ cần thiết có thể lớn hơn cả BFS, đặc biệt nếu heuristic dẫn đến việc mở rộng nhiều trạng thái không liên quan.
- **Hình ảnh minh họa**: ![GIF mô tả GBFS](assets/gif_solve/GBFS.gif)
- **Liên kết**: geeksforgeeks -> https://www.geeksforgeeks.org/greedy-best-first-search-algorithm/

#### A* Search
- **Mô tả**: A* Search là một thuật toán tìm kiếm có thông tin, kết hợp chi phí đã đi (g) từ trạng thái ban đầu đến trạng thái hiện tại với giá trị heuristic (h) để ước lượng chi phí thấp nhất từ trạng thái ban đầu đến mục tiêu qua trạng thái hiện tại. Thuật toán này sử dụng hàng đợi ưu tiên (priority queue) để chọn trạng thái tiếp theo dựa trên giá trị \( f = g + h \).
- **Phân tích lý thuyết**:
  - **Tính tối ưu**: A* đảm bảo tìm ra con đường ngắn nhất đến trạng thái mục tiêu trong không gian tìm kiếm không có trọng số (như bài toán 8-puzzle), miễn là hàm heuristic \( h \) là **admissible** (không bao giờ ước lượng quá chi phí thực tế) và **consistent** (tuân theo bất đẳng thức tam giác: \( h(n) \leq c(n, n') + h(n') \)). Trong dự án này, khoảng cách Manhattan là admissible và consistent, nên A* luôn tối ưu.
  - **Hàm heuristic**: A* sử dụng **khoảng cách Manhattan** làm hàm heuristic \( h \), tương tự Greedy Best-First Search. Chi phí đã đi \( g \) là số bước từ trạng thái ban đầu đến trạng thái hiện tại (mỗi bước có chi phí 1). Ví dụ, với trạng thái ban đầu `217304865`, nếu một trạng thái con có \( g = 5 \) (5 bước từ trạng thái ban đầu) và \( h = 10 \) (khoảng cách Manhattan), thì \( f = 15 \).
  - **Hoạt động**: Bắt đầu từ trạng thái ban đầu, A* tính \( f = g + h \) cho mỗi trạng thái con và chọn trạng thái có giá trị \( f \) thấp nhất để mở rộng. Quá trình này tiếp tục cho đến khi tìm thấy trạng thái mục tiêu. Với trạng thái ban đầu `217304865`, A* sẽ tìm đường đi ngắn nhất (24 bước, giống BFS), nhưng thường nhanh hơn nhờ heuristic định hướng tìm kiếm.
  - **Quản lý vòng lặp**: Sử dụng tập hợp `visited` để tránh lặp lại trạng thái, nhưng A* cũng cần kiểm tra nếu một trạng thái được tìm thấy lại với \( f \) thấp hơn (để cập nhật đường đi). Điều này đảm bảo tính tối ưu ngay cả khi không gian tìm kiếm có vòng lặp.
- **Độ phức tạp**:
  - **Thời gian**: \( O(b^d) \), trong đó \( b \) là nhánh trung bình (tối đa 4 trong 8-puzzle), và \( d \) là độ sâu của đường đi tối ưu. Tuy nhiên, với một heuristic tốt (như khoảng cách Manhattan), A* thường duyệt ít trạng thái hơn BFS, nên hiệu quả hơn về thời gian trong thực tế.
  - **Bộ nhớ**: \( O(b^d) \), vì A* phải lưu trữ tất cả các trạng thái trong hàng đợi ưu tiên, tương tự BFS và Greedy Best-First Search. Tuy nhiên, nhờ heuristic, số trạng thái được lưu trữ thường ít hơn.

#### Iterative Deepening A* (IDA*)
- **Mô tả**: Biến thể của A* với giới hạn độ sâu để tiết kiệm bộ nhớ.

#### Beam Search
- **Mô tả**: Tìm kiếm cục bộ với giới hạn số lượng trạng thái tốt nhất tại mỗi bước.

### Tìm kiếm cục bộ (Local Search)

#### Biến thể Hill Climbing
- **Simple Hill Climbing**: Tìm kiếm theo hướng tăng dần giá trị heuristic.
- **Stochastic Hill Climbing**: Thêm yếu tố ngẫu nhiên để tránh mắc kẹt tại cực trị cục bộ.

#### Simulated Annealing
- **Mô tả**: Tìm kiếm dựa trên mô phỏng quá trình làm nguội kim loại, chấp nhận các bước xấu để thoát khỏi cực trị cục bộ.

### Tìm kiếm không xác định (Non-deterministic Search)

#### AND-OR Search Algorithm
- **Mô tả**: Thuật toán xử lý các bài toán có nhánh AND/OR, tìm kiếm giải pháp trong không gian không xác định.