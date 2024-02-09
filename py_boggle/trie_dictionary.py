import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending


class TrieDictionary(BoggleDictionary):
    

    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                # Do something with word here
                current_node = self.root
                for char in word:
                    if char not in current_node.children:
                        current_node.children[char] = TrieNode()
                    current_node = current_node.children[char]
                current_node.is_word = True
        #raise NotImplementedError("method load_dictionary") # TODO: implement your code here

    def traverse(self, prefix: str) -> Optional[TrieNode]:
      
        current_node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node
        #raise NotImplementedError("method traverse") # TODO: implement your code here

    def is_prefix(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None
        #raise NotImplementedError("method is_prefix") # TODO: implement your code here

    def contains(self, word: str) -> bool:
        node = self.traverse(word)
        return node is not None and node.is_word
        #raise NotImplementedError("method contains") # TODO: implement your code here

    def _dfs(self, node, current_word):
        if node.is_word:
            yield current_word
        for char, child_node in node.children.items():
            yield from self._dfs(child_node, current_word + char)

    def __iter__(self) -> typing.Iterator[str]:
        yield from self._dfs(self.root, "")
        #raise NotImplementedError("method __iter__") # TODO: implement your code here

