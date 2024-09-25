import Framio as fr
import pandas as pd

def Get_History(df, Team1, Team2, Field = None, Tournament_Type = None, Tournaments = None, 
                Period = False, Year1 = 1900, Year2 = 2024, PJ = True, 
                Team1_Win = True, Team2_Win = True, Father = True, 
                Difference = True, Difference_Goal = True, 
                Min_Goals_Team1 = None, Max_Goals_Team1 = None, 
                Min_Goals_Team2 = None, Max_Goals_Team2 = None, 
                Stadium = None, Referee = None):
    
    Data_History = {}
    
    df_History = fr.Get_Selected_Rows_By_Two_Columns(df, 'Home_Team', 'Away_Team', [Team1, Team2], Condition = 'Match either')

    if Field == 'Team1':
        df_History = df_History[df_History['Home_Team'] == Team1]
    elif Field == 'Team2':
        df_History = df_History[df_History['Home_Team'] == Team2]

    if Tournament_Type:
        df_History = df_History[df_History['Tournament'] == Tournament_Type]

    if Tournaments:
        df_History = df_History[df_History['Tournament'].isin(Tournaments)]
    
    if Period:
        df_History = df_History[(df_History['Year'] >= Year1) & (df_History['Year'] <= Year2)]

    if Min_Goals_Team1 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team1) & (df_History['Home_Goals'] >= Min_Goals_Team1)) |
            ((df_History['Away_Team'] == Team1) & (df_History['Away_Goals'] >= Min_Goals_Team1))
        ]
    
    if Max_Goals_Team1 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team1) & (df_History['Home_Goals'] <= Max_Goals_Team1)) |
            ((df_History['Away_Team'] == Team1) & (df_History['Away_Goals'] <= Max_Goals_Team1))
        ]

    if Min_Goals_Team2 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team2) & (df_History['Home_Goals'] >= Min_Goals_Team2)) |
            ((df_History['Away_Team'] == Team2) & (df_History['Away_Goals'] >= Min_Goals_Team2))
        ]
    
    if Max_Goals_Team2 is not None:
        df_History = df_History[
            ((df_History['Home_Team'] == Team2) & (df_History['Home_Goals'] <= Max_Goals_Team2)) |
            ((df_History['Away_Team'] == Team2) & (df_History['Away_Goals'] <= Max_Goals_Team2))
        ]

    if Stadium:
        df_History = df_History[df_History['Stadium'] == Stadium]
    
    if Referee:
        df_History = df_History[df_History['Referee'] == Referee]

    if PJ:
        Data_History['Matches'] = len(df_History)

    if Team1_Win:
        Data_History[f'{Team1} wins:'] = len(df_History[
            ((df_History['Result'] == 'Home') & (df_History['Home_Team'] == Team1)) |
            ((df_History['Result'] == 'Away') & (df_History['Away_Team'] == Team1))
        ])

    if Team2_Win:
        Data_History[f'{Team2} wins:'] = len(df_History[
            ((df_History['Result'] == 'Home') & (df_History['Home_Team'] == Team2)) |
            ((df_History['Result'] == 'Away') & (df_History['Away_Team'] == Team2))
        ])
    
    if Difference:
        if Data_History[f'{Team1} wins:'] > Data_History[f'{Team2} wins:']:
            Data_History['Father'] = Team1
        elif Data_History[f'{Team2} wins:'] > Data_History[f'{Team1} wins:']:
            Data_History['Father'] = Team2
        else:
            Data_History['Father'] = 'Neither'
    
    if Difference:
        Data_History['Difference'] = '+' + str(abs(Data_History[f'{Team1} wins:'] - Data_History[f'{Team2} wins:']))

    if Difference_Goal:
        Data_History['Goals_Difference'] = '+' + str(abs(df_History['Home_Goals'].sum() - df_History['Away_Goals'].sum()))

    return Data_History, df_History

def Performance_Team(df, Team, Tournament_Type = None, Tournaments = None, 
                     Period = False, Year1 = 1900, Year2 = 2024, PJ = True, 
                     Team1_Win = True, Team2_Win = True, Father = True, 
                     Difference = True, Difference_Goal = True, 
                     Min_Goals_Team1 = None, Max_Goals_Team1 = None, 
                     Min_Goals_Team2 = None, Max_Goals_Team2 = None, 
                     Stadium = None, Referee = None):