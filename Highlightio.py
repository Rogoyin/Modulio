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

    """

    i = 0
    while Line[i] != "(":
        i += 1
    Author = Line[i+1:len(Line)-1]
    return Author

def Extract_Book(Line: str) -> str:

    """
    Extracts the book title from a line of text.

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

    """

    Text = '- Tu subrayado en la página '
    First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Text)
    Last_Digit = Line.find(' | posición ') - 1
    Page = Line[First_Digit:Last_Digit]
    return Page

def Extract_Day_Of_Week(Line: str) -> str:

    """
    Extracts the day of the week from a line of text.

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

    """

    Day = Extract_Day_Of_Week(Line).lower()
    First_Digit = Stringio.Get_Last_Character_Position_Of_Substring(Line, Day) + 2
    Last_Digit = Line.find(' de ')
    Day = Line[First_Digit:Last_Digit]
    return Day

def Extract_Month(Line: str) -> str:

    """
    Extracts the month from a line of text.

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
    Creates a list of dictionaries with note data from a list of lines.

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

def Match_Notes_With_Notion_Bases(Token: object, Author_List: list, Page_ID: str, Previous_Match_Base: list) -> list:

    """
    Matches author names from Notion with a list of authors and updates the previous match base.

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
    Extracts authors, books, or both from the note file.

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
