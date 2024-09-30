import Framio as fr
import pandas as pd
from typing import Optional, Tuple, Dict

def Get_History(df: pd.DataFrame, Team1: str, Team2: str, Field: Optional[str] = None, 
                Tournament_Type: Optional[str] = None, Tournaments: Optional[List[str]] = None, 
                Period: bool = False, Year1: int = 1900, Year2: int = 2024, 
                PJ: bool = True, Team1_Win: bool = True, Team2_Win: bool = True, 
                Father: bool = True, Difference: bool = True, 
                Difference_Goal: bool = True, Min_Goals_Team1: Optional[int] = None, 
                Max_Goals_Team1: Optional[int] = None, Min_Goals_Team2: Optional[int] = None, 
                Max_Goals_Team2: Optional[int] = None, Stadium: Optional[str] = None, 
                Referee: Optional[str] = None) -> Tuple[Dict[str, int], pd.DataFrame]:
    
    """
    Get historical match data between two teams based on various filters.

    Parameters:
    - df (pd.DataFrame): DataFrame containing match history.
    - Team1 (str): Name of the first team.
    - Team2 (str): Name of the second team.
    - Field (Optional[str]): Specify which team to filter by.
    - Tournament_Type (Optional[str]): Filter by tournament type.
    - Tournaments (Optional[List[str]]): List of specific tournaments to filter.
    - Period (bool): Whether to filter by year range.
    - Year1 (int): Start year for filtering.
    - Year2 (int): End year for filtering.
    - PJ (bool): Include total matches count in results.
    - Team1_Win (bool): Include Team1 win count in results.
    - Team2_Win (bool): Include Team2 win count in results.
    - Father (bool): Identify the dominating team.
    - Difference (bool): Include win difference in results.
    - Difference_Goal (bool): Include goal difference in results.
    - Min_Goals_Team1 (Optional[int]): Minimum goals for Team1.
    - Max_Goals_Team1 (Optional[int]): Maximum goals for Team1.
    - Min_Goals_Team2 (Optional[int]): Minimum goals for Team2.
    - Max_Goals_Team2 (Optional[int]): Maximum goals for Team2.
    - Stadium (Optional[str]): Filter by stadium name.
    - Referee (Optional[str]): Filter by referee name.

    Returns:
    - Tuple[Dict[str, int], pd.DataFrame]: A dictionary of match data and a DataFrame of filtered matches.

    """
    
    Data_History = {}
    
    df_History = fr.Get_Selected_Rows_By_Two_Columns(df, 'Home_Team', 
                                                      'Away_Team', [Team1, Team2], 
                                                      Condition='Match either')

    if Field == 'Team1':
        df_History = df_History[df_History['Home_Team'] == Team1]
    elif Field == 'Team2':
        df_History = df_History[df_History['Home_Team'] == Team2]

    if Tournament_Type is not None:
        df_History = df_History[df_History['Tournament'] == Tournament_Type]

    if Tournaments is not None:
        df_History = df_History[df_History['Tournament'].isin(Tournaments)]
    
    if Period:
        df_History = df_History[(df_History['Year'] >= Year1) & 
                                 (df_History['Year'] <= Year2)]

    if Min_Goals_Team1 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team1) & 
             (df_History['Home_Goals'] >= Min_Goals_Team1)) |
            ((df_History['Away_Team'] == Team1) & 
             (df_History['Away_Goals'] >= Min_Goals_Team1))
        ]
    
    if Max_Goals_Team1 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team1) & 
             (df_History['Home_Goals'] <= Max_Goals_Team1)) |
            ((df_History['Away_Team'] == Team1) & 
             (df_History['Away_Goals'] <= Max_Goals_Team1))
        ]

    if Min_Goals_Team2 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team2) & 
             (df_History['Home_Goals'] >= Min_Goals_Team2)) |
            ((df_History['Away_Team'] == Team2) & 
             (df_History['Away_Goals'] >= Min_Goals_Team2))
        ]
    
    if Max_Goals_Team2 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team2) & 
             (df_History['Home_Goals'] <= Max_Goals_Team2)) |
            ((df_History['Away_Team'] == Team2) & 
             (df_History['Away_Goals'] <= Max_Goals_Team2))
        ]

    if Stadium is not None:
        df_History = df_History[df_History['Stadium'] == Stadium]
    
    if Referee is not None:
        df_History = df_History[df_History['Referee'] == Referee]

    if PJ:
        Data_History['Matches'] = len(df_History)

    if Team1_Win:
        Data_History[f'{Team1} wins:'] = len(df_History[
            ((df_History['Result'] == 'Home') & 
             (df_History['Home_Team'] == Team1)) |
            ((df_History['Result'] == 'Away') & 
             (df_History['Away_Team'] == Team1))
        ])

    if Team2_Win:
        Data_History[f'{Team2} wins:'] = len(df_History[
            ((df_History['Result'] == 'Home') & 
             (df_History['Home_Team'] == Team2)) |
            ((df_History['Result'] == 'Away') & 
             (df_History['Away_Team'] == Team2))
        ])
    
    if Difference:
        Team1_Wins = Data_History.get(f'{Team1} wins:', 0)
        Team2_Wins = Data_History.get(f'{Team2} wins:', 0)
        
        if Team1_Wins > Team2_Wins:
            Data_History['Father'] = Team1
        elif Team2_Wins > Team1_Wins:
            Data_History['Father'] = Team2
        else:
            Data_History['Father'] = 'Neither'
    
    if Difference:
        Data_History['Difference'] = '+' + str(abs(Team1_Wins - Team2_Wins))

    if Difference_Goal:
        Data_History['Goals_Difference'] = '+' + str(abs(df_History['Home_Goals'].sum() - 
                                                         df_History['Away_Goals'].sum()))

    return Data_History, df_History


# def Performance_Team(df, Team, Tournament_Type = None, Tournaments = None, 
#                      Period = False, Year1 = 1900, Year2 = 2024, PJ = True, 
#                      Team1_Win = True, Team2_Win = True, Father = True, 
#                      Difference = True, Difference_Goal = True, 
#                      Min_Goals_Team1 = None, Max_Goals_Team1 = None, 
#                      Min_Goals_Team2 = None, Max_Goals_Team2 = None, 
#                      Stadium = None, Referee = None):