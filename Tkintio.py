import tkinter as tk
from tkinter import filedialog, simpledialog
import Listio

def Display_Options(Options_List: list = ['Option 1', 'Option 2', 'Option 3'], 
                    Prompt_Message: str = 'Select your preference:',
                    Choice_Message: str = 'Enter the number of your choice:', 
                    Option_Message: str = 'Selected option:', 
                    Invalid_Option_Message: str = 'Default', 
                    Invalid_Input_Message: str = 'The selected option is invalid.', 
                    First_Index: int = 1) -> str:
    
    '''
    Displays a list of options and prompts the user for a choice.

    This function presents a menu of options to the user, allowing them 
    to select one by entering the corresponding number. The selected 
    option is then returned. If the input is invalid, the user is 
    prompted to try again.

    Parameters:
    -----------
    Options_List : list
        A list of strings representing the options to be displayed. 
        Default is ['Option 1', 'Option 2', 'Option 3'].

    Prompt_Message : str
        A message displayed to prompt the user before showing the options. 
        Default is 'Select your preference:'.

    Choice_Message : str
        A message asking the user to enter the number of their choice. 
        Default is 'Enter the number of your choice:'.

    Option_Message : str
        A message displayed after an option is selected. Default is 
        'Selected option:'.

    Invalid_Option_Message : str
        A message displayed if the option chosen is invalid. Default 
        is 'Default', which triggers a generic error message.

    Invalid_Input_Message : str
        A message displayed for invalid input. Default is 
        'The selected option is invalid.'.

    First_Index : int
        The index of the first option displayed to the user. Default is 1.

    Returns:
    --------
    str
        The string of the selected option.

    Notes:
    ------
    - If the input is out of range or not a number, the user will be 
      prompted again.
    - The function allows for customization of all displayed messages.

    Example:
    ---------
    >>> selected_option = Display_Options(['Yes', 'No'], 'Choose:', 'Enter:')
    >>> print(selected_option)
    'Yes'  # or 'No' based on user input

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
    Opens a file explorer dialog to select a file.

    This function launches a file explorer for the user to choose a 
    file. The selected file path is returned as a string. If no file 
    is selected, the function will return None.

    Parameters:
    -----------
    Explorer_Title : str
        The title of the file explorer window. Default is 
        'Select a file'.

    Filetypes_Text : list
        A list of tuples defining the file types that the user can 
        select from. Default allows all file types.

    Returns:
    --------
    str
        The path of the selected file or None if no file is selected.

    Notes:
    ------
    - The function uses a Tkinter window for file selection.
    - If a file is successfully selected, its path will be printed 
      to the console.

    Example:
    ---------
    >>> file_path = Open_File('Choose a file', [("Text files", "*.txt")])
    >>> print(file_path)
    '/path/to/selected/file.txt'

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
    Opens a file explorer dialog to select a directory.

    This function allows the user to choose a directory from their file 
    system. The path of the selected directory is returned. If no 
    directory is selected, None is returned.

    Parameters:
    -----------
    Explorer_Title : str
        The title of the directory selection dialog. Default is 
        'Select a directory'.

    Message_Selected_Directory : str
        A message displayed when a directory is successfully selected. 
        Default is 'Selected directory:'.

    Message_Not_Selected_Directory : str
        A message displayed if no directory is selected. Default is 
        'No directory selected'.

    Returns:
    --------
    str
        The path of the selected directory or None if no directory 
        is selected.

    Notes:
    ------
    - The function uses a Tkinter window for directory selection.
    - The selected directory path is printed to the console.

    Example:
    ---------
    >>> selected_directory = Open_Directory('Choose folder')
    >>> print(selected_directory)
    '/path/to/selected/directory'

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
                  Text = '',
                  Wrap_Lenght = 380, 
                  Pad = 10):
    
    '''
    Creates a new Tkinter window with specified parameters.

    This function initializes a Tkinter window, sets its title, 
    geometry, and position, and displays a Label with the provided 
    text. The window can be customized with various attributes.

    Parameters:
    -----------
    Title : str, optional
        The title of the window. If None, the title will not be set.

    Geometry : str
        The size and geometry of the window specified as 'widthxheight'. 
        Default is "400x300".

    Position : str
        The position of the window on the screen. Default is 'center', 
        which centers the window on the screen.

    Text : str, optional
        The text to be displayed in the window. If None, no text 
        will be shown.

    Wrap_Lenght : int
        The maximum length of text to wrap in the Label. Default is 380.

    Pad : int
        The padding around the Label in pixels. Default is 10.

    Returns:
    --------
    tk.Tk
        The created Tkinter window object.

    Notes:
    ------
    - The function can be modified to include more widgets as needed.
    - The window will remain open until it is closed by the user.

    Example:
    ---------
    >>> window = Create_Window('My Window', '400x300', 'center', 'Hello!')
    >>> window.mainloop()

    '''

    Window = tk.Tk()
    Window.title(Title)
    Window.geometry(Geometry)
    Window.eval(f'tk::PlaceWindow . {Position}')
    tk.Label(Window, text = Text, wraplength = Wrap_Lenght).pack(pady = Pad)

    return Window

def Show_Options_Window(Title: str, Message: str, Options, Widht_Padding = 5):

    '''
    Displays a window with options for the user to select.

    This function creates a new window with a title and a message, 
    displaying a button for each option provided. The width of each 
    button is adjusted based on the maximum character length of the 
    options.

    Parameters:
    -----------
    Title : str
        The title of the options window.

    Message : str
        The message displayed at the top of the window.

    Options : list
        A list of strings representing the options available for selection.

    Widht_Padding : int
        Additional width added to the buttons for padding. Default is 5.

    Returns:
    --------
    None

    Notes:
    ------
    - The function calls Create_Window to generate the options window.
    - The buttons do not currently have an action associated with them.

    Example:
    ---------
    >>> Show_Options_Window('Select an Option', 'Choose one of the options:', ['Option 1', 'Option 2'])
    
    '''

    Window = Create_Window(Title = Title, Text = Message)

    Button_Width = Listio.Max_Characters(Options) + Widht_Padding

    for Option in Options:
        tk.Button(Window, 
                  text = Option,
                  width = Button_Width)

    Window.mainloop()

def Show_Alert_With_Input_Field(Title: str, 
                                Message: str, 
                                Geometry: str = "400x300", 
                                Position: str = 'center', 
                                Text: str = '', 
                                Wrap_Length: int = 380, 
                                Pad: int = 10) -> str:
    
    """
    Displays a custom message prompt with an input field.

    This function creates a window that prompts the user for a string 
    input based on the provided title and message. The user's input 
    is returned as a string.

    Parameters:
    -----------
    Title : str
        The title of the message dialog that appears at the top.

    Message : str
        The message displayed in the dialog prompting the user for 
        input.
    
    Geometry : str, optional
        The dimensions of the window in the format 'widthxheight'. 
        Default is '400x300'.
    
    Position : str, optional
        The position of the window on the screen ('center', 
        'top-left', etc.). Default is 'center'.

    Text : str, optional
        Default text in the input field. Default is None.

    Wrap_Length : int, optional
        Wrap length for the message text. Default is 380.

    Pad : int, optional
        Padding for the window. Default is 10.

    Returns:
    --------
    str
        The user's input string from the dialog box, or None if 
        cancelled.

    """

    Root_Window = tk.Tk()
    Root_Window.withdraw()  # Hide the root window.

    # Create a new top-level window.
    Window = tk.Toplevel(Root_Window)
    Window.title(Title)
    Window.geometry(Geometry)

    # Get screen width and height.
    Screen_Width = Window.winfo_screenwidth()
    Screen_Height = Window.winfo_screenheight()
    
    # Calculate position for centering.
    if Position == 'center':
        Window_Width = int(Geometry.split('x')[0])
        Window_Height = int(Geometry.split('x')[1])
        X_Coordinate = (Screen_Width // 2) - (Window_Width // 2)
        Y_Coordinate = (Screen_Height // 2) - (Window_Height // 2)
        Window.geometry(f"{Geometry}+{X_Coordinate}+{Y_Coordinate}")

    # Add a label with the message.
    Label = tk.Label(Window, text = Message, wraplength = Wrap_Length, padx = Pad, pady = Pad)
    Label.pack()

    # Add an input field.
    Input_Field = tk.Entry(Window, width = 50)
    if Text:
        Input_Field.insert(0, Text)
    Input_Field.pack(padx = Pad, pady = Pad)

    # Add a submit button.
    def On_Submit():
        User_Input = Input_Field.get()
        Window.destroy()  
        Root_Window.quit()  
        return User_Input

    Submit_Button = tk.Button(Window, text = "Submit", command = On_Submit)
    Submit_Button.pack(pady = Pad)

    Root_Window.mainloop()

    return Input_Field.get()

