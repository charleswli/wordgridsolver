# implements a word grid solver
# TODO: factor out navigation code into constant adjacency matrix
import trie
import re
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

    def __init__(self, tiles='abcdefghijklmnop'):
        self.tiles = []
        self.grid = []

        # regular expression to match letters or parenthesized groups
        r = re.compile(r'[a-z]|[(][a-z]+[)]', re.IGNORECASE)
        for tile in r.findall(tiles):
            self.tiles.append(tile.strip('(').strip(')'))

        # init with first 16 letters
        #  TODO: fix mixing magic number use
        for i in range(Grid.SIZE):
            self.grid.append([])
            for j in range(Grid.SIZE):
                self.grid[i].append(self.tiles[i*Grid.SIZE + j])

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
      
        # check if trie path exists for each valid step
        for step in valid_steps:
            k, l = step
            tile = self.grid[k][l]
            if len(tile) > 1:
                curNode = node
                for letter in tile:
                    if letter in curNode.letters.keys():
                        curNode = curNode.letters[letter]
                    else:
                        return
                self.suffix_from_point(curNode, valid_points[:], (k,l), prefix+tile)
            else:
                if tile in node.letters.keys():
                    self.suffix_from_point(node.letters[tile], valid_points[:], (k,l), prefix+tile)

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
                letter = self.grid[i][j]
                if letter in loaded_trie.root.letters:
                    self.suffix_from_point(loaded_trie.root.letters[letter], valid_points[:], (i,j), self.grid[i][j])

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
    print 'Found %d words in %ss ' % (len(g.words), end-start)

    print 'Finding words in grid:\nvnmi\nteas\nspr(qu)\neknt\n'
    start = time.time()
    g = Grid('vnmiteasspr(qu)eknt')
    g.find_dictionary_words(t)
    end = time.time()
    #print sorted(g.words)
    print 'Found %d words in %ss ' % (len(g.words), end-start)
                    
if __name__ == '__main__':
    main()
