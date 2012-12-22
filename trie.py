# naive trie implementation using python dictionary lookups

class Node(object):
    def __init__(self):
        self.letters = {}
        self.is_word = False

    # adds letter
    # returns Node (create if necessary)
    def add_letter(self, letter):
        if letter in self.letters:
            return self.letters[letter]
        self.letters[letter] = Node()
        return self.letters[letter]

class Trie(object):
    def __init__(self):
        self.root = Node()

    def load_word(self, word):
        curRef = self.root
        
        # traverse through links
        for letter in word:
            curRef = curRef.add_letter(letter)

        # mark end Node as a word
        curRef.is_word = True

    # load file of words, each on new line
    def load_file(self, file_name):
        f = open(file_name)
        for line in f.readlines():
            word = line.strip()
            self.load_word(word)
        f.close()

    def print_recursive(self, node, prefix):
        # base case: empty dict
        if node.letters == {}:
            print prefix
            return
        
        if node.is_word:
            print prefix

        # traverse nodes of sorted keys
        sortedKeys = sorted(node.letters.keys())
        for letter in sortedKeys:
            self.print_recursive(node.letters[letter], prefix+letter)

    # wrapper around print_recursive
    def print_words(self):
        self.print_recursive(self.root, '')

    # checks for word existence in trie
    def has_word(self, word):
        curRef = self.root
        for letter in word:
            if letter in curRef.letters:
                curRef = curRef.letters[letter]
            else:
                return False
        return True
            
def main():
    print "Loading dictionary file..."
    t = Trie()
    t.load_file('dictionary.txt')
    print "Dictionary loaded.\n"

    print 'hello in trie: ', t.has_word('hello')
    print 'blah in trie: ', t.has_word('blah')
    print 'goodbye in trie: ', t.has_word('goodbye')
    print 'asdf in trie: ', t.has_word('asdf')

if __name__ == '__main__':
    main()
