wordgridsolver
==============

A Python solver for word grids (e.g. Scramble, Wordament).

Example usage:

```python
import grid, trie
t = trie.Trie()
t.load_file('dictionary.txt')
g = grid.Grid('acedbrsaetelsard')
g.find_dictionary_words(t)

print 'Found %d words:\n' % (len(g.words))
print sorted(g.words)
```

TODO: Add actual Wordament mode (disable two-letter words).
