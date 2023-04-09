# Problem Set 4B
# Name: Marcos Ortiz
# Collaborators: none
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        shift_dict = {}
        lowers = string.ascii_lowercase
        uppers = string.ascii_uppercase
        for i in range(26):
            shift_dict[lowers[i]]=lowers[(i+shift)%26]
            shift_dict[uppers[i]]=uppers[(i+shift)%26]
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        shifted_message = ''
        for char in self.message_text:
            if char in shift_dict:
                shifted_message += shift_dict[char]
            else:
                shifted_message += char
        return shifted_message

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return dict(self.encryption_dict)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        # valid_count[i] is the number of valid words that appear
        # in the message after a shift by i
        valid_count = []

        # best_yet is the largest count of valid words found after a shift
        best_yet = 0
        # Test every possbile shift
        for test_shift in range(26):
            # Reset the count of valids found
            valids_found = 0

            # Apply the shift
            shifted_message = self.apply_shift(test_shift)

            # Count the valid words that appear in the shift message
            # by checking whether the substrings that appear between
            # non-alphabet characters are valid words
            potential_word = ''

            for char in shifted_message:

                if char in string.ascii_letters:
                    potential_word += char
                elif is_word(self.valid_words, potential_word):
                    valids_found +=1
                    potential_word = ''
                if char not in string.ascii_letters:
                    potential_word = ''

            if potential_word and is_word(self.valid_words, potential_word):
                valids_found +=1

            valid_count.append(valids_found)

            best_yet = max(valids_found, best_yet)

        most_valid_shift = valid_count.index(best_yet)

        return (most_valid_shift, self.apply_shift(most_valid_shift))


if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    plainTest1 = PlaintextMessage('hello wonder bump upside down bxlp', 2)
    print('Expected Output: jgnnq yqpfgt dwor wrukfg fqyp dznr')
    print('Actual Output  :', plainTest1.get_message_text_encrypted())
    cipherTest1 = CiphertextMessage('jgnnq yqpfgt dwor wrukfg fqyp dznr')
    print('Expected Output:', (24, 'hello wonder bump upside down bxlp'))
    print('Actual Output  :', cipherTest1.decrypt_message())

    plainTest2 = PlaintextMessage('wonder if this will work as expected', 7)
    print('Expected Output: dvukly pm aopz dpss dvyr hz lewljalk')
    print('Actual Output  :', plainTest2.get_message_text_encrypted())
    cipherTest2 = CiphertextMessage('dvukly pm aopz dpss dvyr hz lewljalk')
    print('Expected Output:', (19, 'wonder if this will work as expected'))
    print('Actual Output  :', cipherTest2.decrypt_message())

    plainTest3 = PlaintextMessage('wonder if this will work as expected', 11)
    print('Expected Output: hzyopc tq estd htww hzcv ld piapnepo')
    print('Actual Output  :', plainTest3.get_message_text_encrypted())
    cipherTest3 = CiphertextMessage('hzyopc tq estd htww hzcv ld piapnepo')
    print('Expected Output:', (15, 'wonder if this will work as expected'))
    print('Actual Output  :', cipherTest3.decrypt_message())

    # Plaintext "wonder if this will work as expected" was encrypted in parts
    # with 'wonder if this' shifted by 7 and 'will work as expected' shifted by
    # 11. Result: 'dvukly pm aopz will work as expected'
    cipherTest4 = CiphertextMessage('dvukly pm aopz htww hzcv ld piapnepo')
    print('Expected Output:', (15, 'skjzan eb pdeo will work as expected'))
    print('Actual Output  :', cipherTest4.decrypt_message())
    #TODO: best shift value and unencrypted story

    pass #delete this line and replace with your code here
