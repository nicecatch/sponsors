import pandas as pd
import zipfile
import threading
import re

def sanitize_string(s):
    """Removes non-alphanumeric characters and converts to lowercase."""
    return re.sub(r'\W+', '_', s).strip('_').lower() if isinstance(s, str) else s

class CSVLoader:
    _instance = None
    _lock = threading.Lock()  # Ensure thread safety

    def __new__(cls, file_path):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._load_csv_from_zip(file_path, "list.csv")
        return cls._instance
    
    def _load_csv_from_zip(self, zip_path, csv_filename):
        """Extract a CSV file from a ZIP archive in memory and load it into Pandas."""
        
        with zipfile.ZipFile(zip_path, "r") as z:
            with z.open(csv_filename) as file:
               self._load_data(file)

    def _load_data(self, file_content):
        """Loads CSV into a Pandas DataFrame"""
        self.df = pd.read_csv(file_content, dtype=str)

        self.df.columns = [sanitize_string(col) for col in self.df.columns]
        # self.df = self.df.applymap(sanitize_string)
        self.df.fillna("", inplace=True) 

    def get_columns(self):
        """Returns list of columns in the CSV"""
        return self.df.columns.tolist()
    
    def filter_by_criteria(self, filters):
        """Filters DataFrame based on a list of column-value pairs."""
        df_filtered = self.df
        for col, value in filters:
            col = sanitize_string(col)  # Ensure column name is sanitized
            if col in df_filtered.columns:
                df_filtered = df_filtered[df_filtered[col].str.contains(value, na=False, case=False)]
        return df_filtered[:800]

    def filter_by_column(self, column_name, value):
        """Filters rows where `column_name` contains `value`"""
        return self.df[self.df[column_name].str.contains(value, na=False, case=False)]