from django.shortcuts import render, redirect
from django.http import HttpResponse
from .solver_logic import build_sudoku as build
from .solver_logic import solve_sudoku as solves
from .forms import SudokuForm
from django.contrib import messages
from django.conf import settings 
import random
import string


# Create your views here.
def index(request):
    state = "start"
    sudoku = []
    unsolved_sudoku = []
    image_form = SudokuForm()
    display_image = False
    user_image = ""
    form_x = ""
    if(request.method == 'POST'):
        state = "edit"
        if("solve_sudoku" in request.POST):
            if("user_image" in request.POST):
                user_image = request.POST["user_image"]
                display_image = True
            sudoku = [request.POST[x] for x in request.POST]
            sudoku.pop(0)
            for x in range(9):
                insud = []
                for y in range(9):
                    if(sudoku[0]==""):
                        insud.append(0)
                    else:
                        insud.append(int(sudoku[0]))
                    sudoku.pop(0)
                sudoku.append(insud)
            sudoku.pop(0)
            if("user_image" in request.POST):
                sudoku.pop(0)

            empty_sudoku = [[0 for x in range(9)] for y  in range(9)]
            if(sudoku==empty_sudoku):
                messages.warning(request, "You can't pass an empty sudoku!")
            else:
                state = "solve"
                unsolved_sudoku = [[x for x in y] for y in sudoku]
                solves.solve_puzzle(sudoku,9)
                form_x = (unsolved_sudoku,sudoku)
                if(sudoku==unsolved_sudoku):
                    messages.error(request, "This sudoku is unsolvable. Please make sure it is a valid sudoku and no mistake has been made in copying!")
                else:
                    messages.success(request, "Sudoku solved successfully!")
                    messages.info(request, "If the original sudoku was sparse then multiple answers were possible. The first one has been shown.")

        elif("sudoku_image" in request.FILES):
            form = SudokuForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                fname,ext = form.instance.__getattribute__("sudoku_image").name.split(".")
                sudoku = build.buildSudoku(settings.MEDIA_ROOT,fname,ext)
                display_image = True
                user_image = "media/"+form.instance.__getattribute__("sudoku_image").name
                messages.info(request, "If the differences between the two sudokus is high then you can re-upload with better lightning/flatter surface. Please ensure that the sudoku is the largest object in your image.")
            else:
                for error in form.errors['sudoku_image']:
                    state = "start"
                    messages.warning(request, error)
    context = {
        'sudoku' : sudoku,
        'unsolved_sudoku' : unsolved_sudoku,
        'image' : image_form,
        'range' : range(9),
        "display_image": display_image,
        "user_image" : user_image,
        'form_x': form_x,
        'state' : state
    }
    return render(request, 'sudoku/index.html',context)