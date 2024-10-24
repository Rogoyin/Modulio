import datetime as dt

def Sorting_Dates_For_Weeks(Dates: list[dt.datetime]) -> list[list[int]]:
    
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

def Add_Time_Delta(Minutes: int = 0, Hours: int = 0, Days: int = 0, Future: bool = True, 
                   String: bool = False):
    
    """
    Add or subtract a time delta from the current datetime.

    This function calculates a new datetime by adding or subtracting 
    a specified amount of time (in minutes, hours, and days) from the 
    current datetime. It can return the result as a formatted string 
    or as a datetime object.

    Parameters:
    Minutes (int): The number of minutes to add or subtract. Default is 0.
    Hours (int): The number of hours to add or subtract. Default is 0.
    Days (int): The number of days to add or subtract. Default is 0.
    Future (bool): If True, adds the time delta. If False, subtracts it. 
                   Default is True.
    String (bool): If True, returns the result as a formatted string. 
                   If False, returns a datetime object. Default is False.

    Returns:
    datetime or str: Returns the new datetime object if String is False, 
                     or a formatted string if String is True.
    """

    Now = dt.datetime.now()
    Period = dt.timedelta(days = Days, hours = Hours, minutes = Minutes)

    if Future:
        Moment = Now + Period
    else:
        Moment = Now - Period

    if String:
        return Moment.strftime('%Y-%m-%d %H:%M')
    else:
        return Moment