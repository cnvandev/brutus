import sys

# Cipher decoder for Niantic Project ARG. Wheeee!

if len(sys.argv) < 2:
    print "Must be given a filename with the code text!"
    exit(1)

string = ""
with open(sys.argv[1]) as f:
  # The first three bytes are '+<#> ' where <#> is some value to shift the cipher by.
  shift_string = f.read(3)
  shift = int(shift_string)

  # Loop through the bytes of the message, if we reach the end of the file then break.
  while True:
    c = f.read(1)
    if not c:
      break #EOF!

    # Ignore case for the translation, we'll put it back in at the end.
    lower = ord(c) > ord("Z")
    char_value = ord(c.upper())

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
        string += c

print string