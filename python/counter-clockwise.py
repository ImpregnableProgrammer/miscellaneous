# Relevant Leet code challenge: https://leetcode.com/problems/spiral-matrix/
# Relevant Reddit post: https://www.reddit.com/r/leetcode/comments/15xn6z9/just_got_this_question_in_an_oa_could_not_figure/
# Relevant OneCompiler Python file: https://onecompiler.com/python/42qq7sgmt (log in via Google as rkapurschool@gmail.com to access)

# Started from challenge problem I was given during the Cisco online assessment I received after applying for a position there
# I had 90 minutes to complete 3 programming problems, and unfortunately this was the one I couldn't complete in time
# mostly due to the confusing wording that was used...
# Basically, traverse a given matrix in counter-clockwise order beginning at the first element, while skipping every other element,
# and output the last element reached
# The following is the final solution I came up with after the assessment ended, and it's quite a bit less complex and more efficient
# than my initial approach

# This will output an animation in a terminal of the matrix entries being traversed in anti-clockwise fashion
# with each entry being colored red as it's visited
# ANSI escape codes: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
def anti_clockwise(matrix):
  r, c = 0, 0 # current row and column
  direction = 1 # keep track of the current direction (0 = left, 1 = down, 2 = right, 3 = up)
  increments = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)} # increment for each direction
  num_visited = 1 # track number of entries visited
  rows, cols = len(matrix), len(matrix[0]) # number of rows and columns in the matrix
  rows_done, cols_done = 0b0, 0b0 # track the rows/cols traversed using binary (e.g. 0b1001 means that rows 3 and 0 are completed)
                                  # this uses (rows + cols) number of bits (which I thought it was kinda clever, heh...)
  entries_visited = 0b01 # track the entries visited using binary, this uses (rows * cols) number of bits
                         # this is just used for outputting the colored matrix
      
  while num_visited < rows * cols:
    # get the next entry in anti-clockwise order in the current direction
    dr, dc = increments[direction]
    rp, cp = r + dr, c + dc
    # check whether the next entry is in bounds and isn't in a traversed row or column
    if 0 <= rp < rows and 0 <= cp < cols and (1 << rp) & rows_done == 0 and (1 << cp) & cols_done == 0:
      
      # output the matrix
      entries_visited |= 1 << (rp * cols + cp)
      print("\033[H")
      for i in range(rows):
        for j in range(cols):
          if (1 << i * cols + j) & entries_visited != 0:
            print(f"\033[30;41m\033[1m{matrix[i][j]:02} \033[0m", end='')
          else:
            print(f"{matrix[i][j]:02} ", end='')
        print()
      time.sleep(0.02) # 20ms delay
      
      r, c = rp, cp
      num_visited += 1
    else:
      # change direction in anti-clockwise order whenever a wall or completed row/col is reached
      # and update the rows and columns traversed accordingly
      if direction in (1, 3):
        cols_done |= 1 << c
      else:
        rows_done |= 1 << r
      direction = (direction + 1) % 4

if __name__ == "__main__":
  import random, time
  # Generate a random matrix of integers with each entry being in the range [0, 99]
  # Number of rows and columns are random values in the range [2, 20]
  rows, cols = random.randint(2, 20), random.randint(2, 20)
  matrix = []
  for _ in range(rows):
    row = []
    for _ in range(cols):
      row.append(random.randint(0, 99))
    matrix.append(row)
  print("\033[2J")
  anti_clockwise(matrix)