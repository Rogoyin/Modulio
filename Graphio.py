import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.linear_model import LinearRegression
from numpy.polynomial.polynomial import Polynomial

#######################################################################################################################
# CREATE #
#######################################################################################################################

import matplotlib.pyplot as plt
import seaborn as sns

# See documentation in "Graphio - Plot Functions.txt" for parameter options.

def Create_Line_Plot(X, Y, Title = None, X_Label = 'X', Y_Label = 'Y', Colors = None, Grid = True, 
                     Figure_Size = (10, 6), Font_Size = 12, Alpha = 1.0, X_Lim = None, Y_Lim = None, 
                     X_Scale = 'linear', Y_Scale = 'linear', Labels = None, Legend = False, 
                     Legend_Location = 'best', Legend_Font_Size = 12, Marker_Styles = 'o', 
                     Line_Styles = '-', Line_Width = 2, Horizontal_Lines = None, Vertical_Lines = None, 
                     Annotations = None, File_Name = None, File_Format = 'png', 
                     X_Label_Rotation = 0, Title_Pad = 20, X_Label_Pad = 10, Y_Label_Pad = 10, 
                     X_Ticks_Step = None, Y_Ticks_Step = None, X_Ticks = None, Y_Ticks = None):
    
    '''
    Example of use:

    gr.Create_Line_Plot(
                        X = X_data,
                        Y = Y_data,
                        Title = 'Sine and Cosine Waves',
                        X_Label = 'X-axis (radians)',
                        Y_Label = 'Y-axis',
                        Colors = Colors,
                        Labels = Labels,
                        Legend = True,
                        X_Lim = (0, 10),
                        Y_Lim = (-1.5, 1.5),
                        Horizontal_Lines = [0],  # Horizontal lines in y=0
                        Vertical_Lines = [np.pi/2, np.pi],  # Vertical lines in pi/2 and pi
                        Annotations = [
                            {'text': 'Max Sine', 'xy': (np.pi/2, 1), 'xytext': (np.pi/2 + 0.5, 1.2), 
                            'arrowprops': {'facecolor': 'black', 'arrowstyle': '->'}},
                            {'text': 'Min Cosine', 'xy': (3*np.pi/2, -1), 'xytext': (3*np.pi/2 + 0.5, -1.2), 
                            'arrowprops': {'facecolor': 'black', 'arrowstyle': '->'}}
                        ],
                        File_Name = 'sine_cosine_plot',  
                        File_Format = 'png',
                        X_Label_Rotation = 45,
                        X_Ticks_Step = 1,  
                        Y_Ticks_Step = 0.5,  
                        X_Ticks = [2, 4, 6, 8],  # Personalized X_Ticks
                        Y_Ticks = [-1, 0, 1]     # Personalized Y_Ticks
                        )

    '''
    
    plt.figure(figsize = Figure_Size)
    
    if isinstance(Y, (list, np.ndarray)):
        if isinstance(Y, np.ndarray):
            Y = [Y]
        for i in range(len(Y)):
            Color = Colors[i] if Colors and i < len(Colors) else None
            Label = Labels[i] if Labels and Legend and i < len(Labels) else None
            Marker_Style = Marker_Styles[i] if isinstance(Marker_Styles, list) and i < len(Marker_Styles) else Marker_Styles
            Line_Style = Line_Styles[i] if isinstance(Line_Styles, list) and i < len(Line_Styles) else Line_Styles
            
            plt.plot(X, Y[i], color = Color, marker = Marker_Style, linestyle = Line_Style, linewidth = Line_Width, 
                     alpha = Alpha, label = Label)
    else:
        raise ValueError("Y must be a list or an array.")

    plt.xscale(X_Scale)
    plt.yscale(Y_Scale)
    
    if X_Lim:
        plt.xlim(X_Lim)
    if Y_Lim:
        plt.ylim(Y_Lim)
    
    if Title:
        plt.title(Title, fontsize = Font_Size, pad = Title_Pad)
    plt.xlabel(X_Label, fontsize = Font_Size, labelpad = X_Label_Pad)
    plt.ylabel(Y_Label, fontsize = Font_Size, labelpad = Y_Label_Pad)
    
    plt.xticks(rotation = X_Label_Rotation)
    
    Combined_X_Ticks = set()
    if X_Ticks is not None:
        Combined_X_Ticks.update(X_Ticks)
    if X_Ticks_Step is not None and X_Lim is not None:
        Combined_X_Ticks.update(np.arange(X_Lim[0], X_Lim[1] + 1, step = X_Ticks_Step))
    
    plt.xticks(sorted(Combined_X_Ticks))  

    Combined_Y_Ticks = set()
    if Y_Ticks is not None:
        Combined_Y_Ticks.update(Y_Ticks)
    if Y_Ticks_Step is not None and Y_Lim is not None:
        Combined_Y_Ticks.update(np.arange(Y_Lim[0], Y_Lim[1] + 1, step = Y_Ticks_Step))
    
    plt.yticks(sorted(Combined_Y_Ticks))  

    if Grid:
        plt.grid(True)
    
    if Horizontal_Lines:
        for Line in Horizontal_Lines:
            plt.axhline(y = Line, color = 'gray', linestyle = '--')
    if Vertical_Lines:
        for Line in Vertical_Lines:
            plt.axvline(x = Line, color = 'gray', linestyle = '--')
    
    if Annotations:
        for Annotation in Annotations:
            plt.annotate(Annotation['text'], xy = Annotation['xy'], xytext = Annotation['xytext'], 
                         arrowprops = Annotation.get('arrowprops', {}))
    
    if Legend and Labels:
        plt.legend(loc = Legend_Location, fontsize = Legend_Font_Size)
    
    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')
    
    plt.show()

def Create_Histogram(Data, Title = None, X_Label = 'X', Y_Label = 'Y', Bins = 10, Colors = None, Alpha = 0.7, 
                     Grid = True, Figure_Size = (10, 6), Font_Size = 12, X_Lim = None, Y_Lim = None, 
                     Legend = False, Legend_Location = 'best', Legend_Font_Size = 12, 
                     Horizontal_Lines = None, Vertical_Lines = None, Annotations = None, File_Name = None, File_Format = 'png'):
    
    plt.figure(figsize = Figure_Size)
    
    if Colors:
        plt.hist(Data, bins = Bins, color = Colors[0], alpha = Alpha, label = X_Label)
    else:
        plt.hist(Data, bins = Bins, alpha = Alpha, label = X_Label)
    
    if X_Lim:
        plt.xlim(X_Lim)
    if Y_Lim:
        plt.ylim(Y_Lim)
    
    if Title:
        plt.title(Title, fontsize = Font_Size)
    plt.xlabel(X_Label, fontsize = Font_Size)
    plt.ylabel(Y_Label, fontsize = Font_Size)
    
    if Grid:
        plt.grid(True)
    
    if Horizontal_Lines:
        for line in Horizontal_Lines:
            plt.axhline(y = line, color = 'gray', linestyle = '--')
    if Vertical_Lines:
        for line in Vertical_Lines:
            plt.axvline(x = line, color = 'gray', linestyle = '--')
    
    if Annotations:
        for annotation in Annotations:
            plt.annotate(annotation['text'], xy = annotation['xy'], xytext = annotation['xytext'], 
                         arrowprops = annotation.get('arrowprops', {}))
    
    if Legend:
        plt.legend(loc = Legend_Location, fontsize = Legend_Font_Size)
    
    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')
    
    plt.show()

def Create_Bar_Plot(X, Y, Title = None, X_Label = 'X', Y_Label = 'Y', Colors = None, Grid = True, Figure_Size = (10, 6), 
                     Font_Size = 12, Alpha = 1.0, X_Lim = None, Y_Lim = None, 
                     X_Ticks = None, Y_Ticks = None, X_Ticks_Step = None, Y_Ticks_Step = None, 
                     Horizontal_Lines = None, Vertical_Lines = None, 
                     Annotations = None, File_Name = None, File_Format = 'png'):
    
    plt.figure(figsize = Figure_Size)
    plt.bar(X, Y, color = Colors, alpha = Alpha)
    
    if Title:
        plt.title(Title, fontsize = Font_Size)
    plt.xlabel(X_Label, fontsize = Font_Size)
    plt.ylabel(Y_Label, fontsize = Font_Size)
    
    Combined_X_Ticks = set()
    if X_Ticks is not None:
        Combined_X_Ticks.update(X_Ticks)
    if X_Ticks_Step is not None:
        Combined_X_Ticks.update(np.arange(X_Lim[0], X_Lim[1] + 1, step=X_Ticks_Step))
    
    plt.xticks(sorted(Combined_X_Ticks))
    
    Combined_Y_Ticks = set()
    if Y_Ticks is not None:
        Combined_Y_Ticks.update(Y_Ticks)
    if Y_Ticks_Step is not None:
        Combined_Y_Ticks.update(np.arange(Y_Lim[0], Y_Lim[1] + 1, step=Y_Ticks_Step))
    
    plt.yticks(sorted(Combined_Y_Ticks))

    if Grid:
        plt.grid(True)
    
    if Horizontal_Lines:
        for line in Horizontal_Lines:
            plt.axhline(y = line, color = 'gray', linestyle = '--')
    if Vertical_Lines:
        for line in Vertical_Lines:
            plt.axvline(x = line, color = 'gray', linestyle = '--')
    
    if Annotations:
        for annotation in Annotations:
            plt.annotate(annotation['text'], xy = annotation['xy'], xytext = annotation['xytext'], 
                         arrowprops = annotation.get('arrowprops', {}))
    
    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')
    
    plt.show()

def Create_Box_Plot(Data, Title = None, X_Label = 'X', Y_Label = 'Y', Grid = True, Figure_Size = (10, 6), 
                    Font_Size = 12, X_Lim = None, Y_Lim = None, Legend = False, Legend_Location = 'best', 
                    Legend_Font_Size = 12, File_Name = None, File_Format = 'png'):
    
    plt.figure(figsize = Figure_Size)
    sns.boxplot(data = Data)
    
    if X_Lim:
        plt.xlim(X_Lim)
    if Y_Lim:
        plt.ylim(Y_Lim)
    
    if Title:
        plt.title(Title, fontsize = Font_Size)
    plt.xlabel(X_Label, fontsize = Font_Size)
    plt.ylabel(Y_Label, fontsize = Font_Size)
    
    if Grid:
        plt.grid(True)
    
    if Legend:
        plt.legend(loc = Legend_Location, fontsize = Legend_Font_Size)
    
    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')
    
    plt.show()

def Create_Scatter_Plot(X, Y, Title = None, X_Label = 'X', Y_Label = 'Y', Colors = None, Grid = True, Figure_Size = (10, 6),
                         Font_Size = 12, Alpha = 1.0, X_Lim = None, Y_Lim = None,
                         X_Ticks = None, Y_Ticks = None, X_Ticks_Step = None, Y_Ticks_Step = None,
                         Annotations = None, File_Name = None, File_Format = 'png',
                         Legend = True, Legend_Location = 'best', Legend_Font_Size = 12,
                         Cluster_Size = 100, Epsilon = 0.1, Min_Samples = 2, Clustering_Method = None, Jitter = None,
                         Cluster_Color = 'Blues', Perform_Regression = True, Regression_Type = 'linear', 
                         Polynomial_Degree = 2):

    plt.figure(figsize = Figure_Size)

    # Group points only if a clustering method is specified.
    if Clustering_Method is not None:
        Coords = np.column_stack((X, Y))

        if Clustering_Method == 'KMeans':
            N_Clusters = 3
            Kmeans = KMeans(n_clusters = N_Clusters, random_state = 0).fit(Coords)
            Labels = Kmeans.labels_

        elif Clustering_Method == 'DBSCAN':
            Clustering = DBSCAN(eps = Epsilon, min_samples = Min_Samples).fit(Coords)
            Labels = Clustering.labels_

        # Plot clusters.
        Unique_Labels = set(Labels)
        Cmap = get_cmap(Cluster_Color)  # Get the specified color map.

        for Label in Unique_Labels:
            if Label == -1:  # Noise.
                continue  
            Cluster_X = X[Labels == Label]
            Cluster_Y = Y[Labels == Label]
            Cluster_Size_Actual = len(Cluster_X)  # Size of the cluster.

            # Calculate a color based on the size of the cluster (larger = more intense).
            Color_Intensity = min(1.0, Cluster_Size_Actual / max(len(X), 1)) * 8  # Scale to 1.0.
            Color = Cmap(Color_Intensity)

            plt.scatter(np.mean(Cluster_X), np.mean(Cluster_Y), s = Cluster_Size * Cluster_Size_Actual, alpha = Alpha, 
                        label = f'Cluster {Label}', color = Color)

        # Plot points not in clusters.
        Points_Not_In_Clusters = Labels == -1
        plt.scatter(X[Points_Not_In_Clusters], Y[Points_Not_In_Clusters], color = 'gray', alpha = Alpha, 
                    label = None)
    else:
        # If no clustering method is specified, plot all points individually.
        plt.scatter(X, Y, color = Colors, alpha = Alpha, label = None)

    if Perform_Regression:
        X_Reshaped = np.array(X).reshape(-1, 1)
        Y_Reshaped = np.array(Y)
        R = np.corrcoef(X, Y)[0, 1]

        if Regression_Type == 'linear':
            Model = LinearRegression().fit(X_Reshaped, Y_Reshaped)
            Y_Pred = Model.predict(X_Reshaped)
            plt.plot(X, Y_Pred, color = 'red', label = f'R = {R:.2f}', linewidth = 2)

        elif Regression_Type == 'polynomial':
            P = Polynomial.fit(X, Y, Polynomial_Degree)
            X_Fit = np.linspace(min(X), max(X), 100)
            Y_Fit = P(X_Fit)
            plt.plot(X_Fit, Y_Fit, color = 'red', label = f'Polynomial Regression (Degree {Polynomial_Degree})', linewidth = 2)

    if Title:
        plt.title(Title, fontsize = Font_Size)

    plt.xlabel(X_Label, fontsize = Font_Size)
    plt.ylabel(Y_Label, fontsize = Font_Size)

    if Legend:
        plt.legend(loc = Legend_Location, fontsize = Legend_Font_Size)

    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')

    plt.show()

def Create_Violin_Plot(Data, Title = None, X_Label = 'X', Y_Label = 'Y', Colors = None, Grid = True, Figure_Size = (10, 6), 
                        Font_Size = 12, Alpha = 1.0, X_Ticks = None, Y_Ticks = None, 
                        X_Ticks_Step = None, Y_Ticks_Step = None, 
                        Annotations = None, File_Name = None, File_Format = 'png', 
                        Legend = False, Legend_Location = 'best', Legend_Font_Size = 12):
    
    plt.figure(figsize = Figure_Size)
    
    plt.violinplot(Data, showmeans=True, showmedians=True)
    
    if Title:
        plt.title(Title, fontsize = Font_Size)
    plt.xlabel(X_Label, fontsize = Font_Size)
    plt.ylabel(Y_Label, fontsize = Font_Size)
    
    Combined_X_Ticks = set()
    if X_Ticks is not None:
        Combined_X_Ticks.update(X_Ticks)
    if X_Ticks_Step is not None:
        Combined_X_Ticks.update(np.arange(1, len(Data) + 1, step = X_Ticks_Step))
    
    plt.xticks(sorted(Combined_X_Ticks))
    
    Combined_Y_Ticks = set()
    if Y_Ticks is not None:
        Combined_Y_Ticks.update(Y_Ticks)
    if Y_Ticks_Step is not None:
        Combined_Y_Ticks.update(np.arange(min(np.concatenate(Data)), max(np.concatenate(Data)) + 1, step = Y_Ticks_Step))
    
    plt.yticks(sorted(Combined_Y_Ticks))

    if Grid:
        plt.grid(True)
    
    if Annotations:
        for annotation in Annotations:
            plt.annotate(annotation['text'], xy = annotation['xy'], xytext = annotation['xytext'], 
                         arrowprops = annotation.get('arrowprops', {}))
    
    if Legend:
        plt.legend(loc = Legend_Location, fontsize = Legend_Font_Size)
    
    if File_Name:
        plt.savefig(f'{File_Name}.{File_Format}', format = File_Format, bbox_inches = 'tight')
    
    plt.show()

#######################################################################################################################
# GROUP #
#######################################################################################################################

# No está bien hecha.
def Create_Subplots(Plot_Functions, Titles = None, Rows = 1, Columns = 1, Figure_Size = (15, 10), Shared_X_Axis = False, Shared_Y_Axis = False):

    """
    Creates a grid of subplots and applies specified plotting functions to each subplot.

    Parameters:
        - Plot_Functions (list of callable): List of functions to generate plots.
        - Titles (list of str, optional): Titles for each subplot. Default is None.
        - Rows (int, optional): Number of rows in the subplot grid. Default is 1.
        - Columns (int, optional): Number of columns in the subplot grid. Default is 1.
        - Figure_Size (tuple, optional): Size of the figure in inches. Default is (15, 10).
        - Shared_X_Axis (bool, optional): If True, share the x-axis among subplots. Default is False.
        - Shared_Y_Axis (bool, optional): If True, share the y-axis among subplots. Default is False.

    Example:
        def Sample_Plot(Title=None):
            plt.plot([1, 2, 3], [4, 5, 6])
            if Title:
                plt.title(Title)

        Create_Subplots(
            Plot_Functions=[lambda Title: Create_Line_Plot(X, Y1, Title=Title),
                            lambda Title: Create_Histogram(Y2, Title=Title)],
            Titles=['First Plot', 'Second Plot'],
            Rows=1,
            Columns=2)

    """

    Figure, Axis_List = plt.subplots(nrows = Rows, ncols = Columns, figsize = Figure_Size, sharex = Shared_X_Axis, sharey = Shared_Y_Axis)
    
    for Index, Plot_Function in enumerate(Plot_Functions):
        Axis = Axis_List[Index // Columns, Index % Columns] if Rows > 1 else Axis_List[Index]
        plt.sca(Axis)
        
        if Titles and Index < len(Titles):
            Title = Titles[Index]
        else:
            Title = None
            
        Plot_Function(Title=Title)
        
    plt.tight_layout()
    plt.show()

#######################################################################################################################
# CORRELATIONS #
#######################################################################################################################

def Correlation_Heatmap(df: pd.DataFrame, Title = None, X_Label = None, Y_Label = None, File = None, Figure_Size = (9, 9), Decimals = 2, 
                        Correlation_Method = 'pearson'):
    
    """
    Creates a half-masked heatmap of the correlation matrix from the input DataFrame.
    Only the lower triangular part of the heatmap is shown, while the upper part is masked.

    Example:
    Half_Masked_Correlation_Heatmap(df, Title="Correlation Heatmap", File="heatmap.png")

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    Title (str): Title of the heatmap.
    X_Label (str): Label for the x-axis.
    Y_Label (str): Label for the y-axis.
    File (str): File name to save the heatmap.
    Figure_Size (tuple): Size of the figure.
    Decimals (int): Number of decimal places to display in annotations.
    Correlation_Method (str): Method for calculating correlation ('pearson', 'spearman', or 'kendall').

    """

    plt.figure(figsize = Figure_Size)
    sns.set(font_scale = 1)

    Correlation_Matrix = df.corr(method = Correlation_Method)

    # Mask of zeros with the same size as the correlation matrix.
    Mask = np.zeros_like(Correlation_Matrix)

    # Hide the upper part of the matrix.
    Mask[np.triu_indices_from(Mask)] = True

    # Create the heatmap with specified decimals in annotations.
    with sns.axes_style('white'):
        sns.heatmap(Correlation_Matrix, mask = Mask, annot = True, fmt = f'.{Decimals}f', cmap = 'coolwarm')

    if Title:
        plt.title(Title)
    if X_Label:
        plt.xlabel(X_Label)
    if Y_Label:
        plt.ylabel(Y_Label)

    if File:
        plt.savefig(File, bbox_inches = 'tight')
    
    plt.show()

    return
