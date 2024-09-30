import pandas as pd

def Group_Dictionaries_By_Parent_Element(
    df: pd.DataFrame, 
    Element_List: list[str], 
    Parent_Element: str, 
    Child_List: list[str]
) -> list[list[dict]]:
    
    """
    Group dictionaries containing child elements for each parent element.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - Element_List (list[str]): List of parent element values to group by.
    - Parent_Element (str): The column name to use as the parent element.
    - Child_List (list[str]): List of child element names to extract.

    Returns:
    - list[list[dict]]: A list of grouped dictionaries for each parent 
      element.
    
    Example:
    - Parent_Element: 'Name'.
    - Element_List: ['Jorge', 'Ramón']
    - Child_List: ['Age', 'City']
    - Result: [['Jorge', {'Age': 26}, {'City': 'Buenos Aires'}], 
                ['Ramón', {'Age': 28}, {'City': 'Rio de Janeiro'}]]

    """

    Result = []

    for Element in Element_List:
        Data_By_Element = [Element]

        for Index, Row in df.iterrows():
            if Element == Row[Parent_Element]:
                Dictionary = {Child: Row[Child] for Child in Child_List}
                Data_By_Element.append(Dictionary)
        
        Result.append(Data_By_Element)
    
    return Result

def Get_Values_By_Key(Dict_List: list[dict], Key: str) -> list:

    """
    Extract values corresponding to a specific key from a list of 
    dictionaries.

    Parameters:
    - Dict_List (list[dict]): A list of dictionaries to extract values from.
    - Key (str): The key for which values should be extracted.

    Returns:
    - list: A list of values corresponding to the specified key.

    """

    Values_List = []
    for Dict in Dict_List:
        Values_List.append(Dict[Key])
    return Values_List

def Get_Key_By_Index(Dictionary: dict, Index: int):

    """
    Retrieve a key from a dictionary by its index.

    Parameters:
    - Dictionary (dict): The dictionary to retrieve the key from.
    - Index (int): The index of the key to retrieve.

    Returns:
    - str: The key at the specified index.

    Raises:
    - KeyError: If the index is out of range.

    """

    Count = 0
    if Index >= len(Dictionary):
        raise KeyError("The dictionary does not have that many indices.")
    
    for Key in Dictionary.keys():
        if Count == Index:
            return str(Key)
        Count += 1

def Count_Specific_Key(List_Of_Dictionaries: list[dict], Key: str) -> int:

    """
    Count how many dictionaries contain a specific key.

    Parameters:
    - List_Of_Dictionaries (list[dict]): The list of dictionaries to 
      search.
    - Key (str): The key to count occurrences of.

    Returns:
    - int: The count of dictionaries containing the specified key.

    """

    Count = 0
    for Dictionary in List_Of_Dictionaries:
        if Key in Dictionary:
            Count += 1
    return Count
