"""
Tests for l1sudoku.
"""

import unittest
from sudoku import Problem, eye, ones_v, solve_plain_l1
from random import choice, randint
from cvxopt.base import matrix
import itertools, operator

TOP95 = """
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....
....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...
......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3.
6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6.....
.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........
6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
.923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9.....
6..3.2....5.....1..........7.26............543.........8.15........4.2........7..
.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...
..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..
3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....
1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......
6..3.2....4.....1..........7.26............543.........8.15........4.2........7..
....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.
45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......
..84...3....3.....9....157479...8........7..514.....2...9.6...2.5....4......9..56
.98.1....2......6.............3.2.5..84.........6.........4.8.93..5...........1..
..247..58..............1.4.....2...9528.9.4....9...1.........3.3....75..685..2...
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.9......
.2.3......63.....58.......15....9.3....7........1....8.879..26......6.7...6..7..4
1.....7.9.4...72..8.........7..1..6.3.......5.6..4..2.........8..53...7.7.2....46
4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......
.......71.2.8........4.3...7...6..5....2..3..9........6...7.....8....4......5....
6..3.2....4.....8..........7.26............543.........8.15........8.2........7..
.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.
......8.17..2........5.6......7...5..1....3...8.......5......2..4..8....6...3....
38.6.......9.......2..3.51......5....3..1..6....4......17.5..8.......9.......7.32
...5...........5.697.....2...48.2...25.1...3..8..3.........4.7..13.5..9..2...31..
.2.......3.5.62..9.68...3...5..........64.8.2..47..9....3.....1.....6...17.43....
.8..4....3......1........2...5...4.69..1..8..2...........3.9....6....5.....2.....
..8.9.1...6.5...2......6....3.1.7.5.........9..4...3...5....2...7...3.8.2..7....4
4.....5.8.3..........7......2.....6.....5.8......1.......6.3.7.5..2.....1.8......
1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......
1....6.8..64..........4...7....9.6...7.4..5..5...7.1...5....32.3....8...4........
249.6...3.3....2..8.......5.....6......2......1..4.82..9.5..7....4.....1.7...3...
...8....9.873...4.6..7.......85..97...........43..75.......3....3...145.4....2..1
...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....
......8.16..2........7.5......6...2..1....3...8.......2......7..3..8....5...4....
.476...5.8.3.....2.....9......8.5..6...1.....6.24......78...51...6....4..9...4..7
.....7.95.....1...86..2.....2..73..85......6...3..49..3.5...41724................
.4.5.....8...9..3..76.2.....146..........9..7.....36....1..4.5..6......3..71..2..
.834.........7..5...........4.1.8..........27...3.....2.6.5....5.....8........1..
..9.....3.....9...7.....5.6..65..4.....3......28......3..75.6..6...........12.3.8
.26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4
2.3.8....8..7...........1...6.5.7...4......3....1............82.5....6...1.......
6..3.2....1.....5..........7.26............843.........8.15........8.2........7..
1.....9...64..1.7..7..4.......3.....3.89..5....7....2.....6.7.9.....4.1....129.3.
.........9......84.623...5....6...453...1...6...9...7....1.....4.5..2....3.8....9
.2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5
9.4..5...25.6..1..31......8.7...9...4..26......147....7.......2...3..8.6.4.....9.
...52.....9...3..4......7...1.....4..8..453..6...1...87.2........8....32.4..8..1.
53..2.9...24.3..5...9..........1.827...7.........981.............64....91.2.5.43.
1....786...7..8.1.8..2....9........24...1......9..5...6.8..........5.9.......93.4
....5...11......7..6.....8......4.....9.1.3.....596.2..8..62..7..7......3.5.7.2..
.47.2....8....1....3....9.2.....5...6..81..5.....4.....7....3.4...9...1.4..27.8..
......94.....9...53....5.7..8.4..1..463...........7.8.8..7.....7......28.5.26....
.2......6....41.....78....1......7....37.....6..412....1..74..5..8.5..7......39..
1.....3.8.6.4..............2.3.1...........758.........7.5...6.....8.2...4.......
2....1.9..1..3.7..9..8...2.......85..6.4.........7...3.2.3...6....5.....1.9...2.5
..7..8.....6.2.3...3......9.1..5..6.....1.....7.9....2........4.83..4...26....51.
...36....85.......9.4..8........68.........17..9..45...1.5...6.4....9..2.....3...
34.6.......7.......2..8.57......5....7..1..2....4......36.2..1.......9.......7.82
......4.18..2........6.7......8...6..4....3...1.......6......2..5..1....7...3....
.4..5..67...1...4....2.....1..8..3........2...6...........4..5.3.....8..2........
.......4...2..4..1.7..5..9...3..7....4..6....6..1..8...2....1..85.9...6.....8...3
8..7....4.5....6............3.97...8....43..5....2.9....6......2...6...7.71..83.2
.8...4.5....7..3............1..85...6.....2......4....3.26............417........
....7..8...6...5...2...3.61.1...7..2..8..534.2..9.......2......58...6.3.4...1....
......8.16..2........7.5......6...2..1....3...8.......2......7..4..8....5...3....
.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.
.52..68.......7.2.......6....48..9..2..41......1.....8..61..38.....9...63..6..1.9
....1.78.5....9..........4..2..........6....3.74.8.........3..2.8..4..1.6..5.....
1.......3.6.3..7...7...5..121.7...9...7........8.1..2....8.64....9.2..6....4.....
4...7.1....19.46.5.....1......7....2..2.3....847..6....14...8.6.2....3..6...9....
......8.17..2........5.6......7...5..1....3...8.......5......2..3..8....6...4....
963......1....8......2.5....4.8......1....7......3..257......3...9.2.4.7......9..
15.3......7..4.2....4.72.....8.........9..1.8.1..8.79......38...........6....7423
..........5724...98....947...9..3...5..9..12...3.1.9...6....25....56.....7......6
....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........
6.....7.3.4.8.................5.4.8.7..2.....1.3.......2.....5.....7.9......1....
....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1..
.32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6.
...5.3.......6.7..5.8....1636..2.......4.1.......3...567....2.8..4.7.......2..5..
.5.3.7.4.1.........3.......5.8.3.61....8..5.9.6..1........4...6...6927....2...9..
..5..8..18......9.......78....4.....64....9......53..2.6.........138..5....9.714.
..........72.6.1....51...82.8...13..4.........37.9..1.....238..5.4..9.........79.
...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..
.2.3.......6..8.9.83.5........2...8.7.9..5........6..4.......1...1...4.22..7..8.9
.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.
.....2.......7...17..3...9.8..7......2.89.6...13..6....9..5.824.....891..........
3...8.......7....51..............36...2..4....7...........6.13..452...........8..
"""


def puzzles():
    """
    Pick one of the TOP95 puzzle strings
    """
    return [l for l in TOP95.split("\n") if l]

def random_puzzle():
    """
    Pick one of the TOP95 puzzle strings
    """
    return choice(puzzles())

def all_ones(vector):
    """
    Return True/False if all vector's entries are/are not
    1s.
    """
    return all([e==1 for e in vector])

def make_problem(char, pos, N=9):
    """
    Make a test problem with a single entry.
    """
    N2 = N**2
    s = "."*pos + char + "."*(N2-pos-1)
    return Problem(s)

class ProblemTest(unittest.TestCase):
    """
    Tests for l1sudoku Problem class
    """
    def setUp(self):
        """
        Instantiate one Problem at random from TOP95
        """
        self.sudoku = Problem(random_puzzle())
        self.N = 9
    
    def test_puzzle(self):
        """
        Test we create a Problem correctly from a string
        """
        print unicode(self.sudoku)
        self.assertEqual(self.N, self.sudoku.N)
        self.assertTrue(len(unicode(self.sudoku)) > self.sudoku.N **2)

    def test_box_size(self):
        """
        Test we get correct boxsize if N is square and large enough.
        """
        self.assertEqual(3, Problem("."*81,N=9).get_box_size())
        self.assertEqual(2, Problem("."*16,N=4).get_box_size())
        self.assertEqual(0, Problem("."*4,N=2).get_box_size())
        self.assertEqual(0, Problem("."*100,N=10).get_box_size())

    def test_nentries(self):
        """
        Check the Problem correctly counts the number
        of clue entries.        
        """
        sudoku = Problem('1' + '.'*(self.N **2 -1), N=self.N)
        self.assertEqual(1, sudoku.num_entries())
        
        rp = random_puzzle().strip()
        nentries_rp = len([e for e in rp if e != '.'])
        sudoku = Problem(rp)
        self.assertEqual(nentries_rp, sudoku.num_entries())
        
    def test_matrix(self):
        """
        Test the problem matrix generated by the Problem
        """
        m = self.sudoku.matrix()
        self.assertTrue(isinstance(m ,matrix ))
        
        nentries = len([e for e in self.sudoku.entries if e])
        N = self.sudoku.N
        self.assertEqual((4 * N**2 + nentries, N**3), m.size)                
        
    def test_to_indicator(self):
        """
        Test the problem matrix generated by the Problem
        """
        N = self.N
        num = randint(1,N)
        pos = randint(0,N**2-1)
        sudoku = make_problem(chr(ord('0') + num), pos)
        
        iv = sudoku.to_indicator_vector()
        self.assertTrue(isinstance(iv ,matrix ))
        self.assertEqual((N**3,1), iv.size)
        self.assertEqual(1, sum(iv))
        self.assertEqual(N*pos+num-1, list(iv).index(1))

        s2 = Problem.from_indicator_vector(iv)
        
        self.assertEqual(unicode(sudoku),unicode(s2))

    def test_all_cells_constraint(self):
        """
        Check the matrix constraint that ensures
        all cells are filled.
        """
        # - Construct a Problem with all cells filled
        # - Get the all_cells matrix
        # - Multiply it with the indicator vector
        # - check the result is all ones
        # - blank a cell, repeat
        # - check the result is not all ones
        N = self.N
        sudoku = Problem("1"*N**2)
        v = sudoku.get_result(all_cells=True)
        self.assertOnes(v)
        v = self.sudoku.get_result(all_cells=True)
        self.assertNotOnes(v)

    def test_row_digits_constraint(self):
        """
        Check the matrix constraint that ensures
        each row contains all digits
        """
        # - Construct a Problem with all cells filled
        # - Get the all_cells matrix
        # - Multiply it with the indicator vector
        # - check the result is all ones
        # - blank a cell, repeat
        # - check the result is not all ones
        N = 9
        sudoku = Problem("123456789"*N)
        v = sudoku.get_result(row_digits=True)
        self.assertOnes(v)
        v = self.sudoku.get_result(row_digits=True)
        self.assertNotOnes(v)

    def test_col_digits_constraint(self):
        """
        Check the matrix constraint that ensures
        each row contains all digits
        """
        # - Construct a Problem with all cells filled
        # - Get the all_cells matrix
        # - Multiply it with the indicator vector
        # - check the result is all ones
        # - blank a cell, repeat
        # - check the result is not all ones
        N = 9

        entries = reduce(operator.__add__,
                         [list(itertools.repeat(i,N)) for  i in range(1,N+1)])
        sudoku = Problem(entries)        
        v = sudoku.get_result(col_digits=True)
        self.assertOnes(v)
        v = self.sudoku.get_result(col_digits=True)
        self.assertNotOnes(v)

    def test_box_digits_constraint(self):
        """
        Check the matrix constraint that ensures
        each box contains all digits
        """
        # - Construct a Problem with all cells filled
        # - Get the all_cells matrix
        # - Multiply it with the indicator vector
        # - check the result is all ones
        # - blank a cell, repeat
        # - check the result is not all ones
        N = 9
        sudoku = Problem("123123123"
                         "456456456"
                         "789789789"
                         "123123123"
                         "456456456"
                         "789789789"
                         "123123123"
                         "456456456"
                         "789789789")
        v = sudoku.get_result(box_digits=True)
        self.assertOnes(v)
        v = self.sudoku.get_result(box_digits=True)
        self.assertNotOnes(v)


    def test_clues_constraint(self):
        """
        Check the matrix constraint that ensures
        the answer is consistent with the clues.
        """
        N = 9
        num = randint(1,N)
        pos = randint(0,N**2-1)
        sudoku = make_problem(chr(ord('0') + num), pos)

        v = sudoku.get_result(clues=True)
        self.assertOnes(v)

    def assertOnes(self, vector):
        """
        Assert the vector consists entirely of ones.
        """
        self.assertTrue(all_ones(vector))

    def assertNotOnes(self, vector):
        """
        Assert the vector does not consist entirely of ones.
        """
        self.assertFalse(all([e==1 for e in vector]))
        
    def test_solve(self):
        """
        Test solving the Problem.
        """
        # Easy test
        self.sudoku = Problem('.81.749....4.193.7379.85.14..7831...238456179..69274..843562791762198543..5743862')
        answer = self.sudoku.solve()
        checkAnswer = Problem('681374925524619387379285614497831256238456179156927438843562791762198543915743862')
        
        self.assertEqual(unicode(checkAnswer), unicode(answer) )

        answer = self.sudoku.solve()
        checkAnswer = Problem('681374925524619387379285614497831256238456179156927438843562791762198543915743862')
        
        self.assertEqual(unicode(checkAnswer), unicode(answer) )

    def test_solve_plainl1(self):
        """
        Test the solve_min function.
        """
        
        M = matrix([1,1,1,1,0,1],(2,3),'d')
        b = ones_v(2)
        x = solve_plain_l1(M, b)
        self.assertEqual(tuple(b), tuple(M*x))

         
def count_success():
    results = {}
    for p in puzzles():
        results[p] = not '_' in unicode(Problem(p).solve())

    print "OK: %d" % results.values().count(True)
    print "Fail: %d" % results.values().count(False)
    return results
