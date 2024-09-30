import re
import string

#######################################################################################################################
# REMOVE #
#######################################################################################################################

def Remove_Substring_From_String(String: str, Substring_To_Remove: str, Times: str | int = 'All') -> str:
    
    """
    Remove a specified substring from a string a given number of times.

    Parameters:
    - String (str): The original string from which to remove the substring.
    - Substring_To_Remove (str): The substring to be removed.
    - Times (str | int): The number of times to remove the substring. 
      Can be 'All' to remove all occurrences or an integer to specify 
      the exact number of occurrences to remove. Default is 'All'.

    Returns:
    - str: The modified string after removing the substring.
    
    """

    if Substring_To_Remove in String and Times == 'All':
        String = String.replace(Substring_To_Remove, "")

    elif isinstance(Times, int):
        Occurrences = String.count(Substring_To_Remove)

        if Occurrences < Times:
            Times = Occurrences

        for _ in range(Times):
            Index = String.find(Substring_To_Remove)
            if Index == -1:  # Break if substring is not found.
                break
            String = String[:Index] + String[Index + len(Substring_To_Remove):]  

    return String

def Remove_String_Between_Characters(String: str, First_Character: str, 
                                     Second_Character: str, 
                                     Remove_Which: str = 'Both') -> str:
    
    """
    Remove string between specified characters, including the characters 
    based on the Remove_Which parameter.

    Parameters:
    - String (str): The original string from which to remove content.
    - First_Character (str): The character marking the start of removal.
    - Second_Character (str): The character marking the end of removal.
    - Remove_Which (str): Specifies which characters to remove. Can be 
      'Both', 'First', 'Last', or 'None'. Default is 'Both'.

    Returns:
    - str: The modified string with content removed between the characters 
      and optionally the characters themselves.
    
    """

    # Create the pattern to match the content between the characters.
    Pattern = rf'\{First_Character}.*?\{Second_Character}'
    
    # Remove the content between the characters.
    Modified_String = re.sub(Pattern, '', String)

    if Remove_Which == 'Both':
        Modified_String = Modified_String.replace(First_Character, '').replace(Second_Character, '')
    elif Remove_Which == 'First':
        Modified_String = Modified_String.replace(First_Character, '', 1)
    elif Remove_Which == 'Last':
        Modified_String = Modified_String[::-1].replace(Second_Character[::-1], '', 1)[::-1]

    return Modified_String

def Remove_Acents(String: str) -> str:

    """
    Remove accents from characters in the string.

    Parameters:
    - String (str): The original string from which to remove accents.

    Returns:
    - str: The modified string with accents removed.

    """

    return String.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def Remove_Vowels(String: str) -> str:

    """
    Remove vowels from a string.

    Parameters:
    - String (str): The original string from which to remove vowels.

    Returns:
    - str: The modified string with vowels removed.

    """

    Vowels = "aeiouAEIOU"
    return ''.join([Letter for Letter in String if Letter not in Vowels])

def Remove_Everything_Least_Numbers(String: str, Remove_Everything: bool = True) -> str:

    """
    Remove everything except numbers or remove numbers based on a flag.

    Parameters:
    - String (str): The input string to be modified.
    - Remove_Everything (bool): If True, keeps only numbers; if False, 
      removes numbers.

    Returns:
    - str: The modified string based on the flag.

    """

    String = String.strip()

    if Remove_Everything:
        return re.sub(r'[^0-9]', '', String)  # Keep only numbers.
    else:
        return re.sub(r'[0-9]', '', String)  # Remove numbers.

def Remove_Last_Character(String: str) -> str:

    """
    Remove the last character from a string.

    Parameters:
    - String (str): The original string from which to remove the last character.

    Returns:
    - str: The modified string without the last character.

    """

    return String[0:-1]

def Remove_Special_Characters(String: str) -> str:

    """
    Remove special characters from a given string.

    Parameters:
    - String (str): The input string from which special characters will be removed.

    Returns:
    - str: The modified string with special characters removed.
    
    """

    Punctuation = string.punctuation

    for Character in String:
        if Character in Punctuation:
            String = String.replace(Character, '')

    return String


#######################################################################################################################
# GET #
#######################################################################################################################

def Get_Last_Character_Position_Of_Substring(String: str, Substring: str) -> int:

    """
    Get the last position of a substring in a string.

    Parameters:
    - String (str): The string to search within.
    - Substring (str): The substring to find.

    Returns:
    - int: The last position of the substring in the string, 
      or -1 if not found.

    """

    return String.find(Substring) + len(Substring)

def Get_Words_From_Text(Text: str, Word_Index: int = 0, Number_Of_Words: int = 1, 
                        Direction: str = 'Right') -> list:
    
    """
    Extract a specific number of words from a string starting 
    from a given position, with the option to extract to the 
    right or left.

    Parameters:
    - Text (str): The string from which words will be extracted.
    - Word_Index (int): The starting position (1-based) from which 
      to begin extracting words. Can be negative.
    - Number_Of_Words (int): The number of words to extract 
      starting from the base position.
    - Direction (str): The direction of extraction. Can be 
      'Right' or 'Left'. Default is 'Right'.

    Returns:
    - list: A list of extracted words from the string, or an 
      empty list if the base position is out of range.

    """

    Words = Text.split()
    
    if Word_Index < 0:
        Word_Index = len(Words) + Word_Index
    else:
        Word_Index = Word_Index - 1

    if Word_Index > len(Words):
        print(f"Error: \n",
              f"The number of words is {len(Words) + 1} and the position you entered is {Word_Index + 1}. \n",
              "It is out of the allowed range.")
        return []  
    
    if Direction == 'Right':
        Start_Position = Word_Index
        End_Position = Word_Index + Number_Of_Words

        if End_Position > len(Words):
            End_Position = len(Words)
            
    elif Direction == 'Left':
        Start_Position = Word_Index - Number_Of_Words + 1
        End_Position = Word_Index

        if Start_Position < 0:
            Start_Position = 0
    
    if Number_Of_Words > 1:
        Extracted_Words = Words[Start_Position:End_Position]
    elif Number_Of_Words == 1:
        Extracted_Words = [Words[Word_Index]]

    return Extracted_Words

def Get_Longest_Words(Text: str) -> list:

    """
    Get the longest words from the given text.

    Parameters:
    - Text (str): The string from which to find the longest words.

    Returns:
    - list: A list of the longest words in the string.

    """

    Words = Text.split()
    Max_Len = max(len(Word) for Word in Words)
    return [Word for Word in Words if len(Word) == Max_Len]

def Get_Coincident_Characters(String: str) -> list:

    """
    Get characters that occur more than once in a string.

    Parameters:
    - String (str): The string to analyze for coincident characters.

    Returns:
    - list: A list of characters that occur multiple times, or 
      an empty list if none exist.

    """

    if String is None:
        return []
    
    Characters = []

    for i in range(0, len(String)):
        for j in range(0, len(String)):
            if i != j and String[i] == String[j] and String[i] not in Characters:
                Characters.append(String[i])

    return Characters

def Get_Mails(String: str) -> list:

    """
    Extract email addresses from a given string.

    Parameters:
    - String (str): The string from which to extract emails.

    Returns:
    - list: A list of extracted email addresses.

    """

    List_Of_Words = String.split()
    Patron = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?'
    Mails = []

    for Word in List_Of_Words:
        Mail = re.search(Patron, Word)
        if Mail is not None:
            Mails.append(Mail.group())

    return Mails

def Get_URL(String: str) -> list:

    """
    Extract URLs from a given string.

    Parameters:
    - String (str): The string from which to extract URLs.

    Returns:
    - list: A list of extracted URLs.

    """

    List_Of_Words = String.split()
    Patron = r'https?://[A-Za-z0-9._%+-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?(?:/[A-Za-z0-9._%+-]*)*'
    URLs = []

    for Word in List_Of_Words:
        URL = re.search(Patron, Word)
        if URL is not None:
            URLs.append(URL.group())

    return URLs

#######################################################################################################################
# PROCESSING #
#######################################################################################################################

def Clean_String_With_Emojis(String_With_Emojis: str, Include_Emojis: bool = False) -> str:

    """
    Remove emojis from the string or return only emojis.

    Parameters:
    - String_With_Emojis (str): The original string with potential emojis.
    - Include_Emojis (bool): If True, return only the emojis found. 
      Default is False, which removes emojis.

    Returns:
    - str: The cleaned string or string containing only emojis.
    
    """

    Emoji_Pattern = re.compile(
        "["  
        "\U0001F600-\U0001F64F"   # Emoticons
        "\U0001F300-\U0001F5FF"   # Miscellaneous Symbols and Pictographs
        "\U0001F680-\U0001F6FF"   # Transport and Map Symbols
        "\U0001F700-\U0001F77F"   # Alchemical Symbols
        "\U0001F780-\U0001F7FF"   # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"   # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"   # Supplemental Emoji
        "\U0001FA00-\U0001FA6F"   # Chess Symbols
        "\U0001FA70-\U0001FAFF"   # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"   # Miscellaneous Symbols
        "\U000024C2-\U0001F251"   # Enclosed Alphanumeric Supplement
        "]+", 
        flags=re.UNICODE
    )

    if Include_Emojis:
        String_With_Emojis = String_With_Emojis.replace("♀️", "").replace("♂️", "")
        return ''.join(Emoji_Pattern.findall(String_With_Emojis))

    return Emoji_Pattern.sub('', String_With_Emojis)

def Invert_Words(Sentence: str) -> str:

    """
    Invert each word in a given sentence.

    Parameters:
    - Sentence (str): The original sentence to be inverted.

    Returns:
    - str: The sentence with each word inverted.
    
    """

    return ' '.join([Word[::-1] for Word in Sentence.split()])

def Convert_Letters_To_Numbers(String: str) -> str:

    """
    Convert specific letters to numbers in the string.

    Parameters:
    - String (str): The original string to convert.

    Returns:
    - str: The modified string with letters replaced by numbers.
    
    """

    Leet_Dict = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 't': '7'}
    return ''.join([Leet_Dict.get(Letter.lower(), Letter) for Letter in String])

def Apply_Camel_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to camel case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to camel case.
    
    """

    Words = String.split(f'{Separator}')
    Camel_Case_String = Words[0].lower() + ''.join(Word.capitalize() for Word in Words[1:])
    return Camel_Case_String

def Apply_Snake_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to snake case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to snake case.
    
    """

    return String.replace(Separator, "_").lower()

def Apply_Pascal_Snake_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to Pascal case with snake case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to Pascal case with snake case.
    
    """

    Words = String.split(f'{Separator}')
    Upper_Snake_Case_String = [Word.capitalize() for Word in Words]
    return "_".join(Upper_Snake_Case_String)

def Apply_Screaming_Snake_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to screaming snake case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to screaming snake case.
    
    """

    return String.replace(Separator, "_").upper()

def Apply_Pascal_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to Pascal case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to Pascal case.
    
    """

    Words = String.split(f'{Separator}')
    return ''.join(Word.capitalize() for Word in Words)

def Apply_Flat_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to flat case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to flat case.
    
    """

    Words = String.split(f'{Separator}')
    Flat_Case_String = ''.join(Word.lower() for Word in Words)
    return Flat_Case_String

def Apply_Upper_Flat_Case(String: str, Separator: str = " ") -> str:

    """
    Convert a string to upper flat case.

    Parameters:
    - String (str): The original string to convert.
    - Separator (str): The character separating words in the string. 
      Default is a space.

    Returns:
    - str: The string converted to upper flat case.
    
    """

    Words = String.split(f'{Separator}')
    Upper_Flat_Case_String = ''.join(Word.upper() for Word in Words)
    return Upper_Flat_Case_String

#######################################################################################################################
# COUNTS #
#######################################################################################################################

def Count_Vowels_And_Consonants(String: str) -> tuple[int, int]:

    """
    Count the number of vowels and consonants in a given string.

    Parameters:
    - String (str): The input string to analyze.

    Returns:
    - tuple[int, int]: A tuple containing the number of vowels and the number of consonants.
    
    """

    Vowels = "aeiouAEIOU"
    Consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    
    Number_Of_Vowels = sum(1 for Letter in String if Letter in Vowels)
    Number_Of_Consonants = sum(1 for Letter in String if Letter in Consonants)
    
    return Number_Of_Vowels, Number_Of_Consonants

#######################################################################################################################
# GENERATE #
#######################################################################################################################

def Generate_Acronym(Sentence: str) -> str:

    """
    Generate an acronym from the first letters of each word in a sentence.

    Parameters:
    - Sentence (str): The input sentence to create an acronym from.

    Returns:
    - str: The generated acronym in uppercase.
    
    """

    return ''.join([Word[0].upper() for Word in Sentence.split()])

#######################################################################################################################
# CHECK #
#######################################################################################################################

def Check_If_Anagram(String1: str, String2: str) -> bool:

    """
    Check if two strings are anagrams of each other.

    Parameters:
    - String1 (str): The first string to compare.
    - String2 (str): The second string to compare.

    Returns:
    - bool: True if the strings are anagrams, False otherwise.
    
    """

    String1 = ''.join(sorted(String1.replace(' ', '').lower()))
    String2 = ''.join(sorted(String2.replace(' ', '').lower()))
    
    return String1 == String2

def Check_If_Palindrome(String: str) -> bool:

    """
    Check if a string is a palindrome.

    Parameters:
    - String (str): The input string to check for palindrome properties.

    Returns:
    - bool: True if the string is a palindrome, False otherwise.
    
    """

    String = ''.join(Letter for Letter in String if Letter.isalnum()).lower()
    
    return String == String[::-1]





