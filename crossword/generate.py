import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            remove = []
            for word in self.domains[variable]:
                if len(word) != variable.length:
                    remove.append(word)

            for word in remove:
                self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        revision = False

        if overlap:
            xover, yover = overlap
            remove = []

            for i in self.domains[x]:
                possible = False
                for j in self.domains[y]:
                    if i[xover] == j[yover] and i != j:
                        possible = True
                        break
                if possible == False:
                    remove.append(i)

            for a in remove:
                self.domains[x].remove(a)
            if remove:
                revision = True
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if arcs == None:
            for a in self.crossword.variables:
                for b in self.crossword.neighbors(a):
                    queue.append((a, b))
        else:
            queue = arcs

        while len(queue) > 0:
            x, y = queue.pop(0)
            if self.revise(x, y) == True:
                if len(self.domains[x]) == 0:
                    return False
                for n in self.crossword.neighbors(x):
                    if n != y:
                        queue.append((n, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.domains:
            if v not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for vx, wx in assignment.items():
            if vx.length != len(wx):
                return False

            for vy, wy in assignment.items():
                if vx != vy:
                    if wx == wy:
                        return False

                    overlaps = self.crossword.overlaps[vx, vy]
                    if overlaps:
                        if len(overlaps) == 1:
                            x, y = overlaps
                            if wx[x] != wy[y]:
                                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbours = []
        for n in self.crossword.neighbors(var):
            if n in assignment:
                continue
            else:
                neighbours.append(n)

        result = []
        for option in self.domains[var]:
            ruledOut = 0

            for n in neighbours:
                for noption in self.domains[n]:
                    overlaps = self.crossword.overlaps[var, n]
                    if len(overlaps) == 1:
                        x, y = overlaps
                        if option[x] != noption[y]:
                            ruledOut += 1
            result.append((option, ruledOut))
        result.sort(reverse = True, key = lambda x: x[1])
        final = []
        for r in result:
            final.append(r[0])
            
        return final
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var = []
        for v in self.crossword.variables:
            if v not in assignment:
                var.append(v)
        sort = []
        for v in var:
            domainlength = len(self.domains[v])
            numneighbours = len(self.crossword.neighbors(v))
            sort.append((v, domainlength, numneighbours))
        sort.sort(reverse = True, key = lambda x: x[2])
        sort.sort(key = lambda x: x[1])
        
        return sort[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        else:
            selvar = self.select_unassigned_variable(assignment)
            for v in self.order_domain_values(selvar, assignment):
                assignment[selvar] = v

                if self.consistent(assignment):
                    result = self.backtrack(assignment)
                    if result != None:
                        return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
