import pandas as pd
from typing import Any, Dict, List, Set

def Group_Dictionaries_By_Parent_Element(Data_Frame: pd.DataFrame, Element_List: List[str], Parent_Element: str, Child_List: List[str]) -> List[List[Dict[str, str]]]:

    """
    Groups dictionaries containing child elements for each parent element.

    Parameters:
        Data_Frame: The DataFrame containing the data.
        Element_List: A list of parent element values to group by.
        Parent_Element: The column name to use as the parent element.
        Child_List: A list of child element names to extract.

    Returns:
        A list of grouped dictionaries for each parent element.

    Example:
        >>> Parent_Element = 'Name'
        >>> Element_List = ['Jorge', 'Ramón']
        >>> Child_List = ['Age', 'City']
        >>> Group_Dictionaries_By_Parent_Element(
        ...     Data_Frame, Element_List, Parent_Element, Child_List
        ... )
        [['Jorge', {'Age': 26}, {'City': 'Buenos Aires'}], 
         ['Ramón', {'Age': 28}, {'City': 'Rio de Janeiro'}]]

    """

    Result = []

    for Parent in Element_List:
        Data_By_Element = [{Parent_Element: Parent}]

        for Index, Row in Data_Frame.iterrows():
            if Parent == Row[Parent_Element]:
                Dictionary = {Child: Row[Child] for Child in Child_List}
                Data_By_Element.append(Dictionary)
        
        Result.append(Data_By_Element)

    return Result

def Get_Keys_By_Value(Dictionary_List: List[Dict[str, Any]], Value: Any) -> List[str]:

    """
    Extract keys corresponding to a specific value from a list of 
    dictionaries.

    Parameters:
        Dictionary_List (List[Dict[str, Any]]): A list of dictionaries 
        to extract keys from.
        Value (Any): The value for which keys should be extracted.

    Returns:
        List[str]: A list of keys corresponding to the specified value.

    Example:
        >>> Get_Keys_By_Value([{'a': 1, 'b': 2}, {'c': 1}], 1)
        ['a', 'c']

    """

    Keys_List = []

    for Dictionary in Dictionary_List:
        for Key, Dict_Value in Dictionary.items():
            # Append the key if its value matches the specified value.
            if Dict_Value == Value:
                Keys_List.append(Key)

    return Keys_List

def Get_Values_By_Key(Dictionary_List: List[Dict[str, Any]], Key: str) -> List[Any]:

    """
    Extract values corresponding to a specific key from a list of 
    dictionaries.

    Parameters:
        Dictionary_List (List[Dict[str, Any]]): A list of dictionaries 
        to extract values from.
        Key (str): The key for which values should be extracted.

    Returns:
        List[Any]: A list of values corresponding to the specified key.

    Example:
        >>> Get_Values_By_Key([{'a': 1, 'b': 2}, {'a': 3}], 'a')
        [1, 3]

    """

    Values_List = []

    for Dictionary in Dictionary_List:
        # Append the value corresponding to the key to the values list.
        Values_List.append(Dictionary.get(Key))

    return Values_List

def Get_Key_By_Index(Dictionary: Dict[str, Any], Index: int) -> str:

    """
    Retrieve a key from a dictionary by its index.

    Parameters:
        Dictionary (Dict[str, Any]): The dictionary to retrieve the 
        key from.
        Index (int): The index of the key to retrieve.

    Returns:
        str: The key at the specified index.

    Raises:
        KeyError: If the index is out of range.

    Example:
        >>> Get_Key_By_Index({'a': 1, 'b': 2, 'c': 3}, 1)
        'b'

    """

    Count = 0

    if Index >= len(Dictionary):
        # Raise KeyError if index exceeds dictionary length.
        raise KeyError("The dictionary does not have that many indices.")
    
    for Key in Dictionary.keys():
        if Count == Index:
            return str(Key)
        Count += 1

    # This line ensures a string return in case of unexpected issues.
    raise KeyError("Index not found in the dictionary.")

def Get_Value_By_Index(Dictionary: Dict[str, Any], Index: int) -> Any:

    """
    Retrieve a value from a dictionary by its index.

    Parameters:
        Dictionary (Dict[str, Any]): The dictionary to retrieve the 
        value from.
        Index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the specified index.

    Raises:
        IndexError: If the index is out of range.

    Example:
        >>> Get_Value_By_Index({'a': 1, 'b': 2, 'c': 3}, 1)
        2

    """

    Count = 0

    if Index >= len(Dictionary):
        # Raise IndexError if index exceeds dictionary length.
        raise IndexError("The dictionary does not have that many indices.")

    for Value in Dictionary.values():
        if Count == Index:
            return Value
        Count += 1

    # This line ensures a return value in case of unexpected issues.
    raise IndexError("Index not found in the dictionary.")

def Get_Nested_Unique_Keys(Dictionary: Dict[str, Any]) -> Set[str]:

    """
    Collect all unique keys from a nested dictionary recursively.

    Parameters:
        Dictionary (Dict[str, Any]): Input dictionary, potentially 
        nested.

    Returns:
        Set[str]: Set of all unique keys found in the dictionary.

    Example:
        >>> Get_Nested_Unique_Keys({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
        {'a', 'b', 'c', 'd', 'e'}

    """

    Keys = set(Dictionary.keys())

    for Value in Dictionary.values():
        if isinstance(Value, dict):
            Keys.update(Get_Nested_Unique_Keys(Value))

    return Keys

def Get_Nested_Unique_Values(Dictionary: Dict[str, Any]) -> Set[Any]:

    """
    Collect all unique values from a nested dictionary recursively.

    Parameters:
        Dictionary (Dict[str, Any]): Input dictionary, potentially 
        nested.

    Returns:
        Set[Any]: Set of all unique values found in the dictionary.

    Example:
        >>> Get_Nested_Unique_Values({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
        {1, 2, 3}

    """

    Values = set()

    for Value in Dictionary.values():
        if isinstance(Value, dict):
            # Recursively collect values from nested dictionaries.
            Values.update(Get_Nested_Unique_Values(Value))
        else:
            Values.add(Value)

    return Values

def Get_Unique_Keys_From_Dictionaries(Dictionary_List: List[Dict[str, Any]]) -> List[str]:

    """
    Extract all unique keys from a list of dictionaries.

    Parameters:
        Dictionary_List (List[Dict[str, Any]]): A list of dictionaries 
        to extract keys from.

    Returns:
        List[str]: A list of unique keys found across all dictionaries.

    Example:
        >>> Get_Keys_From_Dictionaries([{'a': 1, 'b': 2}, {'c': 3}])
        ['a', 'b', 'c']

    """

    Keys_Set: Set[str] = set()

    for Dictionary in Dictionary_List:
        # Add all keys from the dictionary to the set.
        Keys_Set.update(Dictionary.keys())

    return list(Keys_Set)

def Rename_Repeated_Keys(Nested_Dict: Dict[str, Any]) -> Dict[str, Any]:

    """
    Recursively renames keys in a nested dictionary if they are repeated 
    across levels. Repeated keys are renamed in the format 
    "Parent_Key_Child_Key".

    Parameters:
        Nested_Dict (Dict[str, Any]): A dictionary that may contain 
        nested dictionaries.

    Returns:
        Dict[str, Any]: A new dictionary with renamed keys as needed.

    Example:
        >>> Rename_Repeated_Keys({"a": 1, "b": {"a": 2}})
        {'a': 1, 'b': {'b_a': 2}}

    """

    Seen_Keys: Set[str] = set()

    def Rename_Keys(Dictionary: Dict[str, Any], Parent_Key: str) -> Dict[str, Any]:
        Updated_Dict = {}

        for Key, Value in Dictionary.items():
            New_Key = Key if Key not in Seen_Keys else f"{Parent_Key}_{Key}"
            Seen_Keys.add(New_Key)

            if isinstance(Value, dict):
                # Recursively rename keys in nested dictionaries.
                Updated_Dict[New_Key] = Rename_Keys(Value, New_Key)
            else:
                Updated_Dict[New_Key] = Value

        return Updated_Dict

    return Rename_Keys(Nested_Dict, Parent_Key="Root")

def Count_Dictionaries_With_Key(List_Of_Dictionaries: List[Dict[str, Any]], Key: str) -> int:

    """
    Count how many dictionaries contain a specific key.

    Parameters:
        List_Of_Dictionaries (List[Dict[str, Any]]): The list of 
        dictionaries to search.
        Key (str): The key to count occurrences of.

    Returns:
        int: The count of dictionaries containing the specified key.

    Example:
        >>> Count_Dictionaries_With_Key([{'a': 1, 'b': 2}, {'b': 3}, {'c': 4}], 'b')
        2

    """

    Count = 0

    for Dictionary in List_Of_Dictionaries:
        if Key in Dictionary:
            # Increment count if the key exists in the dictionary.
            Count += 1

    return Count
