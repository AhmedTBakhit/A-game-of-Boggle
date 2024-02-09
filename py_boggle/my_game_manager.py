import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame




SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c])
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """

        if not word:
            return None

        ROWS, COLS = len(self.board), len(self.board[0])
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        def is_valid(x, y, visited):
            return 0 <= x < ROWS and 0 <= y < COLS and (x, y) not in visited

        def dfs(i, j, remaining_word, current_path):
            if not remaining_word:
                return current_path

            if not is_valid(i, j, current_path):
                return None

            if self.board[i][j].lower() == remaining_word[0].lower():
                if len(remaining_word) == 1:
                    return current_path + [(i, j)]
            else:
                return None

            for dx, dy in DIRECTIONS:
                result = dfs(i + dx, j + dy, remaining_word[1:], current_path + [(i, j)])
                if result:
                    return result

            return None

        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j].lower() == word[0].lower():
                    if len(word) == 1:
                        return [(i, j)]  # Directly return if it's a single character word
                    path = dfs(i, j, word, [])
                    if path:
                        return path

        print(f"Exiting find_word_in_board for word {word}")  # Debug print
        return None
        #raise NotImplementedError("method find_word_in_board") # TODO: implement your code here

    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        words_found = set()
        for word in self.dictionary:
            if len(word) >= 4 and self.find_word_in_board(word):
                words_found.add(word)
        return words_found
        #raise NotImplementedError("method dictionary_driven_search") # TODO: implement your code here

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """

        def dfs(i, j, current_word, visited):
            if not (0 <= i < self.size and 0 <= j < self.size):
                return set()
            if (i, j) in visited:
                return set()
            next_word = current_word + self.board[i][j]
            words_found = set()
            if len(next_word) >= 4 and self.dictionary.contains(next_word):
                words_found.add(next_word)
            visited.add((i, j))
            for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                words_found |= dfs(i + x, j + y, next_word, visited)
            visited.remove((i, j))
            return words_found

        found_words = set()
        for i in range(self.size):
            for j in range(self.size):
                found_words |= dfs(i, j, "", set())
        return found_words
        #raise NotImplementedError("method board_driven_search") # TODO: implement your code here
