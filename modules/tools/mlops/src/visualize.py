import os
import seaborn as sns
import matplotlib.pyplot as plt

class Visualizing:
    '''
    Description:
    ------------
    Plotting graphics using dictionaries as input data.
    '''
    def __init__(self):
        self.file_path = os.path.dirname(__file__)

    def plotting(self):
        pass

    def precision_recall_curve(self, *args):
        precision, recall, _ = args

        plt.plot(precision, recall)

    def roc_curve(self, *args):
        fpr, tpr, _ = args

        plt.plot(fpr, tpr)

        plt.savefig()
