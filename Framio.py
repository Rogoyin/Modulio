import pandas as pd
import re
import Stringio
from typing import List, Callable, Optional

def Match_And_Copy_Column_Values(df1: pd.DataFrame, df2: pd.DataFrame, 
                                 Column_df1_A: str, Column_df1_B: str, 
                                 Column_df2_A: str, Column_df2_B: str) -> pd.DataFrame:
    
    """
    Compare values from two DataFrames and copy values from one column 
    to another based on matching criteria.

    This function compares values in Column_df1_A from df1 with 
    values in Column_df2_A from df2. If a match is found, the 
    corresponding value from Column_df2_B in df2 is copied into 
    Column_df1_B in df1. If the specified columns are identical, 
    their names are modified to avoid conflicts.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame containing the columns for comparison 
        and value copying.
    df2 : pd.DataFrame
        The second DataFrame containing the values to be copied 
        based on matches found in df1.
    Column_df1_A : str
        The name of the column in df1 used for comparison.
    Column_df1_B : str
        The name of the column in df1 where values will be copied.
    Column_df2_A : str
        The name of the column in df2 used for comparison.
    Column_df2_B : str
        The name of the column in df2 from which values will be copied.

    Returns
    -------
    pd.DataFrame
        The modified df1 DataFrame with updated values in 
        Column_df1_B where matches were found.

    Notes
    -----
    - If Column_df1_A matches Column_df2_A, the column in df2 is 
      renamed with a suffix "_R" to prevent naming conflicts.
    - Similarly, if Column_df1_B matches Column_df2_B, the column 
      in df2 is renamed with a suffix "_R".
    - This function performs a nested loop comparison and may 
      not be efficient for large DataFrames.
    
    Example
    -------
    >>> df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [None, None, None]})
    >>> df2 = pd.DataFrame({'A': [1, 2], 'B': ['X', 'Y']})
    >>> result = Match_And_Copy_Column_Values(df1, df2, 'A', 'B', 'A', 'B')
    >>> print(result)
       A    B
    0  1    X
    1  2    Y
    2  3  None
    """

    if Column_df1_A == Column_df2_A:
        df2 = df2.rename(columns={Column_df2_A: f"{Column_df2_A}_R"})
        Column_df2_A = f"{Column_df2_A}_R"
    if Column_df1_B == Column_df2_B:
        df2 = df2.rename(columns={Column_df2_B: f"{Column_df2_B}_R"})
        Column_df2_B = f"{Column_df2_B}_R"
    
    for i in range(len(df1)):
        Element_Compared_1 = df1[Column_df1_A][i]
        
        for k in range(len(df2)):
            Element_Compared_2 = df2[Column_df2_A][k]

            if Element_Compared_1 == Element_Compared_2:
                df1.at[i, Column_df1_B] = df2.at[k, Column_df2_B]
    
    return df1

def Compare_Columns(df1: pd.DataFrame, Column1: str, 
                    df2: pd.DataFrame, Column2: str, 
                    Label1: str = "df1", Label2: str = "df2") -> pd.DataFrame:
    """
    Compare two specified columns from two DataFrames and identify the 
    unique values present in each column but not in the other. This 
    function helps analyze differences between two datasets.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame containing the column to be compared.
    Column1 : str
        The name of the column in df1 to compare.
    df2 : pd.DataFrame
        The second DataFrame containing the column to be compared.
    Column2 : str
        The name of the column in df2 to compare.
    Label1 : str, optional
        A label to identify df1 in the result. Default is "df1".
    Label2 : str, optional
        A label to identify df2 in the result. Default is "df2".

    Returns
    -------
    pd.DataFrame
        A DataFrame containing two columns: 'Valor' and 'DataFrame'.
        - 'Valor' contains the unique values found in Column1 or 
          Column2 that are not present in the other column.
        - 'DataFrame' indicates the source DataFrame of each unique 
          value, labeled with Label1 or Label2.

    Notes
    -----
    - The function converts the specified columns into sets to 
      efficiently determine unique values.
    - The resulting DataFrame includes all unique values from both 
      columns with their corresponding labels.
    - If either specified column does not exist in the respective 
      DataFrame, a KeyError will be raised.
    - The maximum number of rows displayed in the result is set to 
      None for full visibility.

    Example
    -------
    >>> df1 = pd.DataFrame({'A': [1, 2, 3, 4]})
    >>> df2 = pd.DataFrame({'B': [3, 4, 5, 6]})
    >>> result = Compare_Columns(df1, 'A', df2, 'B', 
    ...                          Label1="DataFrame1", 
    ...                          Label2="DataFrame2")
    >>> print(result)
          Valor DataFrame
    0      1  DataFrame1
    1      2  DataFrame1
    2      5  DataFrame2
    3      6  DataFrame2
    """
    Column1_Set = set(df1[Column1])
    Column2_Set = set(df2[Column2])
    
    Unique_In_Column1 = Column1_Set - Column2_Set
    Unique_In_Column2 = Column2_Set - Column1_Set
    
    Unique_Values = {
        'Valor': list(Unique_In_Column1) + list(Unique_In_Column2),
        'DataFrame': [Label1] * len(Unique_In_Column1) + [Label2] * len(Unique_In_Column2)
    }
    
    df_Result = pd.DataFrame(Unique_Values)

    pd.set_option('display.max_rows', None)
    
    return df_Result

def Get_Last_Number_Of_String_Column(df: pd.DataFrame, Column_With_Strings: str, New_Column_Name: str) -> pd.DataFrame:
    
    List_Of_Last_Numbers = []
    
    for String in df[Column_With_Strings]:
        Last_List_Of_Last_Numbers = re.findall(r'[\d,]+', String)
        Last_List_Of_Last_Numbers = [float(Character.replace(',', '.')) for Character in Last_List_Of_Last_Numbers]
        List_Of_Last_Numbers.append(Last_List_Of_Last_Numbers)
    
    df[New_Column_Name] = [List[-1] for List in List_Of_Last_Numbers]
    
    return df

def Vertical_Concatenate_For_Multiples_DataFrames(*args) -> pd.DataFrame:
    Mixed = pd.concat(args, ignore_index=True)
    return Mixed

def Fill_Column(df: pd.DataFrame, Column, Value) -> pd.DataFrame:  
    df[Column] = Value
    return df

def Get_Selected_Rows_By_Column(df: pd.DataFrame, Column: str, Value: object, Condition: str = 'Match') -> pd.DataFrame:

    """
    Filters rows in the DataFrame based on the specified condition applied to a column.

    Conditions supported: 'Match', 'Contains', '>', '<', '>=', '<=', '!=', 'Is in', 'Not in', 'Starts with', 
    'Ends with', 'Is null', 'Is not null', 'Between'.

    """

    if Condition == "Match":
        return df[df[Column] == Value]
    
    elif Condition == "Contains":
        return df[df[Column].str.contains(Value, na=False)]

    elif Condition == ">":
        return df[df[Column] > Value]
    
    elif Condition == "<":
        return df[df[Column] < Value]
    
    elif Condition == ">=":
        return df[df[Column] >= Value]
    
    elif Condition == "<=":
        return df[df[Column] <= Value]
    
    elif Condition == "!=":
        return df[df[Column] != Value]
    
    elif Condition == "Is in":
        if isinstance(Value, (list, set, tuple)):  
            return df[df[Column].isin(Value)]
        else:
            raise ValueError(f"Value for 'Is in' condition must be a list, set, or tuple.")
    
    elif Condition == "Not in":
        if isinstance(Value, (list, set, tuple)):  
            return df[~df[Column].isin(Value)]
        else:
            raise ValueError(f"Value for 'Not in' condition must be a list, set, or tuple.")
    
    elif Condition == "Starts with":
        return df[df[Column].str.startswith(Value, na=False)]

    elif Condition == "Ends with":
        return df[df[Column].str.endswith(Value, na=False)]

    elif Condition == "Is null":
        return df[df[Column].isnull()]

    elif Condition == "Is not null":
        return df[df[Column].notnull()]

    elif Condition == "Between":
        if isinstance(Value, (list, tuple)) and len(Value) == 2:
            return df[df[Column].between(Value[0], Value[1])]
        else:
            raise ValueError(f"Value for 'Between' condition must be a list or tuple with two elements.")

    else:
        raise ValueError(f"Condition '{Condition}' is not supported. Use 'Match', 'Contains', '>', '<', '>=', '<=', '!=', 'Is in', 'Not in', 'Starts with', 'Ends with', 'Is null', 'Is not null', 'Between'.")

def Get_Selected_Rows_By_Two_Columns(df: pd.DataFrame, Column1: str, Column2: str, Values: list, Condition: str = 'Match') -> pd.DataFrame:
    
    """
    Filters rows in the DataFrame based on the specified condition applied to two columns.

    Conditions supported: 'Match', 'Contains', '>', '<', '>=', '<=', '!=', 'Is in', 
    'Not in', 'Starts with', 'Ends with', 'Is null', 'Is not null', 'Between', 'Match either'.

    """
    
    if Condition == "Match":
        return df[(df[Column1] == Values[0]) | (df[Column2] == Values[0])]
    
    elif Condition == "Contains":
        return df[(df[Column1].str.contains(Values[0], na=False)) | (df[Column2].str.contains(Values[0], na=False))]

    elif Condition == ">":
        return df[(df[Column1] > Values[0]) | (df[Column2] > Values[0])]
    
    elif Condition == "<":
        return df[(df[Column1] < Values[0]) | (df[Column2] < Values[0])]
    
    elif Condition == ">=":
        return df[(df[Column1] >= Values[0]) | (df[Column2] >= Values[0])]
    
    elif Condition == "<=":
        return df[(df[Column1] <= Values[0]) | (df[Column2] <= Values[0])]
    
    elif Condition == "!=":
        return df[(df[Column1] != Values[0]) | (df[Column2] != Values[0])]
    
    elif Condition == "Is in":
        if isinstance(Values, (list, set, tuple)):
            return df[(df[Column1].isin(Values)) | (df[Column2].isin(Values))]
        else:
            raise ValueError(f"Value for 'Is in' condition must be a list, set, or tuple.")
    
    elif Condition == "Not in":
        if isinstance(Values, (list, set, tuple)):
            return df[~((df[Column1].isin(Values)) | (df[Column2].isin(Values)))]
        else:
            raise ValueError(f"Value for 'Not in' condition must be a list, set, or tuple.")
    
    elif Condition == "Starts with":
        return df[(df[Column1].str.startswith(Values[0], na=False)) | (df[Column2].str.startswith(Values[0], na=False))]

    elif Condition == "Ends with":
        return df[(df[Column1].str.endswith(Values[0], na=False)) | (df[Column2].str.endswith(Values[0], na=False))]

    elif Condition == "Is null":
        return df[df[Column1].isnull() | df[Column2].isnull()]

    elif Condition == "Is not null":
        return df[df[Column1].notnull() & df[Column2].notnull()]

    elif Condition == "Between":
        if isinstance(Values, (list, tuple)) and len(Values) == 2:
            return df[(df[Column1].between(Values[0], Values[1])) | (df[Column2].between(Values[0], Values[1]))]
        else:
            raise ValueError(f"Value for 'Between' condition must be a list or tuple with two elements.")

    elif Condition == "Match either":
        if isinstance(Values, (list, set, tuple)):
            return df[(df[Column1].isin(Values)) & (df[Column2].isin(Values))]
        else:
            raise ValueError(f"Value for 'Match either' condition must be a list, set, or tuple.")
    
    else:
        raise ValueError(f"Condition '{Condition}' is not supported. Use 'Match', 'Contains', '>', '<', '>=', '<=', '!=', 'Is in', 'Not in', 'Starts with', 'Ends with', 'Is null', 'Is not null', 'Between', 'Match either'.")

def Add_Word_To_Name_Columns(df, Word = None, Separator = '_'):

    if Word == None:
        Word = f'{df}'

    Columns = df.columns.to_list()
    Renaming = {}

    for Column in Columns:
        Renaming[Column] = Stringio.Remove_Acents(Column) + Separator + Word
    
    df.rename(columns=Renaming, inplace=True)

    return df

def Update_Column_Selected_Rows(df: pd.DataFrame, Condition_Column: str, Condition_Value: object, 
                                      Update_Column: str, Update_Value: object, Condition: str) -> pd.DataFrame:
    
    """
    Updates values in a specified column based on a condition applied to another column.

    """

    Filtered_Rows = Get_Selected_Rows_By_Column(df, Condition_Column, Condition_Value, Condition=Condition)
    df.loc[Filtered_Rows.index, Update_Column] = Update_Value
    return df

def Drop_Selected_Rows(df: pd.DataFrame, Column: str, Value: object, Condition: str = 'Match') -> pd.DataFrame:

    """
    Drops rows where a specified column meets a certain condition.

    """

    Filtered_Rows = Get_Selected_Rows_By_Column(df, Column, Value, Condition=Condition)
    df = df.drop(Filtered_Rows.index)
    return df

def Fill_Missing_Values(df: pd.DataFrame, Column: str, Method: str = None, Fill_Value: object = None) -> pd.DataFrame:

    """
    Fills missing values in a specified column using a given method or fill value.

    """

    if Method:
        df[Column] = df[Column].fillna(method=Method)

    elif Fill_Value:
        df[Column] = df[Column].fillna(value=Fill_Value)
    else:
        raise ValueError("Either 'Method' or 'Fill_Value' must be provided.")
    return df

def Apply_Operation_To_Columns(df: pd.DataFrame, Columns: List[str], Operations: Optional[List[Callable]] = None) -> pd.DataFrame:

    """
    Processes specified columns by applying a series of transformations and conversions.

    Example:

    df = Apply_Operation_To_Columns(df,
                            Columns=['Name', 'City', 'Country'],
                            Operations=[lambda x: x.upper(),
                                        Remove_Vocals])

        Upper the text and remove all vocals of these columns.

    """

    for Column in Columns:
        for Operation in Operations:
            df[Column] = df[Column].apply(Operation)
    return df

def Apply_Operations_To_Selected_Rows(df: pd.DataFrame, Filtered_Column: str, Filter_Value: object, Condition: str, 
                                      Columns_To_Operate: List[str], Operations: List[Callable]) -> pd.DataFrame:
    
    """
    Applies specified operations to selected columns for rows 
    filtered by a given condition.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to apply operations on.

    Filtered_Column : str
        The name of the column used to filter rows.

    Filter_Value : object
        The value to filter the rows in the specified column.

    Condition : str
        The condition to be applied for filtering rows (e.g., 
        '==', '>', '<', etc.).

    Columns_To_Operate : List[str]
        A list of column names on which to apply the operations.

    Operations : List[Callable]
        A list of functions to apply to the selected columns.

    Returns:
    --------
    pd.DataFrame
        The DataFrame after applying the specified operations 
        to the selected rows and columns.

    Notes:
    ------
    - The original index of the DataFrame is preserved during 
      the operation for correct ordering.
    - The function assumes that the operations provided are 
      compatible with the data types in the specified columns.

    Example:
    ---------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> operations = [lambda x: x * 2]
    >>> result = Apply_Operations_To_Selected_Rows(
    ...     df, 'A', 2, '>', ['B'], operations)
    >>> print(result)
       A  B
    0  1  4
    1  2  10
    2  3  12
    """

    df['Original_Index'] = df.index
    Filtered_Rows = Get_Selected_Rows_By_Column(df, Filtered_Column, Filter_Value, Condition=Condition)

    for Operation in Operations:
        for Column in Columns_To_Operate:
            df.loc[Filtered_Rows.index, Column] = Filtered_Rows[Column].apply(Operation)

    df = df.sort_values(by='Original_Index').drop(columns='Original_Index').reset_index(drop=True)

    return df

def Find_Best_Value_Column(
    df: pd.DataFrame,
    Target_Column: str,
    Columns_To_Compare: List[str],
    Best_Value_Column: str,
    Comparison_Function: Optional[Callable[[pd.Series, pd.Series], bool]] = None
) -> pd.DataFrame:
    
    """
    Identifies the best value from specified columns based on a 
    comparison function.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the data.

    Target_Column : str
        The column where the target value is stored.

    Columns_To_Compare : List[str]
        List of column names to compare against the target value.

    Best_Value_Column : str
        The name of the column where the best value will be stored.

    Comparison_Function : Optional[Callable]
        Optional function to determine if a value is better. 
        Defaults to equality comparison. The function must accept 
        two arguments (the target value and the comparison column 
        value) and return a boolean.

    Returns:
    --------
    pd.DataFrame
        The modified DataFrame with the Best_Value_Column updated 
        to the best value based on the comparison function.

    Example:
    ---------
    >>> df = Find_Best_Value_Column(df,
...                        Target_Column='Precio',
...                        Columns_To_Compare=['Proveedor1', 
...                                            'Proveedor2', 
...                                            'Proveedor3'],
...                        Best_Value_Column='Mejor_Proveedor',
...                        Comparison_Function=lambda Target, 
...                        Value: Target == Value
...                              )
    """
    
    if Comparison_Function is None:
        Comparison_Function = lambda Target, Value: Target == Value

    for Index, Row in df.iterrows():
        Best_Value = None
        for Column in Columns_To_Compare:
            if Comparison_Function(Row[Target_Column], Row[Column]):
                Best_Value = Column
                break
        df.at[Index, Best_Value_Column] = Best_Value if Best_Value is not None else pd.NA

    return df

def Convert_Type_Of_Columns(df: pd.DataFrame, List_Of_Columns: list, Type = str):
    for Column in List_Of_Columns:
        if Column in df.columns:
            if df[Column].dtype != Type:
                df[Column] = df[Column].astype(Type)
    return df

def Casing_Column_Names(df: pd.DataFrame, Style: str = 'Pascal Snake Case', Separator: str = "") -> pd.DataFrame:
    Columns = list(df.columns)
    if Style == 'Camel Case':
        Columns = [Stringio.Apply_Camel_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Snake Case':
        Columns = [Stringio.Apply_Snake_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Pascal Snake Case':
        Columns = [Stringio.Apply_Pascal_Snake_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Screaming Snake Case':
        Columns = [Stringio.Apply_Screaming_Snake_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Pascal Case':
        Columns = [Stringio.Apply_Pascal_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Flat Case':
        Columns = [Stringio.Apply_Flat_Case(str(Column), Separator = Separator) for Column in Columns]
    elif Style == 'Upper Flat Case':
        Columns = [Stringio.Apply_Upper_Flat_Case(str(Column), Separator = Separator) for Column in Columns]
    
    df.columns = Columns
    return df

def Change_Column_Names_By_Dictionary(df: pd.DataFrame, Dictionary: dict) -> pd.DataFrame:
    return df.rename(columns=Dictionary)

def Create_Dummy_Variables(DataFrame, Column_Name, Drop_First = False, Group_Others = True, Remove_Others = True, 
                           Threshold = 0.05, Name_Other_Column = "Others", Name_Columns_Style = 'Pascal_Snake_Case', Separator=""):

    """
    Create dummy variables from a categorical column in a DataFrame.

    """

    Dummies = pd.get_dummies(DataFrame[Column_Name], drop_first = Drop_First, prefix = Column_Name)

    if Group_Others:
        # Group infrequent categories into 'Others'
        Frequency = Dummies.sum() / len(DataFrame)
        Rare_Columns = Frequency[Frequency < Threshold].index
        if len(Rare_Columns) > 0:
            Dummies[Name_Other_Column] = Dummies[Rare_Columns].sum(axis = 1)
            Dummies = Dummies.drop(Rare_Columns, axis = 1)

            if Name_Columns_Style:
                Dummies = Casing_Column_Names(Dummies, Style=Name_Columns_Style, Separator=Separator)

    if Remove_Others and Name_Other_Column in Dummies.columns:
        Dummies = Dummies.drop(Name_Other_Column, axis = 1)

    DataFrame_With_Dummies = pd.concat([DataFrame, Dummies], axis = 1)
    DataFrame_With_Dummies = DataFrame_With_Dummies.drop(Column_Name, axis = 1)

    return DataFrame_With_Dummies

def Create_Dummy_Variables_In_All_DataFrame(DataFrame, Drop_First = False, Group_Others = True, Remove_Others = True, 
                                            Threshold = 0.05, Name_Other_Column = "Others"):
    
    Column_Types = DataFrame.dtypes

    for Index, Value in Column_Types.items():
        if Value == 'object':
            DataFrame = Create_Dummy_Variables(DataFrame, Index, Drop_First = Drop_First, Group_Others = Group_Others, Remove_Others = Remove_Others, 
                                               Threshold = Threshold, Name_Other_Column = "Others")
    
    return DataFrame

def Replace_Values_In_Name_Columns(df: pd.DataFrame, Old_Values: str, New_Values: str) -> pd.DataFrame:
    
    if isinstance(Old_Values, str):
        Old_Values = [Old_Values]
    
    if isinstance(New_Values, str):
        New_Values = [New_Values]

    if len(Old_Values) != len(New_Values):
        raise ValueError("Old_Values and New_Values must have the same length.")
    
    for Index, Old_Value in enumerate(Old_Values):
        df.columns = [Column.replace(Old_Value, New_Values[Index]) for Column in df.columns]
    return df

def Get_Duplicates_With_Indices_From_DataFrame(df: pd.DataFrame, Column: str) -> list:

    Duplicates = df[Column].duplicated(keep=False)

    List_Of_Duplicates = []

    for Value in df[Duplicates][Column].unique():
        Duplicate = {}
        Index = df.index[df[Column] == Value].tolist()
        Duplicate[Value] = Index
        List_Of_Duplicates.append(Duplicate)

    return List_Of_Duplicates

def Divide_DataFrames_By_Column(df: pd.DataFrame, Column: str, Condition: str = 'Match') -> dict:

    DataFrames = {}
    Unique_Values = list(df[Column].unique())

    for Value in Unique_Values:
        df_Filtered = Get_Selected_Rows_By_Column(df, Column, Value, Condition = Condition)
        DataFrames[Value] = df_Filtered

    return DataFrames

def Create_Date_Column(df, Day_Column = 'Day', Month_Column = 'Month', Year_Column = 'Year', Spanish = False):

    if Spanish:
        Months_In_Spanish = {
                            'Enero': 1,
                            'Febrero': 2,
                            'Marzo': 3,
                            'Abril': 4,
                            'Mayo': 5,
                            'Junio': 6,
                            'Julio': 7,
                            'Agosto': 8,
                            'Septiembre': 9,
                            'Octubre': 10,
                            'Noviembre': 11,
                            'Diciembre': 12
        }

        df[Month_Column] = df[Month_Column].str.strip()
        df['Month'] = df['Month'].map(Months_In_Spanish)
    
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    return df

def Sort_Columns(df: pd.DataFrame, Order_By: str, Ascending = False):
    Sort_Columns = [Order_By]

    if Order_By == 'Date':
        Sort_Columns.extend(['Hour'])
    elif Order_By == 'Month':
        Sort_Columns.extend(['Date', 'Hour'])
    elif Order_By == 'Year':
        Sort_Columns.extend(['Month', 'Date', 'Hour'])

    df = df.sort_values(by=Sort_Columns, ascending=[Ascending] * len(Sort_Columns))

    return df

# Se puede hacer todavía más personalizada ajustando el marcador: número, letra, a partir de cuál, si salta en múltiplos, etc.
def Divide_Column(df, Column_To_Divide = None, Separator = "_", Column_Names = None, Delete = True):

    Split_Result = df[Column_To_Divide].str.split(Separator, expand = True)
    Number_Of_Columns = Split_Result.shape[1]

    if Column_Names is None or len(Column_Names) != Number_Of_Columns:
        Column_Names = [f"{Column_To_Divide}_{i}" for i in range(1, Number_Of_Columns + 1)]

    df[Column_Names] = Split_Result

    if Delete:
        df = df.drop(columns = [Column_To_Divide])

    return df

def Values_Of_New_Column_By_Compare_Other_Columns(Row, Column1, Value1, Column2, Value2, Value3, Operation=">"):

    """
    Returns a value based on comparing two columns in a DataFrame row.

    """
    
    if Operation == ">":
        if Row[Column1] > Row[Column2]:
            return Value1
        elif Row[Column1] < Row[Column2]:
            return Value2
        else:
            return Value3
    elif Operation == "<":
        if Row[Column1] < Row[Column2]:
            return Value1
        elif Row[Column1] > Row[Column2]:
            return Value2
        else:
            return Value3
    elif Operation == "==":
        if Row[Column1] == Row[Column2]:
            return Value1
        elif Row[Column1] != Row[Column2]:
            return Value2
        else:
            return Value3
    else:
        raise ValueError(f"Operation '{Operation}' is not supported. Use '>', '<', or '=='.")
    
def Remove_Values_Under_Threshold(df, Column, Threshold_Percentage = 5, Threshold_Numeric = None, Remove = True, 
                                  New_Value = 'Others'):

    Uniques = list(df[Column].unique())
    Length = len(df[Column])

    if Threshold_Percentage:
        Threshold = (Length / 100) * Threshold_Percentage
    else:
        Threshold = Threshold_Numeric

    for Value in Uniques:
        Count = (df[Column] == Value).sum()
        if Count < Threshold:
            if Remove:
                df = Drop_Selected_Rows(df, Column, Value)
            else:
                df[Column] = df[Column].replace(Value, New_Value)

    df.reset_index(drop=True, inplace=True)

    return df

def Combine_Columns(df, Column1, Column2, New_Column_Name = None, Criteria = 'Sum', Remove = False):

    if New_Column_Name is None:
        New_Column_Name = Criteria

    elif Criteria == 'Sum':
        if df[Column1].dtype == df[Column2].dtype and df[Column1].dtype in [str, int, float, list, tuple]:
            df[New_Column_Name] = df[Column1] + df[Column2]
        else:
            raise TypeError(f'Column1 and Column2 must have the same type.')

    elif Criteria == 'Difference':
        if pd.api.types.is_numeric_dtype(df[Column1]) and pd.api.types.is_numeric_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] - df[Column2]
        else:
            raise KeyError(f'"Difference" criteria needs numbers.')

    elif Criteria == 'Product':
        if pd.api.types.is_numeric_dtype(df[Column1]) and pd.api.types.is_numeric_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] * df[Column2]
        else:
            raise KeyError(f'"Product" criteria needs numbers.')

    elif Criteria == 'Division':
        if pd.api.types.is_numeric_dtype(df[Column1]) and pd.api.types.is_numeric_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] / df[Column2].replace(0, float('nan'))
        else:
            raise KeyError(f'"Division" criteria needs numbers.')
    
    if Criteria == 'Average':
        if pd.api.types.is_numeric_dtype(df[Column1]) and pd.api.types.is_numeric_dtype(df[Column2]):
            df[New_Column_Name] = (df[Column1] + df[Column2]) / 2
        else:
            raise KeyError(f'"Average" criteria needs numbers, not objects.')

    elif Criteria == 'Concatenate':
        df[New_Column_Name] = df[Column1].astype(str) + df[Column2].astype(str)

    elif Criteria == 'Logical AND':
        if pd.api.types.is_bool_dtype(df[Column1]) and pd.api.types.is_bool_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] & df[Column2]
        else:
            raise KeyError(f'"Logical AND" criteria needs boolean values.')

    elif Criteria == 'Logical OR':
        if pd.api.types.is_bool_dtype(df[Column1]) and pd.api.types.is_bool_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] | df[Column2]
        else:
            raise KeyError(f'"Logical OR" criteria needs boolean values.')

    elif Criteria == 'Logical XOR':
        if pd.api.types.is_bool_dtype(df[Column1]) and pd.api.types.is_bool_dtype(df[Column2]):
            df[New_Column_Name] = df[Column1] ^ df[Column2]
        else:
            raise KeyError(f'"Logical XOR" criteria needs boolean values.')

    elif Criteria == 'Logical NOT':
        if pd.api.types.is_bool_dtype(df[Column1]):
            df[New_Column_Name] = ~df[Column1]
        else:
            raise KeyError(f'"Logical NOT" criteria needs boolean values for Column1.')

    else:
        raise ValueError(f"Criteria '{Criteria}' is not supported.")

    if Remove:
        df = df.drop(columns=[Column1,Column2])

    return df

def Insert_Column_In_Specific_Position(df, Value, Column_Name, Number_Position = None, Before_To = None, After_To = None):

    if (Number_Position and Before_To) or (Number_Position and After_To) or (Before_To and After_To):
        raise KeyError("Please specify only one of the following: Number_Position, Before_To, or After_To.")
    
    if Number_Position is not None:
        df.insert(Number_Position, Column_Name, value=Value)
    
    elif Before_To is not None:
        try:
            Number_Position = list(df.columns).index(Before_To)
            df.insert(Number_Position, Column_Name, value=Value)
        except ValueError:
            raise KeyError(f"Column '{Before_To}' not found in DataFrame.")
    
    elif After_To is not None:
        try:
            Number_Position = list(df.columns).index(After_To) + 1
            df.insert(Number_Position, Column_Name, value=Value)
        except ValueError:
            raise KeyError(f"Column '{After_To}' not found in DataFrame.")
    
    else:
        raise KeyError("You must specify one of the following: Number_Position, Before_To, or After_To.")
    
    return df

def Apply_String_Style_To_All_DataFrame(df, String_Style='Title', Replace_From=None, Replace_To=None):

    for Column in df.columns:
        if df[Column].dtype == 'object':
            if String_Style == 'Title':
                df[Column] = df[Column].str.title()
            elif String_Style == 'Capitalize':
                df[Column] = df[Column].str.capitalize()
            elif String_Style == 'Lower':
                df[Column] = df[Column].str.lower()
            elif String_Style == 'Upper':
                df[Column] = df[Column].str.upper()
            elif String_Style == 'Swapcase':
                df[Column] = df[Column].str.swapcase()
            elif String_Style == 'Strip':
                df[Column] = df[Column].str.strip()
            elif String_Style == 'Replace' and Replace_From is not None and Replace_To is not None:
                df[Column] = df[Column].str.replace(Replace_From, Replace_To)
    
    return df

def Process_DataFrame(df: pd.DataFrame, 
                      Columns: list = [], 
                      Fill_NaN: float = 0, 
                      Dummies: bool = False,
                      String_Style: str = 'None', 
                      Replace: list = [],
                      Case_Name_Columns: str = 'None', 
                      Separator_In_Name_Columns: str = 'None',
                      Remove_Accents_In_Name_Columns: bool = True, 
                      Replace_Enie_In_Name_Columns: bool = True,
                      Replace_In_Name_Columns: list = []):
    """
    Processes a DataFrame by applying various transformations to the data and column names.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame to be processed.
    Columns : list, optional
        List of specific columns to keep in the DataFrame. Default is None (keeps all columns).
    Fill_NaN : int or float, optional
        The value to fill NaN entries in the DataFrame. Default is 0.
    Dummies : bool, optional
        Whether to create dummy variables for all categorical columns in the DataFrame. Default is False.
    String_Style : str, optional
        Style to apply to string entries in the DataFrame. Options include 'Title', 'Upper', 'Lower', etc. Default is 'Title'.
    Replace : list of two lists, optional
        A list containing two lists: one with words to replace and another with their corresponding replacements. Default is None.
    Case_Name_Columns : str, optional
        Case style to apply to the column names. Options include 'Pascal Case', 'snake_case', etc. Default is 'Pascal Snake Case'.
    Separator_In_Name_Columns : str, optional
        Separator to use between words in the column names. Default is '_'.
    Remove_Accents_In_Name_Columns : bool, optional
        Whether to remove accents from the column names (e.g., replace 'á' with 'a'). Default is True.
    Replace_Enie_In_Name_Columns : bool, optional
        Whether to replace 'ñ' in column names with 'ni'. Default is True.
    Replace_In_Name_Columns : list of two lists, optional
        A list containing two lists: one with substrings to replace in column names and another with their corresponding replacements. Default is None.

    Returns:
    --------
    pd.DataFrame
        The processed DataFrame with the applied transformations.

    Notes:
    ------
    - If `Columns` is provided, only those columns will be kept in the DataFrame.
    - NaN values will be filled according to the `Fill_NaN` parameter.
    - If `Dummies` is True, dummy variables will be created for categorical columns.
    - Column names can be transformed to a specific case style and cleaned up by replacing characters such as spaces or special accents.
    - The function supports replacement of specific words or characters both in the DataFrame's data and in the column names.
    """
    if Columns:
        df = df[Columns]

    if Fill_NaN is not None:
        df = df.fillna(Fill_NaN)
    
    if Remove_Accents_In_Name_Columns:
        df = Replace_Values_In_Name_Columns(df, ['á', 'é', 'í', 'ó', 'ú'], ['a', 'e', 'i', 'o', 'u'])
    
    if Separator_In_Name_Columns != 'None':
        Separators = ['-', ' ', '_', '|', ':', ',', '.']
        for Separator in Separators:
            df.columns = df.columns.str.replace(Separator, Separator_In_Name_Columns, regex=False)
            
    if Replace_Enie_In_Name_Columns:
        df = Replace_Values_In_Name_Columns(df, ['ñ'], ['ni'])

    if Dummies:
        df = Create_Dummy_Variables_In_All_DataFrame(df)
    
    if Case_Name_Columns != 'None':
        df = Casing_Column_Names(df, Style = Case_Name_Columns, Separator = Separator_In_Name_Columns)
    
    if String_Style != 'None':
        df = Apply_String_Style_To_All_DataFrame(df, String_Style = String_Style)

    if Replace:
        for Index, Word in enumerate(Replace[0]):
            df = Apply_String_Style_To_All_DataFrame(df, String_Style = 'Replace', Replace_From=Replace[0][Index], 
                                                     Replace_To=Replace[1][Index])
    
    if Replace_In_Name_Columns:
        for Index, Word in enumerate(Replace_In_Name_Columns[0]):
            df = Replace_Values_In_Name_Columns(df, Replace_In_Name_Columns[0][Index], Replace_In_Name_Columns[1][Index])
    
    return df