import pandas as pd
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_ALIGN_VERTICAL

def Create_Expanded_Grid_Word_Document(
    Dataframe: pd.DataFrame, 
    Bold_Column: str, 
    Currency_Column: str, 
    Output_File: str, 
    Rows_Per_Page: int, 
    Columns_Per_Page: int,
    Length_Page: int = 22
) -> None:

    """
    Creates a Word document with a grid layout, where rows and columns
    expand to cover the full page. The number column is bold and occupies
    the majority of the cell, while the text column is smaller.

    Parameters:
        Dataframe (pd.DataFrame): The source dataframe containing the data.
        Bold_Column (str): The name of the column whose values will appear
        smaller and unbolded.
        Currency_Column (str): The name of the column whose values will 
        appear bolded and larger.
        Output_File (str): The name of the output Word file.
        Rows_Per_Page (int): Number of rows to display per page.
        Columns_Per_Page (int): Number of columns to display per row.
        Length_Page (int): Centimeters of the page.

    Returns:
        None

    Example:
        >>> df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie'], 
        ...                    'Amount': [1234.56, 789.01, 456.78]})
        >>> Create_Expanded_Grid_Word_Document(
        ...     df, 'Name', 'Amount', 'output.docx', 5, 2, 22
        ... )

    """

    Document_File = Document()
    Total_Entries = len(Dataframe)
    Entries_Per_Page = Rows_Per_Page * Columns_Per_Page

    Entry_Index = 0

    while Entry_Index < Total_Entries:
        # Add a new section (page).
        if Entry_Index > 0:
            Document_File.add_page_break()

        # Create a table for the page.
        Table = Document_File.add_table(rows=Rows_Per_Page, cols=Columns_Per_Page)

        # Adjust the table to expand across the full page.
        Table_Width = 16.5  # Width in cm (adjust based on page size and margins).
        Column_Width = Table_Width / Columns_Per_Page

        for Row_Index in range(Rows_Per_Page):
            for Col_Index in range(Columns_Per_Page):
                Cell = Table.cell(Row_Index, Col_Index)

                # Set cell width.
                Cell_Width_Element = Cell._element
                Table_Properties = Cell_Width_Element.xpath('.//w:tcPr')[0]
                Width_Element = OxmlElement('w:tcW')
                Width_Element.set(qn('w:w'), str(int(Column_Width * 567)))  # Convert cm to twips.
                Width_Element.set(qn('w:type'), 'dxa')
                Table_Properties.append(Width_Element)

                if Entry_Index < Total_Entries:
                    # Get the current row from the DataFrame.
                    Row = Dataframe.iloc[Entry_Index]
                    Small_Text = Row[Bold_Column]
                    Large_Bold_Value = f"${int(Row[Currency_Column]):,}"

                    # Add content to the cell.
                    Paragraph = Cell.paragraphs[0]

                    Run_Bold = Paragraph.add_run(Large_Bold_Value)
                    Run_Bold.bold = True
                    
                    Run_Normal = Paragraph.add_run(f"\n{Small_Text}")

                    # Adjust font size to fit the new layout.
                    Large_Font_Size = 48  # Larger font size for bold numbers.
                    Small_Font_Size = 12  # Smaller font size for regular text.
                    Run_Bold.font.size = Pt(Large_Font_Size)
                    Run_Normal.font.size = Pt(Small_Font_Size)

                    # Align the content in the center of the cell.
                    Paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    Cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

                    Entry_Index += 1
                else:
                    # Leave empty cells if there are no more entries.
                    Cell.text = ""

        # Adjust row height to expand rows across the page.
        for Row in Table.rows:
            Row_Height = Length_Page / Rows_Per_Page
            Row.height = Cm(Row_Height)

        # Apply a grid style for visibility.
        Table.style = "Table Grid"

    # Save the document to the specified file.
    Document_File.save(Output_File)