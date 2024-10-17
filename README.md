#### 所需套件（繪圖用）

利用 numpy & matplotlib 來繪製圖表，如果只要查看程式碼運行結果，可註解掉 import 這兩個套件的程式碼，以及呼叫 `draw_plot` 此函式的部分。

#### 執行程式碼

輸入 `python3 main.py` 後，在 terminal 中可以輸入 n 以及 obstacle(障礙物密度)的值，以查看不同網格數量的可行路徑變化。

#### 程式碼架構

1. 基本變數創建：

   - 障礙物生成：透過 `gen_obstacle` 此函式隨機生成障礙物位置。
   - 網格生成：透過 `create_board`，此函式會回傳一個 n\*n 的陣列。透過呼叫上面的障礙物生成函式，將障礙物所在的位置包含的值設為 -1。如果想查看生成的網格，可使用 `print_board` 函式。

2. 情境一實作：不同走法所需的成本相同時的可行/最佳路徑

   - 動態規劃： `numb_of_path_dp` 會接收上面生成的 n*n 陣列 (i.e.`board`) ，其中 `dp` 為用來記憶子問題解的 n*n 陣列。`dp[i][j]` 紀錄走到 `board[i][j]` 的可行路徑數量。當 `board[i][j]` 為 -1 時，可行路徑數量為 0。
   - 遞迴法：`num_of_path_recursion` 亦接收 `board` 陣列，遞迴結束條件有以下幾種：
     - 走到終點，代表可行路徑存在，因此回傳 1
     - 走到障礙物，回傳 0
     - 走到無效位置，回傳 0

3. 情境二實作：轉彎時成本加一

   - 動態規劃：`num_of_shortest_path_dp` 接收 `board` 陣列，其中 `dp[i][j][k]=(min_cost, number_of_path)`。

     - 變數說明：
       - dp 為一個 3 維陣列，每個陣列中的元素為一個 tuple，第一個值代表走到 `board[i][j]` 所需的最小成本，第二個值代表花費最小成本到達 `board[i][j]` 的路徑總數。
       - `k` 代表路徑方向（0=從左邊來 / 1=從上面來）
     - 運作機制：
       - 想到達每個位置 `board[i][j]`有兩種可能路徑：從左邊 `board[i][j - 1]` 或是上面 `board[i - 1][j]`。為了記錄是否轉彎，因此分開計算兩種方向的成本以及路徑數（i.e. dp[i][j][0] 和 dp[i][j][1]）

   - 遞迴法：`num_of_shortest_path_recursion`
