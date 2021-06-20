import unittest
import classes

class GroupTestCase(unittest.TestCase):
    def setUp(self):
        pass
        #self.g = classes.Group()

class BoardTestcase(unittest.TestCase):
    def setUp(self):
        self.b = classes.Board(list(range(0,81)))

    def tearDown(self):
        self.b = None

    def test_create_board(self):
        pass

    def test_board(self):
        c1 = self.b.grid[0]
        self.assertEqual(c1.val,0)
        self.assertEqual(c1.row,0)
        self.assertEqual(c1.col,0)
        self.assertEqual(c1.box,0)
        c2 = self.b.grid[35]
        self.assertEqual(c2.val,35)
        self.assertEqual(c2.row,3)
        self.assertEqual(c2.col,8)
        self.assertEqual(c2.box,5)


    def dtest_rows(self):
        self.assertEqual(self.b.getRow(0).have,set(range(0,9)))
        self.assertEqual(self.b.getRow(4).have,set(range(27,36)))

unittest.main()