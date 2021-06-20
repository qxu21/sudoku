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
        self.assertEqual(len(self.b.grid),81)
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
        self.assertEqual(c1.board,self.b)


    def test_rows(self):
        self.assertEqual(self.b.getRow(0).values(),set(range(0,9)))
        self.assertEqual(self.b.getRow(3).values(),set(range(27,36)))
        self.assertTrue(all([c.row == 3 for c in self.b.getRow(3).cells]))

    def test_boxes(self):
        self.assertEqual(
            self.b.getBox(0).values(),
            {0,1,2,9,10,11,18,19,20})
        self.assertEqual(
            self.b.getBox(4).values(),
            {30,31,32,39,40,41,48,49,50})
        self.assertTrue(all([c.box == 5 for c in self.b.getBox(5).cells]))

    def test_columns(self):
        self.assertEqual(
            self.b.getCol(0).values(),
            {0,9,18,27,36,45,54,63,72})
        self.assertEqual(
            self.b.getCol(4).values(),
            set(range(4,77,9)))
        self.assertTrue(all([c.col == 4 for c in self.b.getCol(4).cells]))

unittest.main()