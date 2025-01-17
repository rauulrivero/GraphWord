import re


class WordFilter:
    def __init__(self, dictionary, min_len=3, max_len=3):
        """
        Initializes the word filter.

        :param dictionary: Dictionary of words to filter.
        :param min_len: Minimum word length.
        :param max_len: Maximum word length.
        """
        self.dictionary = dictionary
        self.min_len = min_len
        self.max_len = max_len

    def filter_words(self):
        """
        Filters words from the dictionary based on length and pronounceability.

        :return: Filtered dictionary.
        """
        return {
            word: value
            for word, value in self.dictionary.items()
            if self._is_valid_word(word)
        }

    def _is_valid_word(self, word):
        """
        Checks if a word is valid according to the established rules.

        :param word: The word to check.
        :return: True if the word is valid, False otherwise.
        """
        # Convert the word to lowercase
        word = word.lower()

        # Check if the word contains only alphabetic characters
        if not word.isalpha():
            return False

        # Check the word length
        if not (self.min_len <= len(word) <= self.max_len):
            return False

        # Check if the word is pronounceable
        if not self._is_pronounceable(word):
            return False

        return True

    def _is_pronounceable(self, word):
        """
        Checks if a word is pronounceable.

        :param word: The word to check.
        :return: True if the word is pronounceable, False otherwise.
        """
        # Reject repetitive sequences of consonants or vowels
        if re.search(r'(.)\1{1,}', word): 
            return False
        
        # Reject words with non-pronounceable sequences (consecutive consonants without vowels)
        if re.search(r'[bcdfghjklmnpqrstvwxyz]{3,}', word): 
            return False

        # Reject words with unnatural vowel sequences
        if re.search(r'[aeiou]{3,}', word): 
            return False

        return True
