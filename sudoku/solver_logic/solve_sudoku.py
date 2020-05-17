import math

def in_box(puzzle,i,j,n,size):
    root = int(math.sqrt(size))
    a= i-i%root
    b= j-j%root
    for x in range(root):
        for y in range(root):
            if(n==puzzle[a+x][b+y]):
                return False
    return True

def in_row(puzzle,i,n,size):
    for x in range(size):
        if(n==puzzle[i][x]):
            return False
    return True

def in_col(puzzle,j,n,size):
    for y in range(size):
        if(n==puzzle[y][j]):
            return False
    return True

def allowed(puzzle,i,j,n,size):
    if(in_box(puzzle,i,j,n,size) and in_row(puzzle,i,n,size) and in_col(puzzle,j,n,size)):
        return True
    return False

def print_sudoku(puzzle,size):
    root = int(math.sqrt(size))
    for i in range(size):
        for j in range(size):
            print(puzzle[i][j],end="\t")
            if((j+1)%root==0):
                print(end="\t")
        print(end="\n")
        if((i+1)%root==0):
            print(end="\n")
    #print(arr)
"""if(allowed(2,0,16)):
    print('Yay')
else:
    print('Nay')"""

def is_valid(puzzle,istart,jstart,size):
    if(istart==(size-1) and jstart==(size-1)):
        return True
    for i in range(0,size):
        for j in range(0,size):
            if(puzzle[i][j]>0):
                n,puzzle[i][j]=puzzle[i][j],0
                if(not allowed(puzzle,i,j,n,size)):
                    puzzle[i][j]=n
                    return False
                else:
                	puzzle[i][j]=n
    return True

def put_number(puzzle,istart,jstart,size):
    if(istart==(size-1) and jstart==(size-1)):
        return True
    for i in range(istart,size):
        for j in range(0,size):
            if(puzzle[i][j]==0):
                for n in range(1,(size+1)):
                    if(allowed(puzzle,i,j,n,size)):
                        puzzle[i][j]=n
                        #print(i,j,n)
                        if(put_number(puzzle,i,j,size)):
                            #print(i,j,n)
                            return True
                        else:
                            puzzle[i][j]=0

                return False
    return True

def solve_puzzle(puzzle,size):
    puzzle1 = puzzle
    if(not is_valid(puzzle1,0,0,size)):
        return puzzle1
    if(put_number(puzzle,0,0,size)):
        return puzzle
    else:
        return puzzle1

