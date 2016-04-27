## Cross Four
Connect-Four is a game for two players, where the object of the game is to get four or
more pieces of your color in a line vertically, horizontally, or diagonally. The game board
is a grid of spaces for pieces, six high and seven wide.

Pieces are inserted at the top of the game board and fall to the lowest open level in
their column. Players attempt to get four pieces in a row while blocking their opponent
from doing the same. Whoever gets four of their pieces in a line first wins, but if the board
fills, it is a draw.

## Algorithm
Minimax Algorithm.

```Pseudocode
01 function minimax(node, depth, maximizingPlayer)
02     if depth = 0 or node is a terminal node
03         return the heuristic value of node
04     if maximizingPlayer
05         bestValue := −∞
06         for each child of node
07             v := minimax(child, depth − 1, FALSE)
08             bestValue := max(bestValue, v)
09         return bestValue
10     else    (* minimizing player *)
11         bestValue := +∞
12         for each child of node
13             v := minimax(child, depth − 1, TRUE)
14             bestValue := min(bestValue, v)
15         return bestValue
```

## Evaluation Function
- Weight for 4-in-a-rows: 10000
- Weight for 3-in-a-rows: 100
- Weight for 2-in-a-rows: 1
  
Heuristic evaluation function:

(num of 4-in-a-rows)*10000 + (num of 3-in-a-rows)*100 + (num of 2-in-a-rows)*1 
      
## Alpha-beta Pruning

```Pseudocode
01 function alphabeta(node, depth, α, β, maximizingPlayer)
02      if depth = 0 or node is a terminal node
03          return the heuristic value of node
04      if maximizingPlayer
05          v := -∞
06          for each child of node
07              v := max(v, alphabeta(child, depth - 1, α, β, FALSE))
08              α := max(α, v)
09              if β ≤ α
10                  break (* β cut-off *)
11          return v
12      else
13          v := ∞
14          for each child of node
15              v := min(v, alphabeta(child, depth - 1, α, β, TRUE))
16              β := min(β, v)
17              if β ≤ α
18                  break (* α cut-off *)
19          return v
```
