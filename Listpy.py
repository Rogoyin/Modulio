import numpy as np
import re
import itertools

def Verify_Iterable_Elements_Of_List(List: list):

    '''
    Verifies if all elements in a list are iterable types (list, tuple, dict).

    This function checks each element in the provided list to ensure 
    that it is an instance of an iterable type. If all elements are 
    iterable, the function returns True; otherwise, it returns False.

    Parameters:
    -----------
    List : list
        A list of elements to verify.

    Returns:
    --------
    bool
        True if all elements are iterable, False otherwise.

    Example:
    ---------
    >>> result = Verify_Iterable_Elements_Of_List([[1, 2], (3, 4), {}])
    >>> print(result)
    True

    '''

    for Element in List:
        if not isinstance(Element, (list, tuple, dict)):
            return False
    return True

def Convert_List_Of_Tuples_To_List_Of_List(Tuples_List: list):

    '''
    Converts a list of tuples to a list of lists.

    This function takes a list of tuples as input and converts each 
    tuple into a list. If the input contains non-iterable elements, 
    it returns the original list as a list.

    Parameters:
    -----------
    Tuples_List : list
        A list of tuples to convert.

    Returns:
    --------
    list
        A list of lists if all elements are tuples; otherwise, 
        returns the original list.

    Example:
    ---------
    >>> result = Convert_List_Of_Tuples_To_List_Of_List([(1, 2), (3, 4)])
    >>> print(result)
    [[1, 2], [3, 4]]
    '''

    if Verify_Iterable_Elements_Of_List(Tuples_List):
        Lists_List = []
        for Tuple in Tuples_List:
            Lists_List.append(list(Tuple))
        return Lists_List
    else:
        return list(Tuples_List)

def Find_Max_Position_In_Segment(List: list, Start_Index: int, End_Index: int) -> int:

    '''
    Finds the position of the maximum value within a specified segment of a list.

    This function determines the index of the maximum value in a 
    segment of the provided list, defined by the start and end 
    indices.

    Parameters:
    -----------
    List : list
        The list from which the maximum value's position will be found.

    Start_Index : int
        The starting index of the segment.

    End_Index : int
        The ending index of the segment.

    Returns:
    --------
    int
        The index of the maximum value within the specified segment.

    Example:
    ---------
    >>> result = Find_Max_Position_In_Segment([1, 3, 2, 5, 4], 1, 3)
    >>> print(result)
    3

    '''

    Segment = List[Start_Index:End_Index + 1]
    return Segment.index(max(Segment))

def Sort_Lists_By_Reference(Reference_List: list, *Lists_To_Sort: list) -> tuple:

    '''
    Sorts a reference list and other associated lists based on the order of the reference list.

    This function sorts the provided reference list in ascending 
    order and rearranges the other lists according to the new order 
    of the reference list.

    Parameters:
    -----------
    Reference_List : list
        The list to be sorted, which dictates the order of sorting 
        for the other lists.

    *Lists_To_Sort : list
        Additional lists that will be sorted in the same order as 
        the reference list.

    Returns:
    --------
    tuple
        A tuple containing the sorted reference list and the 
        associated sorted lists.

    Example:
    ---------
    >>> ref_list, sorted_lists = Sort_Lists_By_Reference([3, 1, 2], [30, 10, 20])
    >>> print(ref_list, sorted_lists)
    [1, 2, 3], ([10, 20, 30],)

    '''

    Current_Index = len(Reference_List) - 1

    while Current_Index > 0:
        Max_Position = Find_Max_Position_In_Segment(Reference_List, 0, Current_Index)
        Reference_List[Max_Position], Reference_List[Current_Index] = Reference_List[Current_Index], Reference_List[Max_Position]
        
        for List in Lists_To_Sort:
            List[Max_Position], List[Current_Index] = List[Current_Index], List[Max_Position]
        
        Current_Index -= 1
        
    return Reference_List, tuple(Lists_To_Sort)

def Calculate_Average_Of_Lists(List_Of_Lists: list) -> list:

    '''
    Calculates the average of each list within a list of lists.

    This function computes the average value of each sublist in the 
    provided list of lists.

    Parameters:
    -----------
    List_Of_Lists : list
        A list containing multiple lists for which averages will be 
        calculated.

    Returns:
    --------
    list
        A list of average values corresponding to each sublist.

    Example:
    ---------
    >>> averages = Calculate_Average_Of_Lists([[1, 2, 3], [4, 5, 6]])
    >>> print(averages)
    [2.0, 5.0]

    '''

    Averages = [np.mean(List) for List in List_Of_Lists]
    return Averages

def Transpose_List_Of_Lists(List_Of_Lists: list) -> list:

    '''
    Transposes a list of lists, converting rows to columns and vice versa.

    This function rearranges the provided list of lists so that the 
    first sublist becomes the first column, the second sublist becomes 
    the second column, and so on.

    Parameters:
    -----------
    List_Of_Lists : list
        A list of lists to be transposed.

    Returns:
    --------
    list
        A new list of lists that represents the transposed version of 
        the input list.

    Example:
    ---------
    >>> transposed = Transpose_List_Of_Lists([[1, 2, 3], [4, 5, 6]])
    >>> print(transposed)
    [[1, 4], [2, 5], [3, 6]]

    '''

    Transposed_List = list(map(list, zip(*List_Of_Lists)))
    return Transposed_List

def Slice_Iterable_By_Reference(Iterable, Base_Element, Remove = 'Before', 
                                Include = True, Appears = 1):

    '''
    Slices an iterable based on the position of a specified base element.

    This function modifies the provided iterable by slicing it 
    according to the first occurrence of a specified element. The 
    slicing can either remove elements before or after the base 
    element.

    Parameters:
    -----------
    Iterable : iterable
        The iterable to be sliced.

    Base_Element : object
        The element that serves as the reference point for slicing.

    Remove : str
        Indicates whether to remove elements 'Before' or 'After' the 
        base element. Default is 'Before'.

    Include : bool
        Indicates whether to include the base element in the result. 
        Default is True.

    Appears : int
        The occurrence of the base element to be used for slicing. 
        Default is 1.

    Returns:
    --------
    iterable
        The sliced iterable.

    Raises:
    -------
    KeyError
        If the base element is not found in the iterable.

    Example:
    ---------
    >>> result = Slice_Iterable_By_Reference([1, 2, 3, 4], 3)
    >>> print(result)
    [4]

    '''

    if Base_Element not in Iterable:
        raise KeyError('The element must be in the iterable.')
    
    Count = 0
    for Index, Element in enumerate(Iterable):
        if Element == Base_Element:
            Count += 1
            if Count == Appears:
                if Remove == 'Before':
                    if Include == False:
                        Index += 1
                    Iterable = Iterable[Index:]
                else:
                    if Include:
                        Index += 1
                    Iterable = Iterable[:Index]
    return Iterable

def Get_Index_Of_All_Ocurrences(Iterable, Target_Element) -> list:

    '''
    Retrieves the indices of all occurrences of a specified element in an iterable.

    This function iterates through the provided iterable and collects 
    the indices where the target element appears.

    Parameters:
    -----------
    Iterable : iterable
        The iterable in which to search for the target element.

    Target_Element : object
        The element whose indices are to be found.

    Returns:
    --------
    list
        A list of indices where the target element occurs.

    Example:
    ---------
    >>> indices = Get_Index_Of_All_Ocurrences([1, 2, 3, 2, 4], 2)
    >>> print(indices)
    [1, 3]

    '''

    Count = 1
    Occurrences = []

    for Index, Element in enumerate(Iterable):
        if Element == Target_Element:
            Occurrences.append(Index)
            Count += 1
    
    return Occurrences

def Find_And_Replace(Iterable, Target_Element, New_Value, Occurrence = 1):

    '''
    Finds and replaces a specified occurrence of an element in an iterable.

    This function searches for the target element within the iterable 
    and replaces the specified occurrence with a new value.

    Parameters:
    -----------
    Iterable : iterable
        The iterable in which to find and replace the target element.

    Target_Element : object
        The element to be replaced.

    New_Value : object
        The value that will replace the target element.

    Occurrence : int
        The specific occurrence of the target element to replace. 
        Default is 1.

    Returns:
    --------
    iterable
        The modified iterable after replacement.

    Raises:
    -------
    KeyError
        If the target element does not appear the specified number of times.

    Example:
    ---------
    >>> modified = Find_And_Replace([1, 2, 2, 3], 2, 5, 1)
    >>> print(modified)
    [1, 5, 2, 3]

    '''

    Occurrences_Index = Get_Index_Of_All_Ocurrences(Iterable, Target_Element)
    if Occurrence > len(Occurrences_Index):
        raise KeyError(f"El elemento target {Target_Element} no aparece {Occurrence} veces: aparece menos.")
    
    Index_To_Change = Occurrences_Index[Occurrence - 1]
    Iterable[Index_To_Change] = New_Value
    return Iterable

def Get_Index_Sublist(List, Sublist):

    '''
    Retrieves the indices of all occurrences of a specified sublist within a list.

    This function searches for the provided sublist in the main list 
    and returns the starting indices of each occurrence.

    Parameters:
    -----------
    List : list
        The list in which to search for the sublist.

    Sublist : list
        The sublist to find within the main list.

    Returns:
    --------
    list
        A list of starting indices where the sublist occurs.

    Example:
    ---------
    >>> indices = Get_Index_Sublist([1, 2, 3, 2, 4], [2])
    >>> print(indices)
    [1, 3]
    '''

    List_Of_Index = []
    for Index, Element in enumerate(List):
        if Element == Sublist[0]:
            if List[Index:Index+len(Sublist)] == Sublist:
                List_Of_Index.append(Index)
    return List_Of_Index

def Filter_List_By_Criteria(List: list, Criteria: str = "=", Value = None, Value2 = None):

    '''
    Filters a list based on specified criteria.

    This function iterates through the input list and applies the 
    given criteria to filter the elements. The filtered elements 
    are returned in a new list.

    Parameters:
    -----------
    List : list
        The list to be filtered.

    Criteria : str
        The criteria to apply for filtering. It can be one of: 
        =, !=, >, <, <=, >=, 
        Contains, Not Contains, Starts With, Ends With, In, Not In, 
        Is Instance, Between, Length, Is None, Is Not None, Modulo, 
        Regex, All True, Any True, Custom Function, Type Equals, 
        Within Range. Default is "=".

    Value : object
        The value to compare against based on the specified criteria. 

    Value2 : object
        A second value to use for certain criteria, such as 'Between' 
        or 'Length'.

    Returns:
    --------
    list
        A new list containing elements that meet the specified criteria.

    Raises:
    -------
    KeyError
        If an unsupported criteria is specified.

    Example:
    ---------
    >>> filtered = Filter_List_By_Criteria([1, 2, 3, 4], Criteria='>', Value=2)
    >>> print(filtered)
    [3, 4]

    '''

    Final_List = []
    
    for Element in List:
        if Criteria == "=":
            if Element == Value:
                Final_List.append(Element)
        elif Criteria == "!=":
            if Element != Value:
                Final_List.append(Element)
        elif Criteria == ">":
            if Element > Value:
                Final_List.append(Element)
        elif Criteria == "<":
            if Element < Value:
                Final_List.append(Element)
        elif Criteria == ">=":
            if Element >= Value:
                Final_List.append(Element)
        elif Criteria == "<=":
            if Element <= Value:
                Final_List.append(Element)
        elif Criteria == "Contains":
            if isinstance(Element, str) and isinstance(Value, str) and Value in Element:
                Final_List.append(Element)
        elif Criteria == "Not Contains":
            if isinstance(Element, str) and isinstance(Value, str) and Value not in Element:
                Final_List.append(Element)
        elif Criteria == "Starts With":
            if isinstance(Element, str) and isinstance(Value, str) and Element.startswith(Value):
                Final_List.append(Element)
        elif Criteria == "Ends With":
            if isinstance(Element, str) and isinstance(Value, (str, tuple)) and Element.endswith(Value):
                Final_List.append(Element)
        elif Criteria == "In":
            if Element in Value:
                Final_List.append(Element)
        elif Criteria == "NotIn":
            if Element not in Value:
                Final_List.append(Element)
        elif Criteria == "Is Instance":
            if Value is not None and isinstance(Value, type) and isinstance(Element, Value):
                Final_List.append(Element)
        elif Criteria == "Between":
            if Value <= Element <= Value2:
                Final_List.append(Element)
        elif Criteria == "Length":
            if hasattr(Element, '__len__') and len(Element) == Value:
                Final_List.append(Element)
        elif Criteria == "Is None":
            if Element is None:
                Final_List.append(Element)
        elif Criteria == "Is Not None":
            if Element is not None:
                Final_List.append(Element)
        elif Criteria == "Modulo":
            if Element % Value == Value2:
                Final_List.append(Element)
        elif Criteria == "Regex":
            if isinstance(Element, str) and isinstance(Value, (str, re.Pattern)) and re.search(Value, Element):
                Final_List.append(Element)
        elif Criteria == "All True":
            if Value is not None and callable(Value) and all(Value(E) for E in Element):
                Final_List.append(Element)
        elif Criteria == "Any True":
            if Value is not None and callable(Value) and any(Value(E) for E in Element):
                Final_List.append(Element)
        elif Criteria == "Custom Function":
            if Value is not None and callable(Value) and Value(Element):
                Final_List.append(Element)
        elif Criteria == "Type Equals":
            if type(Element) == Value:
                Final_List.append(Element)
        elif Criteria == "Within Range":
            if Value < Element < Value2:
                Final_List.append(Element)
        else:
            raise KeyError("The criteria must be one of: =, !=, >, <, <=, >=, Contains, Not Contains, Starts With, Ends With, In, Not In, Is Instance, Between, Length, Is None, Is Not None, Modulo, Regex, All True, Any True, Custom Function, Type Equals, Within Range.")
    
    return Final_List

def Remove_Duplicates_In_List(List: list):

    '''
    Removes duplicate elements from a list.

    This function iterates through the provided list and returns a 
    new list that contains only unique elements.

    Parameters:
    -----------
    List : list
        The list from which duplicates should be removed.

    Returns:
    --------
    list
        A new list containing only unique elements.

    Example:
    ---------
    >>> unique_list = Remove_Duplicates_In_List([1, 2, 2, 3])
    >>> print(unique_list)
    [1, 2, 3]

    '''

    List_Without_Duplicates = []
    Seen = set()  # For optimized searches.
    for Element in List:
        if Element not in Seen:
            List_Without_Duplicates.append(Element)
            Seen.add(Element)
    
    return List_Without_Duplicates

def Find_Element(List: list, Value_Element: object, Get_Index: bool = False):

    '''
    Finds an element in a list and optionally retrieves its index.

    This function checks if the specified value is present in the 
    provided list. If Get_Index is True, it returns the indices of 
    all occurrences; otherwise, it returns a boolean indicating 
    presence.

    Parameters:
    -----------
    List : list
        The list in which to search for the specified value.

    Value_Element : object
        The value to search for in the list.

    Get_Index : bool
        Whether to return the indices of occurrences instead of a 
        boolean. Default is False.

    Returns:
    --------
    bool or list
        True if the element is found (and Get_Index is False); 
        otherwise, a list of indices if Get_Index is True.

    Example:
    ---------
    >>> result = Find_Element([1, 2, 3], 2)
    >>> print(result)
    True

    >>> indices = Find_Element([1, 2, 3, 2], 2, True)
    >>> print(indices)
    [1, 3]

    '''

    Index_List = []

    for Index, Element in enumerate(List):
        if Value_Element == Element:
            if Get_Index == False:
                return True
            else:
                Index_List.append(Index)
    
    if Index_List is None:
        return False
    else:
        return Index_List

def Max_Characters(Iterable):

    '''
    Finds the maximum number of characters among the elements in an iterable.

    This function calculates the maximum length of string representations 
    of the elements in the provided iterable.

    Parameters:
    -----------
    Iterable : iterable
        The iterable containing elements to evaluate.

    Returns:
    --------
    int
        The maximum number of characters among the elements.

    Example:
    ---------
    >>> max_chars = Max_Characters([1, 'abc', 3.14159])
    >>> print(max_chars)
    5

    '''

    Max_Characters = 0

    for Element in Iterable:
        Characters = len(str(Element))

        if Characters > Max_Characters:
            Max_Characters = Characters   

    return Max_Characters

def Generate_All_Combinations(List: list, Elements: int):

    '''
    Generates all combinations of a specified length from a list.

    This function returns all possible combinations of a given size 
    from the input list.

    Parameters:
    -----------
    List : list
        The list from which combinations will be generated.

    Elements : int
        The number of elements in each combination.

    Returns:
    --------
    list
        A list of tuples representing all possible combinations.

    Raises:
    -------
    ValueError
        If the number of elements is greater than the length of the list.

    Example:
    ---------
    >>> combinations = Generate_All_Combinations([1, 2, 3, 4], 2)
    >>> print(combinations)
    [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    
    '''

    if Elements > len(List):
        raise ValueError("El número de elementos no puede ser mayor que la longitud de la lista.")

    List_Of_Combinations = list(itertools.combinations(List, Elements))

    return List_Of_Combinations