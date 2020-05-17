from django.db import models

# Create your models here.
class SudokuImage(models.Model): 
    sudoku_image = models.ImageField(upload_to='',blank=True) 
