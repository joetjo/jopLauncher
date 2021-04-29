

class GhGridBehaviour:

    def __init__(self, row, col):
        self.current_row = row
        self.current_col = col

    def row_col_reset(self, col, row):
        self.current_row = row
        self.current_col = col

    # Return current row
    def row(self):
        return self.current_row

    # Return current col
    def col(self):
        return self.current_col

    # Return next row to use and increment row
    def row_next(self):
        self.current_row += 1
        return self.current_row - 1

    # Return next col to use and increment col
    def col_next(self):
        self.current_col += 1
        return self.current_col - 1
