from notion_client import Client
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
from Stringpy import Clean_String_With_Emojis

#######################################################################################################################
# ADD OR CREATE #
#######################################################################################################################

def Add_Block(Token: Client, Parent_ID: str, Child_Block: dict) -> dict:

    """
    Adds a new block as a child to an existing block in a Notion page. Child_Block is the block data to be 
    added as a child. This should be a dictionary representing the new block.

    """

    Response = Token.blocks.children.append(
        block_id=Parent_ID,
        children=[Child_Block]
    )

    return Response

def Create_Callout(Text: str, Emoji: str ='🏛️', Color: str ='gray'):

    Callout_Block = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": Text
                    }
                }
            ],
            "icon": {
                "type": "emoji",
                "emoji": Emoji
            },
            "color": f'{Color}_background'
        }
    }

    return Callout_Block

def Create_Text_Block(Text: str, Color: str):

    Block = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": Text
                    }
                }
            ],
            "color": Color
        }
    }

    return Block

def Create_Page(Token: Client, Parent_ID: str, Title: str, Properties: dict = {}) -> dict:

    """
    Creates a new page in a Notion database or workspace. Has a additional properties to set for the new page. 
    This should be a dictionary where keys are property names and values are the corresponding values.
    Returns a dict, the response from the Notion API after creating the page.

    """

    Page_Data = {
        'parent': {'id': Parent_ID},
        'properties': {
            'title': {
                'title': [
                    {
                        'text': {
                            'content': Title
                        }
                    }
                ]
            }
        }
    }

    if Properties:
        Page_Data['properties'].update(Properties)

    Page = Token.pages.create(**Page_Data)

    return Page

def Create_Page_and_Add_Block(Token: Client, Parent_ID: str, Title: str, Block: dict) -> dict:

    Page = Create_Page(Token, Parent_ID, Title)
    Page_ID = Page.get('id')
    
    if Page_ID:
        Token.blocks.children.append(
            block_id=Page_ID,
            children=[Block]
        )
    
    return Page


#######################################################################################################################
# PAGES #
#######################################################################################################################

# def Delete_Page(Token: Client, Page_ID: str):

# def Duplicate_Page(Token: Client, Page_ID: str) -> dict:

# def Change_Page_Name(Token: Client, Page_ID: str, New_Name: str) -> dict:

# def Change_Page_Properties(Token: Client, Page_ID: str, New_Properties: Dict) -> dict:


#######################################################################################################################
# BLOCKS #
#######################################################################################################################

# def Move_Block():

# def Delete_Block():

# def Modify_Content_Block():


#######################################################################################################################
# DATABASES #
#######################################################################################################################

# def Change_Database_Properties():

# def Add_Database_Properties():

# def Delete_Database():

# def Filter_Database():

# def Sorting_Database():

# def Find_Page_In_Database():


#######################################################################################################################
# GET BLOCKS #
#######################################################################################################################

def Get_Blocks(Token: Client, Page_ID: str):
    
    """
    Retrieve all blocks from a Notion page, handling pagination if necessary.

    Returns a list of dictionaries, where each dictionary represents a block in Notion. 

    """

    Results = []
    Response = Token.Client.blocks.children.list(block_id=Page_ID)
    Results.extend(Response['results'])

    # Continue paging if more blocks are available.
    while Response.get('has_more'):
        Response = Token.Client.blocks.children.list(
            block_id=Page_ID,
            start_cursor=Response['next_cursor']
        )
        Results.extend(Response['results'])

    return Results

def Print_Block_IDs_And_Text(Token: Client, Page_ID: str, Child_Recursive: bool = False, Prefix: str = ""):
    
    """
    Print block IDs and text content from a Notion page. Can process child blocks recursively.

    Example:
    Print_Block_IDs_And_Text('my_token', 'page_id', Child_Recursive=True)

    """

    Blocks = Get_Blocks(Token, Page_ID)

    Block_Types_With_Text = ['heading_1', 'heading_2', 'heading_3', 'paragraph', 'bulleted_list_item', 
                             'numbered_list_item', 'callout']

    Count = 0
    
    for Block in Blocks:
        Content_Type = Block["type"]
        Block_ID = Block['id']

        Current_Prefix = f"{Prefix}{Count + 1}"
        Count += 1
        Has_Children = True if Block['has_children'] else False

        if Content_Type in Block_Types_With_Text:
            try:
                Rich_Text_Elements = Block[Content_Type].get('rich_text', [])

                Content = []

                for Element in Rich_Text_Elements:
                    if 'text' in Element and 'content' in Element['text']:
                        Content.append(Element['text']['content'])
                    elif 'plain_text' in Element:
                        Content.append(Element['plain_text'])

                Final_Content = ' '.join(Content)

                print(f'Block {Current_Prefix}:')
                print(f"ID: {Block['id']}")
                print(f"Type: {Block['type']}")
                print(f"Content: {Final_Content}")
                print(f"Has children: {Has_Children}")
                print('\n')

                if Has_Children and Child_Recursive:
                    Print_Block_IDs_And_Text(Token, Block_ID, Child_Recursive=True, Prefix=f"{Current_Prefix}.")

            except (KeyError, IndexError, TypeError) as e:
                print(f"Error processing block with ID {Block['id']}: {e}")

        else:
            print(f"The block with ID {Block['id']} is not of the expected text type.")


#######################################################################################################################
# CLIENT #
#######################################################################################################################

def Check_Client_Permissions(Token: Client, Page_ID: str) -> bool:
    try:
        Response = Token.pages.Print(page_id=Page_ID)
        return True
    
    except Exception as e:
        print(f"Error accessing the page: \n {e}")        
        return False


#######################################################################################################################
# GET PROPERTIES OR CONTENT #
#######################################################################################################################

def Get_Block_Properties(Token: Optional[Client] = None, Block_ID: Optional[str] = None, 
                         Block_Data: Optional[dict] = None, Properties: List[str] = []) -> Dict[str, any]:
    
    """
    Get specified properties from a block using its ID or provided data.

    Parameters:
    - Token (Client, optional): An instance of the Notion client.
    - Block_ID (str, optional): The ID of the block.
    - Block_Data (dict, optional): The data of the block. If not provided, will retrieve using Token and Block_ID.
    - Properties (list): List of properties to get.

    Returns:
    - dict: Dictionary with extracted properties.

    Example:
    Get_Block_Properties(notion_client, 'block-id-123', ['Title', 'Date'])

    """
    
    if Block_Data is None:
        if Token is None or Block_ID is None:
            raise ValueError("Either Block_Data must be provided or both Token and Block_ID must be provided.")
        Block_Data = Token.blocks.retrieve(block_id=Block_ID)
    
    Block_Properties = {}
    for Property in Properties:

        Value = Block_Data.get('properties', {}).get(Property, {})
        Type = Value.get('type', '')

        if Type == 'rich_text':
            Text = Value.get('rich_text', [{}])[0].get('plain_text', 'No Text')
            Block_Properties[Property] = Text

        elif Type == 'number':
            Number = Value.get('number', 'No Number')
            Block_Properties[Property] = Number

        elif Type == 'select':
            Selection = Value.get('select', {}).get('name', 'No Selection')
            Block_Properties[Property] = Selection

        elif Type == 'multi_select':
            Multiple_Selection = [Option['name'] for Option in Value.get('multi_select', [])]
            Block_Properties[Property] = Multiple_Selection

        elif Type == 'date':
            Date = Value.get('date', {}).get('start', 'No Date')
            Block_Properties[Property] = Date

        elif Type == 'checkbox':
            Checkbox = Value.get('checkbox', False)
            Block_Properties[Property] = Checkbox

        elif Type == 'url':
            URL = Value.get('url', 'No URL')
            Block_Properties[Property] = URL

        elif Type == 'email':
            Email = Value.get('email', 'No Email')
            Block_Properties[Property] = Email

    return Block_Properties

def Get_Page_Properties(Token: Optional[Client] = None, Page_ID: Optional[str] = None, 
                        Page_Data: Optional[dict] = None, Properties: List[str] = ['Title']) -> Dict[str, any]:
    
    """
    Get specified properties from a Notion page using its ID or provided data.

    Parameters:
    - Token (Client, optional): An instance of the Notion client.
    - Page_ID (str, optional): The ID of the page.
    - Page_Data (dict, optional): The data of the page. If not provided, will retrieve using Token and Page_ID.
    - Properties (list): List of property names to get.

    Returns:
    - dict: Dictionary with extracted properties.

    Example:
    Get_Page_Properties(notion_client, 'page-id-456', ['Title', 'ID', 'Creation_Date'])

    """
    
    if Page_Data is None:
        if Token is None or Page_ID is None:
            raise ValueError("Either Page_Data must be provided or both Token and Page_ID must be provided.")
        Page_Data = Token.pages.retrieve(page_id=Page_ID)
    
    Element_Properties = {}

    if 'Title' in Properties:
        Title_Property = Page_Data['properties'].get('Name', {}).get('title', [])
        Title = Title_Property[0]['plain_text'] if Title_Property else 'No Title'
        Element_Properties['Title'] = Title
    
    if 'ID' in Properties:
        Element_Properties['ID'] = Page_Data.get('id', 'No ID')

    if 'Creation_Date' in Properties:
        Creation_Date = Page_Data['properties'].get('Created', {}).get('created_time', 'Unknown')

        if Creation_Date != 'Unknown':
            try:
                Creation_Date_Format = datetime.fromisoformat(Creation_Date.replace('Z', '+00:00'))
                Element_Properties['Creation_Date'] = {
                    'Day': Creation_Date_Format.day,
                    'Month': Creation_Date_Format.month,
                    'Year': Creation_Date_Format.year,
                    'Hour': Creation_Date_Format.hour,
                    'Minute': Creation_Date_Format.minute
                }

            except ValueError:
                Element_Properties['Creation_Date'] = 'Unknown'
        else:
            Element_Properties['Creation_Date'] = 'Unknown'

    if 'Tags' in Properties:
        Tags = Page_Data['properties'].get('Tags', {}).get('multi_select', [])
        Tag_Names = [Tag['name'] for Tag in Tags]
        Element_Properties['Tags'] = Tag_Names

    if 'Link' in Properties:
        Link = Page_Data.get('url', 'No Link')
        Element_Properties['Link'] = Link

    if 'Emoji' in Properties:
        Icon = Page_Data.get('icon', {})
        if Icon.get('type') == 'emoji':
            Emoji = Icon.get('emoji', 'No Emoji')
            Element_Properties['Emoji'] = Emoji
        else:
            Element_Properties['Emoji'] = 'No Emoji'
    
    return Element_Properties

def Get_Database_Properties(Token: Client, Database_ID: str, Properties_List: List[str] = ['Title']) -> List[Dict[str, any]]:
    
    """
    Get data from a Notion database and returns it as a list of dictionaries.
    Handles pagination and supports getting specific properties.

    Parameters:
    - Token (Client): An instance of the Notion client.
    - Database_ID (str): The ID of the database.
    - Properties_List (list): List of properties to get from each page.

    Returns:
    - list: List of dictionaries with extracted properties.

    Example:
    Get_Database_Properties(notion_client, 'database-id-789', ['Title', 'ID', 'Tags'])

    """
    try:
        Data_List = []
        Initial_Cursor = None

        while True:
            Database_Data = Token.databases.query(
                database_id=Database_ID,
                start_cursor=Initial_Cursor,
                page_size=100
            )

            for Item in Database_Data['results']:
                Item_ID = Item['id']
                if Item['object'] == 'page':
                    Item_Data = Get_Page_Properties(Token, Item_ID, Properties_List)
                else:
                    # Assuming you might not need to handle blocks here as Notion databases typically contain pages
                    continue

                if Item_Data:
                    Data_List.append(Item_Data)

            if not Database_Data['has_more']:
                break

            Initial_Cursor = Database_Data['next_cursor']

        return Data_List

    except Exception as Error:
        print("Error accessing the database:", Error)
        return []

def Get_Block_IDs_And_Content(Token: Client, Page_ID: str):   

    """
    Prints the IDs and content of blocks from a Notion page, excluding empty blocks.

    """

    Results = []
    Response = Token.blocks.children.list(block_id=Page_ID)

    for Block in Response['results']:
        Content = Get_Block_Content(Block)
        if Content is not None:
            Results.append(Content)

    while Response.get('has_more'):
        Response = Token.blocks.children.list(
            block_id=Page_ID,
            start_cursor=Response['next_cursor']
        )
        for Block in Response['results']:
            Content = Get_Block_Content(Block)
            if Content is not None:
                Results.append(Content)

    df = pd.DataFrame(Results)

    return df

def Get_Block_Content(Token: Optional[Client] = None, Block_ID: Optional[str] = None, 
                      Block_Data: Optional[Dict] = None, Nulls: bool = False) -> Optional[Dict[str, str]]:
    
    """
    Get content and ID from a block based on its type and filters out null or empty content.

    Parameters:
    - Token (Client, optional): An instance of the Notion client.
    - Block_ID (str, optional): The ID of the block.
    - Block_Data (dict, optional): The data of the block. If not provided, will retrieve using Token and Block_ID.
    - Nulls (bool): Whether to return blocks with null or empty content.

    Returns:
    - dict: Dictionary with block ID and content if content is not empty, otherwise None.

    Example:
    Get_Block_Content(notion_client, 'block-id-123', Nulls=True)

    """
    
    if Block_Data is None:
        if Token is None or Block_ID is None:
            raise ValueError("Either Block_Data must be provided or both Token and Block_ID must be provided.")
        Block_Data = Token.blocks.retrieve(block_id=Block_ID)
    
    Block_Data_Extracted = {'ID': Block_Data.get('id', 'No ID'), 'Content': ''}

    Block_Type = Block_Data.get('type', '')
    Valid_Types = ['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item']

    if Block_Type in Valid_Types:
        Rich_Text = Block_Data.get(Block_Type, {}).get('rich_text', [])
        Block_Data_Extracted['Content'] = ' '.join([Text.get('plain_text', '') for Text in Rich_Text])
    
    if Nulls or Block_Data_Extracted['Content'].strip():
        return Block_Data_Extracted
    else:
        return None

def Get_All_Blocks_Content(Token: Client, Page_ID: str):
    Blocks = Get_Blocks(Token, Page_ID)
    Content_List = []

    for Block in Blocks:
        Content_List.append(Get_Block_Content(Block))
    
    return Content_List