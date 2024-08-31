from flask import Flask, request, render_template, redirect
import os
from readImage import get_grid
from solver import sudokuBoard
from copy import deepcopy

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    print(request)
    
    if 'sudoku_image' not in request.files:
        return redirect('/')
    
    file = request.files['sudoku_image']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        grid = get_grid(file_path)
        os.remove(file_path)
        to_solve = sudokuBoard(deepcopy(grid))

        if to_solve.solve():
            return render_template('solution.html', solutionBoard=to_solve.get_board(), originalBoard=grid)
        else:
            return render_template('nosolution.html')
        
if __name__ == '__main__':
    app.run(debug=True)