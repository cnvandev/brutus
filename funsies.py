import re
import sys

''' Cyclically deciphers the given text using a basic shift cipher. Makes no assumptions as to whether it's the real shift. '''
def decipher(text, shift):
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


''' Finds the shift that gives the highest number of dictionary words from the supplied list based on the cipher text given. '''
def find_shift(dict_words, text):
  # Try deciphering the raw text with every letter of the alphabet.
  shift = 0
  word_total = 0
  for test_shift in range(0, 26):
    deciphered_text = decipher(cipher_text, test_shift)
    deciphered_words = re.split("\W+", deciphered_text)

    # See how many words we get - this can probably be inlined somehow.
    test_word_total = 0
    for deciphered_word in deciphered_words:
      if deciphered_word in dict_words:
        test_word_total += 1

    if test_word_total > word_total:
      shift = test_shift
      word_total = test_word_total
      print "New probable shift: \"%d\" with %d dictionary words in interpretation." % (shift, word_total)

  return shift


''' Builds a dictionary list of words from the word file indicated. '''
def init_dictionary(word_file):
  dict_words = []
  for x in open(word_file):
    dict_words.append(x.lower().strip())
  return dict_words


# Actual code goes here!
if __name__=="__main__":
  # We'll determine the shift by figuring out which decoding of the message gives us the longest list of English dictionary words.
  dict_words = init_dictionary("/usr/share/dict/words")

  if len(sys.argv) < 2:
      print "Must be given a filename with the code text!"
      exit(1)

  with open(sys.argv[1]) as f:
    cipher_text = ""

    # Loop through the bytes of the message, if we reach the end of the file then break.
    while True:
      c = f.read(1)
      if not c:
        break #EOF!
      cipher_text += c

    shift = find_shift(dict_words, cipher_text)
    print "Most proble interpretation:\n=========================================================\n\n", decipher(cipher_text, shift)