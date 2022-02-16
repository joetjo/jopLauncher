# Copyright 2022 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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

    def debug(self, ctx):
        print("{} : {}, {}".format(ctx, self.row(), self.col()))
