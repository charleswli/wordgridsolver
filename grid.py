# implements a word grid solver
# TODO: factor out navigation code into constant adjacency matrix
import trie
import time

class Grid(object):
    SIZE = 4

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
        i, j = start_point

        # up 
        if i > 0:
            if (i-1,j) in valid_points:
                valid_steps.append((i-1, j))
            # up-left
            if j > 0 and (i-1,j-1) in valid_points:
                valid_steps.append((i-1, j-1))

            # up-right
            if j < (Grid.SIZE-1) and (i-1,j+1) in valid_points:
                valid_steps.append((i-1, j+1))

        # down
        if i < (Grid.SIZE-1):
            if (i+1,j) in valid_points:
                valid_steps.append((i+1, j))
            # down-left
            if j > 0 and (i+1,j-1) in valid_points:
                valid_steps.append((i+1, j-1))
            # down-right
            if j < (Grid.SIZE-1) and (i+1,j+1) in valid_points:
                valid_steps.append((i+1, j+1))

        # left
        if j > 0:
            if (i,j-1) in valid_points:
                valid_steps.append((i, j-1))
        # right
        if j < (Grid.SIZE-1):
            if (i,j+1) in valid_points:
                valid_steps.append((i, j+1))
        
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
