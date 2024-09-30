import re
import pandas as pd
import numpy as np
import Stringio
import Listio
import Notio
import Framio
import numpy as np

def Extract_Author(Line: str) -> str:

    """
    Extracts the author from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      author's name. The author's name is expected to be enclosed in 
      parentheses following the book title.

    Returns:
    - str: The extracted author's name.

    """

    i = 0
    while Line[i] != "(":
        i += 1
    Author = Line[i+1:len(Line)-1]
    return Author

def Extract_Book(Line: str) -> str:

    """
    Extracts the book title from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      book title. The book title is expected to appear before the author's 
      name, which is enclosed in parentheses.

    Returns:
    - str: The extracted book title.

    """

    Line = Stringio.Remove_Substring_From_String(Line, '\ufeff')
    i = 0
    while Line[i] != "(":
        i += 1
    Book = Line[:i-1]
    return Book

def Extract_Page(Line: str) -> str:

    """
    Extracts the page number from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      page number. The page number is expected to follow the text 
      '- Tu subrayado en la página ' and precede ' | posición '.

    Returns:
    - str: The extracted page number.

    """

    Text = '- Tu subrayado en la página '
    First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text)
    Last_Digit = Line.find(' | posición ') - 1
    Page = Line[First_Digit:Last_Digit]
    return Page

def Extract_Day_Of_Week(Line: str) -> str:

    """
    Extracts the day of the week from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      day of the week. The day is indicated by a two-letter abbreviation 
      following the text ' | Añadido el '.

    Returns:
    - str: The full name of the day of the week (e.g., 'Lunes').

    """
    
    Day_Of_Week = ''
    Text = ' | Añadido el '
    First_Letter = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text)
    Second_Letter = First_Letter + 1
    Two_Letters = Line[First_Letter] + Line[Second_Letter]

    if Two_Letters == 'lu':
        Day_Of_Week = 'Lunes'
    elif Two_Letters == 'ma':
        Day_Of_Week = 'Martes'
    elif Two_Letters == 'mi':
        Day_Of_Week = 'Miércoles'
    elif Two_Letters == 'ju':
        Day_Of_Week = 'Jueves'
    elif Two_Letters == 'vi':
        Day_Of_Week = 'Viernes'
    elif Two_Letters == 'sa':
        Day_Of_Week = 'Sábado'
    elif Two_Letters == 'do':
        Day_Of_Week = 'Domingo'

    return Day_Of_Week

def Extract_Day(Line: str) -> str:

    """
    Extracts the day from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      day. The day is located between the extracted day of the week 
      and the word 'de'.

    Returns:
    - str: The extracted day as a string.

    """

    Day = Extract_Day_Of_Week(Line).lower()
    First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Day) + 2
    Last_Digit = Line.find(' de ')
    Day = Line[First_Digit:Last_Digit]
    return Day

def Extract_Month(Line: str) -> str:

    """
    Extracts the month from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      month. The month is identified by matching it against a predefined 
      list of month names.

    Returns:
    - str: The extracted month, capitalized (e.g., 'Enero').

    """

    Months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    for Month in Months:
        if Month in Line:
            Final_Month = Month
    Final_Month = Final_Month.capitalize()
    return Final_Month

def Extract_Year(Line: str) -> str:

    """
    Extracts the year from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      year. The year is expected to be in the range of 1900 to 2100.

    Returns:
    - str: The extracted year as a string.

    """

    Years = np.arange(1900, 2100).tolist()
    for Year in Years:
        if str(Year) in Line:
            Index_Last_Year = Line.rfind(str(Year))
            Final_Year = Line[Index_Last_Year:Index_Last_Year + 4]
            break 

    return Final_Year

def Extract_Hour(Line: str) -> str:

    """
    Extracts the time (hour) from a line of text.

    Parameters:
    - Line (str): A string containing the text from which to extract the 
      hour. The hour is found by identifying a colon (':') and extracting 
      the characters surrounding it.

    Returns:
    - str: The extracted hour as a string (e.g., '12:30').

    """

    Text = ':'
    First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text) - 3
    if Line[First_Digit] == ' ':
        First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text) - 2
    Last_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text) + 2
    Hour = Line[First_Digit:Last_Digit]
    return Hour

def Build_Note(Lines_List: list) -> list:

    """
    Creates a list of dictionaries containing note data from a list of lines.

    Parameters:
    - Lines_List (list): A list of strings where each string represents a 
      line of text containing information about a note, including author, 
      book, page, date, hour, and highlight.

    Returns:
    - list: A list of dictionaries where each dictionary contains 
      information for a note, with keys like 'Author', 'Book', 'Page', 
      'Day_Of_Week', 'Day', 'Month', 'Year', 'Hour', and 'Highlight'.

    """

    Separator = '=========='
    Notes_List = []
    i = 0

    while i < len(Lines_List):
        Note_Dict = {}
        Note_Dict['Author'] = Extract_Author(Lines_List[i])
        Note_Dict['Book'] = Extract_Book(Lines_List[i])
        Note_Dict['Page'] = Extract_Page(Lines_List[i + 1])
        Note_Dict['Day_Of_Week'] = Extract_Day_Of_Week(Lines_List[i + 1])
        Note_Dict['Day'] = Extract_Day(Lines_List[i + 1])
        Note_Dict['Month'] = Extract_Month(Lines_List[i + 1])
        Note_Dict['Year'] = Extract_Year(Lines_List[i + 1])
        Note_Dict['Hour'] = Extract_Hour(Lines_List[i + 1])
        i += 3

        Highlight_Lines_List = []
        while Lines_List[i] != Separator:
            Highlight_Lines_List.append(Lines_List[i])
            i += 1

        Highlight = ' '.join(map(str, Highlight_Lines_List))
        Note_Dict['Highlight'] = Highlight
        Notes_List.append(Note_Dict)
        i += 1
    
    return Notes_List

def Match_Notes_With_Notion_Bases(Token: object, Author_List: list, Page_ID: str, 
                                  Previous_Match_Base: list) -> list:

    """
    Matches author names from Notion with a list of authors and updates the 
    previous match base.

    Parameters:
    - Token (object): An authentication token used for accessing Notion 
      API.
    - Author_List (list): A list of author names to match with Notion.
    - Page_ID (str): The unique identifier for the Notion page to be 
      accessed.
    - Previous_Match_Base (list): A list of previously matched authors 
      and their IDs.

    Returns:
    - list: The updated match base list, including any new matches found 
      between the Notion titles and the provided author list.

    """

    Titles = Notio.Get_Database_Properties(Token, Page_ID, Data=['Title', 'ID'])

    if Previous_Match_Base != []:
        Listed_Authors = [author['Author'] for author in Previous_Match_Base]
    else:
        Listed_Authors = []

    Notion_Last_Names = []
    for i in range(len(Titles)):
        Name = Titles[i]['Title']
        Name = Stringio.Remove_Acents(Name)
        Name = Stringio.Get_Words_From_Text(Name, -1).strip()
        Notion_Last_Names.append(Name)

    List_Last_Names = []
    for i in range(len(Author_List)):
        Name = Author_List[i]
        Name = Stringio.Remove_Acents(Name)
        Name = Stringio.Get_Words_From_Text(Name, -1).strip()
        List_Last_Names.append(Name)

    for i in range(len(Notion_Last_Names)):
        Match_Dict = {}

        k = 0
        while k < len(List_Last_Names):
            if Notion_Last_Names[i] == List_Last_Names[k]:
                Final_Author_ID = Titles[i]['ID']
                Final_Author_List = Author_List[k]

                Match_Dict['Author'] = Final_Author_List
                Match_Dict['ID'] = Final_Author_ID

                if Final_Author_List not in Listed_Authors:
                    Previous_Match_Base.append(Match_Dict)

            k += 1

    return Previous_Match_Base

def Extract_Note_Data(File_Path: str, Data_To_Extract: str = 'Authors') -> list:

    """
    Extracts authors, books, or both from the note file specified by the 
    file path.

    Parameters:
    - File_Path (str): The file path to the note file from which data is 
      to be extracted.
    - Data_To_Extract (str): A string indicating the type of data to 
      extract; can be 'Authors', 'Books', or 'Both'.

    Returns:
    - list: Depending on the value of Data_To_Extract, it returns a list 
      of unique authors, a list of unique books, or a list of dictionaries 
      containing both authors and their corresponding books.

    """

    try:
        with open(File_Path, 'r', encoding='utf-8') as File:
            Content = File.read()

        Lines_List = Content.splitlines()
        Notes = Build_Note(Lines_List)
        df = pd.DataFrame(Notes)

        if Data_To_Extract == 'Authors':
            Authors = df['Author'].unique()
            return Authors.tolist()

        if Data_To_Extract == 'Books':
            Books = df['Book'].unique()
            return Books.tolist()

        if Data_To_Extract == 'Both':
            Books_Authors_List = []
            Books = df['Book'].unique()

            for i in range(len(Books)):
                Dict = {}
                k = 0
                while df['Book'][k] != Books[i]:
                    k += 1
                Dict['Author'] = df['Author'][k]
                Dict['Book'] = df['Book'][k]
                Books_Authors_List.append(Dict)

            return Books_Authors_List

    except FileNotFoundError:
        print(f"Error: The file at '{File_Path}' was not found.")
        return []
    except Exception as e:
        print(f"Error: There was a problem processing the file. {e}")
        return []

def Build_Df_Of_Highlights(File_Path: str) -> pd.DataFrame:

    """
    Converts notes from a file into a pandas DataFrame.

    Parameters:
    - File_Path (str): The file path to the note file to be processed.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing the processed notes 
      with columns for author, book, page, day, month, year, hour, 
      and highlight text. The DataFrame is sorted by year.

    """

    with open(File_Path, 'r', encoding='utf-8') as File:
        Content = File.read()

    Lines_List = Content.splitlines()
    Notes = Build_Note(Lines_List)
    df = pd.DataFrame(Notes)

    # Hour Format.
    df['Hour'] = pd.to_datetime(df['Hour'], format='%H:%M').dt.time

    # 'Date' column.
    df = Framio.Create_Date_Column(df, Spanish = True)

    # Sort.
    df = Framio.Sort_Columns(df, Order_By='Year')

    return df
