import solve_sudoku as solve
import crop_sudoku as crop
import transform_sudoku as transform


size=16
name="sudoku-giant"
ftype="jpeg"

crop.cropImage(name,ftype)

transform = ts.transformImage(name,ftype,size)

"""puzzle=[[10,0,0,0,     0,6,0,8,      0,14,0,2,     0,0,0,0],
        [0,6,0,0,     0,14,0,0,      11,0,0,0,     10,1,2,12],
        [0,0,4,0,     0,16,0,0,      0,9,6,3,     0,0,0,0],
        [11,12,0,14,     4,3,0,1,      0,15,0,5,     0,16,8,0],

        [13,0,0,3,     0,0,1,0,      7,6,0,0,     2,9,5,0],
        [0,5,12,16,     0,10,0,11,      0,0,0,0,     0,0,4,7],
        [0,0,0,2,     0,5,4,16,      3,11,0,0,     14,10,0,0],
        [0,1,10,11,     0,0,2,0,      4,8,0,9,     0,12,0,0],

        [0,7,13,6,     0,2,12,0,      10,0,14,0,     0,3,0,0],
        [2,0,0,15,     0,0,6,7,      16,3,0,0,     9,0,0,13],
        [0,0,1,0,     3,11,0,10,      0,13,15,0,     6,0,7,16],
        [8,0,0,0,     0,0,0,4,      0,0,0,6,     5,0,1,0],

        [4,0,14,13,     10,8,0,6,      9,0,11,0,     12,0,0,2],
        [1,2,0,0,     0,9,11,0,      15,4,13,7,     0,6,0,0],
        [0,0,0,0,     15,7,0,2,      8,0,3,14,     0,0,0,0],
        [0,15,7,0,     0,4,14,0,      0,0,2,0,     11,0,3,9]]
"""

print(puzzle)

solution=solve.solve_puzzle(puzzle,size)

solve.print_sudoku(solution,size)