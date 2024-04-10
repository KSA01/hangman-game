
import nltk
from nltk.corpus import stopwords, words, names, wordnet, movie_reviews, reuters, brown, gutenberg, webtext, nps_chat, inaugural
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from textblob import Word as TextWord
import pickle

class WordDifficulty:
    """Estimate the difficulty level of a given English word.

    This class provides methods to estimate the difficulty level of an English word
    based on its usage frequency in various corpora and other linguistic transformations.

    Attributes:
        stopwords (set): A set of common English stopwords.
        words (set): A set of common English words.
        names (set): A set of common names.
        word_freq (dict): A dictionary containing frequency distributions of words in different corpora.
        lemmatizer (WordNetLemmatizer): An instance of WordNetLemmatizer for lemmatization.
    """

    def __init__(self):
        self.load_cached_resources()

    def load_cached_resources(self):
        try:
            with open('nltk_resources.pkl', 'rb') as f:
                cached_data = pickle.load(f)
                self.stopwords = cached_data['stopwords']
                self.words = cached_data['words']
                self.names = cached_data['names']
                self.wordnet_words = cached_data['wordnet_words']
                self.word_freq = cached_data['word_freq']
                self.lemmatizer = cached_data['lemmatizer']
        except FileNotFoundError:
            # Initialize resources if cache file doesn't exist
            self.initialize_resources()

    def initialize_resources(self):
        # Initialization logic for NLTK resources
        self.stopwords = set(stopwords.words('english'))
        self.words = set(words.words())
        self.names = set(names.words())
        self.wordnet_words = set(wordnet.words())
        self.word_freq = {
            "words": FreqDist(words.words()),
            "wordnet_words": FreqDist(wordnet.words()),
            
            "movie_reviews": FreqDist(movie_reviews.words()),
            "reuters": FreqDist(reuters.words()),
            "brown": FreqDist(brown.words()),
            "gutenberg": FreqDist(gutenberg.words()),
            "webtext": FreqDist(webtext.words()),
            "nps_chat": FreqDist(nps_chat.words()),
            "inaugural": FreqDist(inaugural.words()),
        }
        self.lemmatizer = WordNetLemmatizer()
        # Cache the initialized resources
        self.cache_resources()

    def cache_resources(self):
        cached_data = {
            'stopwords': self.stopwords,
            'words': self.words,
            'names': self.names,
            'wordnet_words': self.wordnet_words,
            'word_freq': self.word_freq,
            'lemmatizer': self.lemmatizer
        }
        with open('nltk_resources.pkl', 'wb') as f:
            pickle.dump(cached_data, f)

    def evaluate_word_difficulty(self, word):
        """Estimate the difficulty level of a word.

       Args:
           word (str): The word to evaluate.

       Returns:
           str: The difficulty level of the word, which can be "easy," "moderate," or "difficult."
       """
        word = word.lower()
        base_form = self.to_base_form(word)
        not_slang_form = self.slang_to_normal(word)

        value = self.score_word_difficulty(word)
        sum_eval = value
        if base_form != word:
            value_base = self.score_word_difficulty(base_form)
            if value_base:
                sum_eval = max(sum_eval, value_base) if sum_eval else value_base
        if not_slang_form != word:
            value_base = self.score_word_difficulty(not_slang_form)
            if value_base:
                sum_eval = max(sum_eval, value_base) if sum_eval else value_base
        if sum_eval is None:
            return "unclassified"
        if sum_eval < 30: # Can be adjusted - 0 is hardest limit (20)
            return "Hard"
        if sum_eval < 120: # (110)
            return "Med"
        return "Easy"

    def score_word_difficulty(self, word):
        """Estimate the difficulty of a word based on its usage frequency.

       Args:
           word (str): The word to evaluate.

       Returns:
           int or None: The difficulty score of the word, or None if the word is not found in any corpus.
       """
        word = word.lower()
        if word in self.stopwords:
            return 200  # super easy
        eval_result = self.eval_word(word)
        if not self.is_a_word(word, eval_result):
            return
        sum_eval = sum(eval_result.values())
        return sum_eval

    def eval_word(self, word):
        """Evaluate the word's frequency in various corpora.

        Args:
            word (str): The word to evaluate.

        Returns:
            dict: A dictionary containing the word's frequency in different corpora.
        """
        word = word.lower()
        return {corpus: freq[word] for corpus, freq in self.word_freq.items()}

    def is_a_word(self, word, eval_result=None):
        """Check if a word is a valid English word.

        Args:
            word (str): The word to check.
            eval_result (dict): A pre-evaluated word frequency dictionary (optional).

        Returns:
            bool: True if the word is a valid English word; otherwise, False.
        """
        if any(value in self.stopwords for value in [word, word.title()]):
            return True
        if any(value in self.words for value in [word, word.title()]):
            return True
        if not eval_result:
            eval_result = self.eval_word(word)
        sum_eval = sum(eval_result.values())
        if sum_eval == 0:
            return False
        non_movie_reviews_eval = sum(value for key, value in eval_result.items() if key not in ["movie_reviews"])
        if non_movie_reviews_eval == 0 and word.title() in self.names:
            return False
        return True

    def plural_to_base_form(self, word):
        """Convert a plural noun to its base form.

        Args:
            word (str): The word to convert.

        Returns:
            str: The base form of the word.
        """
        return self.lemmatizer.lemmatize(word.lower(), pos='n')

    def verb_to_present_tense(self, noun):
        """Convert a verb to its present tense form.

        Args:
            noun (str): The verb to convert.

        Returns:
            str: The present tense form of the verb.
            For example: running ==> run.
        """
        word = TextWord(noun.lower())
        return word.lemmatize("v")

    def to_base_form(self, word):
        """Transform a word to its base form using multiple methods.

        Args:
            word (str): The word to transform.

        Returns:
            str: The base form of the word after applying multiple transformations.
        """
        fixed_word = self.plural_to_base_form(word)
        fixed_word = self.verb_to_present_tense(fixed_word)
        return fixed_word

    def slang_to_normal(self, word):
        """Convert slang forms of words into normal forms.

        Args:
            word (str): The word to convert.

        Returns:
            str: The normal form of the word, or the original word if not found in slang.
            For example: flyin ==> flying, runnin ==> running.
        """
        if word.endswith("in") and f"{word}g" in self.words:
            return f"{word}g"
        return word