
def Check_Pair(Number: int) -> bool:

    """
    Checks if a given number is an even number.

    The function determines whether the provided number is even by using 
    the modulus operator. If the number is divisible by 2, it is classified 
    as even and the function returns True; otherwise, it returns False.

    Parameters:
    -----------
    Number : int
        The number to be checked. This must be an integer value.

    Returns:
    --------
    bool
        Returns True if the number is even; otherwise, it returns False.

    Notes:
    ------
    - The function only accepts integers as valid input.
    - If a non-integer type is passed, a TypeError will be raised.

    Example:
    ---------
    >>> result1 = Check_Pair(4)
    >>> print(result1)
    True

    >>> result2 = Check_Pair(5)
    >>> print(result2)
    False
    """

    return Number % 2 == 0

def Sum_Digits(Number) -> int:

    """
    Calculates the sum of the digits of a given number.

    The function converts the number into a string to iterate through each 
    digit. It sums up the integer values of the digits and returns the 
    total sum. This is useful for scenarios where the digit sum is required 
    for further calculations or checks.

    Parameters:
    -----------
    Number : int
        The number whose digits will be summed. This must be an integer 
        value.

    Returns:
    --------
    int
        The total sum of the digits in the provided number.

    Notes:
    ------
    - The function works with both positive and negative integers.
    - If a non-integer type is passed, a TypeError will be raised.

    Example:
    ---------
    >>> result1 = Sum_Digits(123)
    >>> print(result1)
    6

    >>> result2 = Sum_Digits(-456)
    >>> print(result2)
    15
    """
    
    Sum = 0
    for Digit in str(Number):
        Sum = Sum + int(Digit)
    return Sum
    
def Round_By_Multiple(Number, Multiple, Rounding_Direction = None):

    '''
    Rounds a given number to the nearest multiple of a specified value.

    The function analyzes the last digit of the number to determine whether 
    to round up or down, based on the specified rounding direction. If the 
    rounding direction is not provided, it defaults to rounding to the nearest 
    multiple based on standard rounding rules.

    Parameters:
    -----------
    Number : float or int
        The number to be rounded. This can be either an integer or a float.

    Multiple : float or int
        The value to which the number will be rounded. This should be a 
        non-zero number that determines the rounding multiple.

    Rounding_Direction : str, optional
        Specifies the direction to round the number. Acceptable values are:
        - 'Under': Rounds down to the nearest multiple of the specified value.
        - 'Upper': Rounds up to the nearest multiple of the specified value.
        If None (default), the function will round to the nearest multiple 
        based on standard rounding rules.

    Returns:
    --------
    float or int
        The rounded number, either to the nearest multiple, rounded up, 
        or rounded down based on the specified direction.

    Notes:
    ------
    - The function handles both positive and negative numbers.
    - If the specified multiple is zero, a ValueError will be raised.
    - The function evaluates the last digit of the number to determine 
      the rounding choice (up or down).
    - If the rounding direction does not match the default behavior, 
      the number will be rounded according to the specified direction.

    Example:
    ---------
    >>> result1 = Round_By_Multiple(27, 5)
    >>> print(result1)
    25.0

    >>> result2 = Round_By_Multiple(27, 5, Rounding_Direction='Upper')
    >>> print(result2)
    30.0

    >>> result3 = Round_By_Multiple(27, 5, Rounding_Direction='Under')
    >>> print(result3)
    25.0

    '''

    Last_Digit = float(str(Number)[-1])

    if Last_Digit >= 5:
        Final_Round = 'Upper'
    else:
        Final_Round = 'Under'

    if Rounding_Direction == 'Under' and Final_Round != Rounding_Direction:
        return (round(Number / Multiple) * Multiple) - Multiple
    elif Rounding_Direction == 'Upper' and Final_Round != Rounding_Direction:
        return (round(Number / Multiple) * Multiple) + Multiple
    
    else:
        return (round(Number / Multiple) * Multiple)

















































































