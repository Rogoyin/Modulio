import tkinter as tk
from tkinter import filedialog
import Listio

def Display_Options(Options_List: list = ['Option 1', 'Option 2', 'Option 3'], 
                    Prompt_Message: str = 'Select your preference:',
                    Choice_Message: str = 'Enter the number of your choice:', 
                    Option_Message: str = 'Selected option:', 
                    Invalid_Option_Message: str = 'Default', 
                    Invalid_Input_Message: str = 'The selected option is invalid.', 
                    First_Index: int = 1) -> str:
    
    '''
    Display a list of options and prompt the user for a choice.
    Example: Display_Options(['Yes', 'No'], 'Choose:', 'Enter:')

    '''

    print(Prompt_Message)

    for Index_Option, Option in enumerate(Options_List, First_Index):
        print(f"{Index_Option}. {Option}")

    Choice = input(Choice_Message)

    try:
        Choice = int(Choice)
        if First_Index <= Choice < First_Index + len(Options_List):
            Selected_Option = Options_List[Choice - First_Index]
            print(f"{Option_Message} {Selected_Option}")
            return Selected_Option
        else:
            if Invalid_Option_Message == 'Default':
                print(f'The input must be a number between {First_Index} and {First_Index + len(Options_List) - 1}')
            else:
                print(Invalid_Input_Message)
            return Display_Options(Options_List, Prompt_Message, Choice_Message, Option_Message, Invalid_Option_Message, Invalid_Input_Message, First_Index)

    except ValueError:
        print(Invalid_Input_Message)
        return Display_Options(Options_List, Prompt_Message, Choice_Message, Option_Message, Invalid_Option_Message, Invalid_Input_Message, First_Index)

def Open_File(Explorer_Title: str = 'Select a file', 
              Filetypes_Text: list = [("All files", "*.*")]) -> str:
    
    '''
    Open a file explorer dialog to select a file.
    Example: Open_File('Choose a file', [("Text files", "*.txt")])

    '''

    Main_Window = tk.Tk()
    Main_Window.withdraw()
    Main_Window.wm_attributes('-topmost', 1)
    File_Selected_Path = filedialog.askopenfilename(title=Explorer_Title, filetypes=Filetypes_Text)
    Main_Window.destroy()

    if File_Selected_Path:
        print(f"Selected file: {File_Selected_Path}")
        return File_Selected_Path

def Open_Directory(Explorer_Title: str = 'Select a directory',
                   Message_Selected_Directory: str = 'Selected directory:', 
                   Message_Not_Selected_Directory: str = 'No directory selected') -> str:
    
    '''
    Open a file explorer dialog to select a directory.
    Example: Open_Directory('Choose folder')

    '''
    
    Main_Window = tk.Tk()
    Main_Window.withdraw()
    Main_Window.wm_attributes('-topmost', 1)
    Directory_Selected_Path = filedialog.askdirectory(title=Explorer_Title)
    Main_Window.destroy()

    if Directory_Selected_Path:
        print(f"{Message_Selected_Directory} {Directory_Selected_Path}")
        return Directory_Selected_Path
    else:
        print(Message_Not_Selected_Directory)
        return None

def Create_Window(Title = None, 
                  Geometry = "400x300", 
                  Position = 'center', 
                  Text = None,
                  Wrap_Lenght = 380, 
                  Pad = 10):
    
    Window = tk.Tk()
    Window.title(Title)
    Window.geometry(Geometry)
    Window.eval(f'tk::PlaceWindow . {Position}')
    tk.Label(Window, text = Text, wraplength = Wrap_Lenght).pack(pady = Pad)

    return Window

def Show_Options_Window(Title, Message, Options, Widht_Padding = 5):

    Window = Create_Window(Title = Title, Text = Message)

    Button_Width = Listio.Max_Characters(Options) + Widht_Padding

    for Option in Options:
        tk.Button(Window, 
                  text = Option,
                  width = Button_Width)

    Window.mainloop()

def Show_Message(Title, Message):
    Window = tk.Tk()
    Window.withdraw()  # Oculta la ventana principal
    return tk.simpledialog.askstring(Title, Message)  

