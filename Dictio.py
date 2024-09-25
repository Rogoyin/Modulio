import pandas as pd

def Group_Dictionaries_By_Parent_Element(df: pd.DataFrame, Element_List: list, Parent_Element: str, Child_List: list) -> list:
    
    '''
    Group dictionaries containing child elements for each parent element in a DataFrame.
    
    Example:
    - Parent_Element: 'Name'.
    - Element_List: ['Jorge', 'Ramón']
    - Child_List: ['Age', 'City']
    - Result: dict: [['Jorge', {'Age': 26}, {'City': 'Buenos Aires'}], 
                     ['Ramón', {'Age': 28}, {'City': 'Rio de Janeiro'}]

    '''

    Result = []

    for Element in Element_List:
        Data_By_Element = [f'{Element}']

        for Index, Row in df.iterrows():
            if Element == Row[Parent_Element]:
                Dictionary = {Child: Row[Child] for Child in Child_List}
                Data_By_Element.append(Dictionary)
        
        Result.append(Data_By_Element)
    
    return Result

def Get_Values_By_Key(Dict_List: list, Key: str) -> list:

    """
    Extracts values corresponding to a specific key from a list of dictionaries.
    
    """

    Values_List = []
    for Dict in Dict_List:
        Values_List.append(Dict[Key])
    return Values_List

def Get_Key_By_Index(Dictionary: dict, Index: int):
    Count = 0
    if Index > len(Dictionary):
        raise KeyError("El diccionario no tiene tantos index como los que pusiste.")
    for Key in Dictionary.keys():
        if Count == Index:
            return Key
        else:
            return None

def Count_Specific_Key(List_Of_Dictionaries: dict, Key):
    Count = 0
    for Dictionary in List_Of_Dictionaries:
        if Key in Dictionary:
            Count += 1
    return Count