from datetime import datetime

def Sorting_Dates_For_Weeks(Dates: list[datetime]) -> list[list[int]]:
    
    """
    Sort a list of dates into weeks and return indices of the days.

    Parameters:
    - Dates (list[datetime]): A list of dates, where each element is a 
      datetime object representing a day, month, year, and possibly time.

    Returns:
    - list[list[int]]: A list of weeks, where each week contains indices 
      of the days within that week.
    
    """

    Weeks = []
    Index = 0

    while Index < len(Dates) - 2:
        if Dates[Index].weekday() == 0:  # Check if it's Monday.
            Week = []
            while Index < len(Dates) - 2 and Dates[Index].weekday() <= Dates[Index + 1].weekday():
                Week.append(Index)  # Append index of the date.
                Index += 1
            Week.append(Index)  # Append the last index of the week.
            Weeks.append(Week)  # Add the week to the list of weeks.
        Index += 1

    if Dates[-1].weekday() == 0:  # If the last date is a Monday.
        Weeks[-1].append(len(Dates) - 1)  # Append the last index to the last week.
    else:
        Weeks.append([len(Dates) - 1])  # Add the last date as a new week.

    return Weeks