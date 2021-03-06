#!/usr/local/bin/python
def u_converter( string = "\u5982\u679c\u7231" ):
    """
    Simple handler for converting a str type string with pure unicode
    code point (that is it has '\u' in string but no 'u' prefix) to
    an unicode type string.

    Actually, this method has the same effect with 'u' prefix. But differently,
    it allows you to pass a variable of code points string as well as a constant
    one.
    """
    chars = string.split("\u")
    chinese = ''
    for char in chars:
        if len(char):
            try:
                ncode = int(char,16)
            except ValueError:
                continue
            try:
                uchar = unichr(ncode)
            except ValueError:
                continue
            chinese += uchar
    return chinese
if __name__ == "__main__":
    import sys
    pure_string = sys.argv[1]
    print u_converter(pure_string)
