

class GhGridBehaviour:

    def __init__(self, row, col):
        self.current_row = row
        self.current_col = col

    def row_col_reset(self, row = 0, col = 0):
        self.current_row = row
        self.current_col = col

    # return current and reset value to row
    def row_reset(self,  row = 0):
        current = self.current_row
        self.current_row = row
        return current

    # return current and reset value to col
    def col_reset(self,  col = 0):
        current = self.current_col
        self.current_col = col
        return current

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
