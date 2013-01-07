# implements a word grid solver
# TODO: factor out navigation code into constant adjacency matrix
import trie
import time

class Grid(object):
    SIZE = 4

    ADJACENT_POINTS = {(0,0):[(0,1),(1,0),(1,1)],
                       (0,1):[(0,0),(0,2),(1,0),(1,1),(1,2)],
                       (0,2):[(0,1),(0,3),(1,1),(1,2),(1,3)],
                       (0,3):[(0,2),(1,2),(1,3)],
                       (1,0):[(0,0),(0,1),(1,1),(2,0),(2,1)],
                       (1,1):[(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)],
                       (1,2):[(0,1),(0,2),(0,3),(1,1),(1,3),(2,1),(2,2),(2,3)],
                       (1,3):[(0,2),(0,3),(1,2),(2,2),(2,3)],
                       (2,0):[(1,0),(1,1),(2,1),(3,0),(3,1)],
                       (2,1):[(1,0),(1,1),(2,2),(2,0),(2,2),(3,0),(3,1),(3,2)],
                       (2,2):[(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3)],
                       (2,3):[(1,2),(1,3),(2,2),(3,2),(3,3)],
                       (3,0):[(2,0),(2,1),(3,1)],
                       (3,1):[(2,0),(2,1),(2,2),(3,0),(3,2)],
                       (3,2):[(2,1),(2,2),(2,3),(3,1),(3,3)],
                       (3,3):[(2,2),(2,3),(3,2)]}

    def __init__(self, letters='abcdefghijklmnop'):
        self.letters = letters
        self.grid = []

        # init with first 16 letters
        #  TODO: fix mixing magic number use
        for i in range(Grid.SIZE):
            self.grid.append(letters[i*Grid.SIZE:(i+1)*Grid.SIZE])
        
        self.words = []

    # recursively explore valid neighboring points from current point
    def suffix_from_point(self, node, valid_points, start_point, prefix):
        # base case
        if node.is_word:
            self.words.append(prefix)

        # ensure we don't step in same square twice
        valid_points.remove(start_point)

        # list possible steps to take
        valid_steps = []
        for point in self.ADJACENT_POINTS[start_point]:
            if point in valid_points:
                valid_steps.append(point)
        i, j = start_point
      
        # check if trie path exists for each valid step
        for step in valid_steps:
            k, l = step
            letter = self.grid[k][l]
            if letter in node.letters.keys():
                self.suffix_from_point(node.letters[letter], valid_points[:], (k,l), prefix+letter)

    # find words in grid that exist in given trie
    def find_dictionary_words(self, loaded_trie):
        # list valid points
        valid_points = []
        for i in xrange(Grid.SIZE):
            for j in xrange(Grid.SIZE):
                valid_points.append((i,j))
        
        # iterate through valid starting points and take steps
        for i in xrange(Grid.SIZE):
            for j in xrange(Grid.SIZE):

                # take steps
                self.suffix_from_point(loaded_trie.root, valid_points[:], (i,j), '')

        #remove duplicates
        self.words = sorted(list(set(self.words)))

def main():
    print 'Loading dictionary into trie...'
    start = time.time()
    t = trie.Trie()
    t.load_file('dictionary.txt')
    end = time.time()
    print "Loaded dictionary in %ss\n" % (end-start)

    print 'Finding words in grid:\naced\nbrsa\netel\nsard\n'
    start = time.time()
    g = Grid('acedbrsaetelsard')
    g.find_dictionary_words(t)
    end = time.time()
    #print sorted(g.words)
    print 'Found %d words in %ss ' % (len(g.words), end-start)
                    
if __name__ == '__main__':
    main()
