import random
from typing import List

def Generate_Random_Numbers(Count: int, Minimum_Value: int, Maximum_Value: int) -> List[int]:

    """

    Generates a list of random integers within a specified range.

    Parameters:
        Count: The number of random integers to generate.
        Minimum_Value: The minimum value for the random integers.
        Maximum_Value: The maximum value for the random integers.

    Returns:
        A list of random integers within the specified range.

    Example:
        >>> Generate_Random_Numbers(5, 1, 10)
        [3, 7, 2, 10, 6]

    """

    return [random.randint(Minimum_Value, Maximum_Value) for _ in range(Count)]

def Generate_Random_Letters(Count: int, Include_Uppercase: bool = True) -> List[str]:

    """

    Generates a list of random letters from the alphabet.

    Parameters:
        Count: The number of random letters to generate.
        Include_Uppercase: Indicates whether to include uppercase letters.

    Returns:
        A list of random letters from the alphabet.

    Example:
        >>> Generate_Random_Letters(5, Include_Uppercase=True)
        ['A', 'b', 'Z', 'm', 'P']

    """

    Letters = "abcdefghijklmnopqrstuvwxyz"
    if Include_Uppercase:
        Letters += Letters.upper()

    return [random.choice(Letters) for _ in range(Count)]

