import numpy as np
import re
import itertools

def Verify_Iterable_Elements_Of_List(List: list):
    for Element in List:
        if not isinstance(Element, (list, tuple, dict)):
            return False
    return True

def Convert_List_Of_Tuples_To_List_Of_List(Tuples_List: list):
    if Verify_Iterable_Elements_Of_List(Tuples_List):
        Lists_List = []
        for Tuple in Tuples_List:
            Lists_List.append(list(Tuple))
        return Lists_List
    else:
        return list(Tuples_List)

def Find_Max_Position_In_Segment(List: list, Start_Index: int, End_Index: int) -> int:

    '''
    Find the position of the maximum value within a specified segment of a list.

    '''

    Segment = List[Start_Index:End_Index + 1]
    return Segment.index(max(Segment))

def Sort_Lists_By_Reference(Reference_List: list, *Lists_To_Sort: list) -> tuple:

    '''
    Sort a reference list and other associated lists based on the order of the reference list.

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
    Calculate the average of each list within a list of lists.

    '''

    Averages = [np.mean(List) for List in List_Of_Lists]
    return Averages

def Transpose_List_Of_Lists(List_Of_Lists: list) -> list:

    '''
    Transpose a list of lists, converting rows to columns and vice versa.

    '''

    Transposed_List = list(map(list, zip(*List_Of_Lists)))
    return Transposed_List

def Slice_Iterable_By_Reference(Iterable, Base_Element, Remove = 'Before', Include = True, Appears = 1):

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
    Count = 1
    Occurrences = []

    for Index, Element in enumerate(Iterable):
        if Element == Target_Element:
            Occurrences.append(Index)
            Count += 1
    
    return Occurrences

def Find_And_Replace(Iterable, Target_Element, New_Value, Occurrence = 1):
    Occurrences_Index = Get_Index_Of_All_Ocurrences(Iterable, Target_Element)
    if Occurrence > len(Occurrences_Index):
        raise KeyError(f"El elemento target {Target_Element} no aparece {Occurrence} veces: aparece menos.")
    
    Index_To_Change = Occurrences_Index[Occurrence - 1]
    Iterable[Index_To_Change] = New_Value
    return Iterable

def Get_Index_Sublist(List, Sublist):
    # Se puede optimizar.
    List_Of_Index = []
    for Index, Element in enumerate(List):
        if Element == Sublist[0]:
            if List[Index:Index+len(Sublist)] == Sublist:
                List_Of_Index.append(Index)
    return List_Of_Index

def Filter_List_By_Criteria(List: list, Criteria: str = "=", Value = None, Value2 = None):

    '''
    Example:

    Filter_List_By_Criteria([1,2,3,4], Criteria = 'Custom Function', Value = lambda x: x % 2 == 0, Value2 = None)
    Result: [2, 4]
    
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
            if isinstance(Element, str) and Value in Element:
                Final_List.append(Element)
        elif Criteria == "Not Contains":
            if isinstance(Element, str) and Value not in Element:
                Final_List.append(Element)
        elif Criteria == "Starts With":
            if isinstance(Element, str) and Element.startswith(Value):
                Final_List.append(Element)
        elif Criteria == "Ends With":
            if isinstance(Element, str) and Element.endswith(Value):
                Final_List.append(Element)
        elif Criteria == "In":
            if Element in Value:
                Final_List.append(Element)
        elif Criteria == "NotIn":
            if Element not in Value:
                Final_List.append(Element)
        elif Criteria == "Is Instance":
            if isinstance(Element, Value):
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
            if isinstance(Element, str) and re.search(Value, Element):
                Final_List.append(Element)
        elif Criteria == "All True":
            if all(Value(E) for E in Element):
                Final_List.append(Element)
        elif Criteria == "Any True":
            if any(Value(E) for E in Element):
                Final_List.append(Element)
        elif Criteria == "Custom Function":
            if Value(Element):
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
    List_Without_Duplicates = []
    Seen = set()  # For optimized searches.
    for Element in List:
        if Element not in Seen:
            List_Without_Duplicates.append(Element)
            Seen.add(Element)
    
    return List_Without_Duplicates

def Find_Element(List: list, Value_Element: object, Get_Index: bool = False):

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
    Max_Characters = 0

    for Element in Iterable:
        Characters = len(str(Element))

        if Characters > Max_Characters:
            Max_Characters = Characters   

    return Max_Characters

def Generate_All_Combinations(List: list, Elements: int):

    if Elements > len(List):
        raise ValueError("El número de elementos no puede ser mayor que la longitud de la lista.")

    List_Of_Combinations = list(itertools.combinations(List, Elements))

    return List_Of_Combinations