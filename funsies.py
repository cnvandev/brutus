import fileinput
import re
import sys

def decipher(text, shift):
  ''' Cyclically deciphers the given text using a basic shift cipher. Makes no assumptions as to whether it's the real shift. '''
  string = ""
  for letter in text:
    # Ignore case for the translation, we'll put it back in at the end.
    lower = ord(letter) > ord("Z")
    char_value = ord(letter.upper())

    # If the character is alphanumeric, print its shifted value. Shifting is cyclic, so if we hit "z" we should go back around to A.
    if char_value >= ord("A"):
        new_char_value = char_value - shift

        # If it's less than A, cycle back around by adding the value of the last character to it.
        # If it's greater than z, cycly back ground by subtracting the value of the last character from it.
        if new_char_value < ord("A"):
            new_char_value += ord("Z") - ord("A") + 1
        elif new_char_value > ord("Z"):
            new_char_value -= ord("Z")
        
        string += chr(new_char_value).lower() if lower else chr(new_char_value)
    else:
        string += letter

  return string


def find_shift(dict_words, text):
  ''' Finds the shift that gives the highest number of dictionary words from the supplied list based on the cipher text given. '''
  # Try deciphering the raw text with every letter of the alphabet.
  shift = 0
  word_total = 0
  for test_shift in range(0, 26):
    deciphered_text = decipher(text, test_shift)
    deciphered_words = re.split("\W+", deciphered_text)

    # See how many words we get - this can probably be inlined somehow.
    test_word_total = 0
    for deciphered_word in deciphered_words:
      if deciphered_word in dict_words:
        test_word_total += 1

    if test_word_total > word_total:
      shift = test_shift
      word_total = test_word_total

  return (shift, word_total)


def init_dictionary(word_file):
  ''' Builds a dictionary list of words from the word file indicated. '''
  dict_words = set()
  for x in open(word_file):
    dict_words.add(x.lower().strip())
  return dict_words


# Actual code goes here!
if __name__=="__main__":
  # We'll determine the shift by figuring out which decoding of the message gives us the longest list of English dictionary words.
  dict_words = init_dictionary("/usr/share/dict/words")

  # Loop through the bytes of the message, if we reach the end of the file then break.
  print "Most proble interpretation:"
  print "========================================================="
  total_words = 0
  for cipher_line in fileinput.input():
    (shift, line_words) = find_shift(dict_words, cipher_line)
    final_text = decipher(cipher_line, shift)
    total_words += line_words
    print final_text
  print "\n(%d total matching words)" % total_words