import pandas as pd
import re
import Stringio
from typing import List, Callable, Optional

def Match_And_Copy_Column_Values(df1: pd.DataFrame, df2: pd.DataFrame, 
                                 Column_df1_A: str, Column_df1_B: str, 
                                 Column_df2_A: str, Column_df2_B: str) -> pd.DataFrame:
    
    '''
    Compare values from df1 and df2 based on Column_df1_A and Column_df2_A, and copy values from Column_df2_B to 
    Column_df1_B in df1.

    '''

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

    '''
    This function compares two specified columns from two separate dataframes and identifies the unique values 
    present in each column but not in the other. It returns a new dataframe with the unique values and the corresponding 
    source of the values (custom labels provided by Label1 and Label2).

    '''

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
    Applies a given operations to a list of specified columns for rows filtered by a condition.

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
    Identifies the best value from specified columns based on a comparison function.

    Parameters:
    - df: DataFrame containing the data.
    - Target_Column: The column where the target value is stored.
    - Columns_To_Compare: List of column names to compare against the target value.
    - Best_Value_Column: The name of the column where the best value will be stored.
    - Comparison_Function: Optional function to determine if a value is better. Defaults to equality comparison.
    The function must accept two arguments (the target value and the comparison column value) and return a boolean.

    Returns:
    - The modified DataFrame with the Best_Value_Column updated to the best value based on the comparison function.

    Example:
        df = Find_Best_Value_Column(df,
                                    Target_Column = 'Precio',
                                    Columns_To_Compare = ['Proveedor1', 'Proveedor2', 'Proveedor3'],
                                    Best_Value_Column = 'Mejor_Proveedor',
                                    Comparison_Function = lambda Target, Value: Target == Value
                                    )
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