import re

#######################################################################################################################
# REMOVE #
#######################################################################################################################

def Remove_Substring_From_String(String: str, Substring_To_Remove: str) -> str:

    if Substring_To_Remove in String:
        String = String.replace(Substring_To_Remove, "")
    return String

def Remove_String_Between_Characters(String: str, First_Character: str, Second_Character: str) -> str:

    '''
    Remove String between specified characters, including the characters themselves.

    '''

    Pattern = rf'\{First_Character}.*?\{Second_Character}'
    return re.sub(Pattern, '', String)

def Remove_Acents(String: str) -> str:
    return String.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def Remove_Vowels(String: str) -> str:
    Vowels = "aeiouAEIOU"
    return ''.join([Letter for Letter in String if Letter not in Vowels])

def Remove_Everything_Least_Numbers(String: str, Remove_Everything: bool = True) -> str:

    """
    Removes everything except numbers from the string or removes numbers based on the flag.

    Parameters:
        String (str): The input string.
        Remove_Everything (bool): If True, keeps only numbers; if False, removes numbers.

    Returns:
        str: The modified string based on the flag.
        
    """
    String = String.strip()

    if Remove_Everything:
        return re.sub(r'[^0-9]', '', String)  # Keep only numbers.
    else:
        return re.sub(r'[0-9]', '', String)  # Remove numbers.

def Remove_Last_Character(String: str) -> str:
    return String[0:-1]

# def Remove_Special_Characters(String: str) -> str:

#######################################################################################################################
# GET #
#######################################################################################################################

def Get_Last_Character_Position_Of_Substring(String: str, Substring: str) -> int:
    return String.find(Substring) + len(Substring)

def Get_Words_From_Text(Text: str, Word_Index: int = 0, Number_Of_Words: int = 1, Direction: str = 'Right') -> list:

    '''
    Extract a specific number of words from a String starting from a given position, with the option to extract to the 
    right or left.

    Parameters:
    - Text (str): The String from which words will be extracted.
    - Word_Index (int): The starting position (1-based) from which to begin extracting words. Adjusted internally 
    for 0-based indexing. Can be negative.
    - Number_Of_Words (int): The number of words to extract starting from the base position.
    - Direction (str): The direction of extraction. Can be 'Right' or 'Left'. Default is 'Right'.

    Returns:
    - list: A list of extracted words from the String, or an empty list if the base position is out of range or if an 
    error occurs.

    Examples:
    1. Extract_Words("Python is a programming language", 2, 3, 'Right')
       -> ['is', 'a', 'programming']
    
    2. Extract_Words("Python is a programming language", 4, 2, 'Left')
       -> ['a', 'is']

    '''
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

def Get_Longest_Words(Text: str) -> str:
    Words = Text.split()
    Max_Len = max(len(Word) for Word in Words)
    return [Word for Word in Words if len(Word) == Max_Len]

def Get_Coincident_Characters(String: str) -> list:

    if String is None:
        return []
    
    Characters = []

    for i in range (0, len(String)):
        for j in range (0, len(String)):
            if i != j and String[i] == String[j] and String[i] not in Characters:
                Characters.append(String[i])

    return Characters

def Get_Mails(String: str) -> list:

    List_Of_Words = String.split()
    Patron = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?'
    Mails = []

    for Word in List_Of_Words:
        Mail = re.search(Patron, Word)
        if Mail is not None:
            Mails.append(Mail.group())

    return Mails

def Get_URL(String: str) -> list:

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
    Removes emojis from the string. It returns only emojis if Include_Emojis is True.

    """

    Emoji_Pattern = re.compile(
        "["  
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", 
        flags=re.UNICODE
    )

    if Include_Emojis:
        String_With_Emojis = String_With_Emojis.replace("♀️", "").replace("♂️", "")
        return ''.join(Emoji_Pattern.findall(String_With_Emojis))
    
    return Emoji_Pattern.sub('', String_With_Emojis)

def Invert_Words(Sentence: str) -> str:
    return ' '.join([Word[::-1] for Word in Sentence.split()])

def Convert_Letters_To_Numbers(String: str) -> str:
    Leet_Dict = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 't': '7'}
    return ''.join([Leet_Dict.get(Letter.lower(), Letter) for Letter in String])

def Apply_Camel_Case(String: str, Separator: str = " ") -> str:
    Words = String.split(f'{Separator}')
    Camel_Case_String = Words[0].lower() + ''.join(Word.capitalize() for Word in Words[1:])
    return Camel_Case_String

def Apply_Snake_Case(String: str, Separator: str = " ") -> str:
    return String.replace(Separator, "_").lower()

def Apply_Pascal_Snake_Case(String: str, Separator: str = " ") -> str:
    Words = String.split(f'{Separator}')
    Upper_Snake_Case_String = [Word.capitalize() for Word in Words]
    return "_".join(Upper_Snake_Case_String)

def Apply_Screaming_Snake_Case(String: str, Separator: str = " ") -> str:
    return String.replace(Separator, "_").upper()

def Apply_Pascal_Case(String: str, Separator: str = " ") -> str:
    Words = String.split(f'{Separator}')
    return ''.join(Word.capitalize() for Word in Words)

def Apply_Flat_Case(String: str, Separator: str = " ") -> str:
    Words = String.split(f'{Separator}')
    Flat_Case_String = ''.join(Word.lower() for Word in Words)
    return Flat_Case_String

def Apply_Upper_Flat_Case(String: str, Separator: str = " ") -> str:
    Words = String.split(f'{Separator}')
    Upper_Flat_Case_String = ''.join(Word.upper() for Word in Words)
    return Upper_Flat_Case_String

# def Clean_Spaces(String: str) -> str:

# def Split_By_Words(Text: str) -> str:

#######################################################################################################################
# COUNTS #
#######################################################################################################################

def Count_Vowels_And_Consonants(String: str) -> int:
    Vowels = "aeiouAEIOU"
    Consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    Number_Of_Vowels = sum(1 for Letter in String if Letter in Vowels)
    Number_Of_Consonants = sum(1 for Letter in String if Letter in Consonants)
    return Number_Of_Vowels, Number_Of_Consonants

#######################################################################################################################
# GENERATE #
#######################################################################################################################

def Generate_Acronym(Sentence: str) -> str:
    return ''.join([Word[0].upper() for Word in Sentence.split()])

#######################################################################################################################
# CHECK #
#######################################################################################################################

def Check_If_Anagram(String1: str, String2: str) -> bool:
    String1 = ''.join(sorted(String1.replace(' ', '').lower()))
    String2 = ''.join(sorted(String2.replace(' ', '').lower()))
    return String1 == String2

def Check_If_Palindrome(String: str) -> bool:
    String = ''.join(Letter for Letter in String if Letter.isalnum()).lower()
    return String == String[::-1]

# def Check_Similarity(String1: str, String2: str) -> str:

# def Split_By_Words(String: str) -> str:





