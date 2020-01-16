import pandas as pd
import os


class Exercise:  # Parser()
    names = ['alpha', 'bravo', 'charlie', 'delta', 'echo']

    def __init__(self, filename, verbose=False):
        """ Reads CSV File from disk, collects meta-data from object

        Arguments:
            filename (str) -- [path to file]

        Keyword Arguments:
            verbose {bool} -- [enables verbose mode, default is disabled]
            (default: {False})

        Raises:
            IOError: [CSV is invalid]
            FileNotFoundError: [CSV is not found]
        """
        self.dataframe = None
        self.bodypart = None
        self.verbose = verbose

        if os.path.exists(filename):
            if filename.endswith('.csv'):
                self.filename = filename
                self.read_dataframe_from_file()

                name = os.path.splitext(os.path.basename(filename))[0]
                namesplit = name.split('_')

                self.size = int(self.dataframe.size /
                                len(self.dataframe.columns))
                self.catagorie = int(namesplit[0].replace('Cat', ''))
                self.patient = int(namesplit[1].replace('pat', ''))
                self.meting = int(namesplit[2].replace('meting', ''))
                self.oefening = int(namesplit[3].replace(
                    'oef', '').replace('.csv', ''))

                if self.verbose:
                    print('[Parser()] parser initalised [{c} {p} {m} {o}]'.
                          format(
                              c=self.catagorie,
                              p=self.patient,
                              m=self.meting,
                              o=self.oefening))
            else:
                raise IOError("File is not a valid CSV file")
        else:
            raise FileNotFoundError("CSV File Not Found")

    def read_dataframe_from_file(self):
        """Reading data from csv file, appending correct column names
        into the pandas dataframe file
        """
        self.dataframe = pd.read_csv(
            self.filename, names=list(range(30)))

        # Renaming column names to bodypart
        self.dataframe = self.dataframe.rename(
            columns={0: "thorax_r_x", 1: "thorax_r_y", 2: "thorax_r_z",
                     3: "clavicula_r_x", 4: "clavicula_r_y",
                     5: "clavicula_r_z",
                     6: "scapula_r_x", 7: "scapula_r_y", 8: "scapula_r_z",
                     9: "humerus_r_x", 10: "humerus_r_y", 11: "humerus_r_z",
                     12: "ellebooghoek_r",
                     15: "thorax_l_x", 16: "thorax_l_y", 17: "thorax_l_z",
                     18: "clavicula_l_x", 19: "clavicula_l_y",
                     20: "clavicula_l_z",
                     21: "scapula_l_x", 22: "scapula_l_y", 23: "scapula_l_z",
                     24: "humerus_l_x", 25: "humerus_l_y", 26: "humerus_l_z",
                     27: "ellebooghoek_l"})

    def find_row_index(self, rows):
        """Finds an row based on values in

        Arguments:
            [list] -- list of values that should be in the row (correct order)

        Returns:
            [int] -- [index of row in dataframe]
        """
        # Create a list of True/False values for each item in bodypart
        resultlist = self.bodypart.iloc[:, 0] == rows[0]

        # Returning the first index that is a match
        return self.bodypart[resultlist].index[0]

    def dataframe_size(self):
        """calculates the number of rows in exercise

        Returns:
            int -- numbers of rows in execersise
        """
        if self.bodypart is not None:
            return int(int(self.bodypart.size) / 3)
        else:
            return int(self.dataframe.size /
                       len(self.dataframe.columns))
