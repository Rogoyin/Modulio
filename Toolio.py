
def Print_Docstring(Function):  

    """
    Print the docstring of a given function with enhanced formatting.

    Parameters:
    -----------
    Function : callable
        The function whose docstring is to be printed.

    Returns:
    --------
    None
        The function prints the docstring of the provided function.

    """
    
    if not callable(Function):
        raise ValueError("The provided argument is not a function.")

    # Capture docstring.
    Captured_Docstring = Function.__doc__ or "No docstring available." 
     # Fallback if no docstring is present.

    # Print the captured docstring with formatting.
    print("===" * 10)  # Decorative line.
    print(Captured_Docstring)
    print("===" * 10)  # Decorative line.

