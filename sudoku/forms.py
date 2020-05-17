from django import forms 
from .models import SudokuImage
  
class SudokuForm(forms.ModelForm): 
  
    class Meta: 
        model = SudokuImage 
        fields = ['sudoku_image'] 
        labels = {
            'sudoku_image': "Select image",
        }
 