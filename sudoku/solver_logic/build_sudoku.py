from . import crop_sudoku as crop
from . import transform_sudoku as transform


def buildSudoku(base,name,ftype):
        size=9

        crop.cropImage(base,name,ftype)
        return(transform.transformImage(base,name,ftype,size))