from pathlib import Path
from datetime import date
from pandas import DataFrame
import json

class FileManager:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parents[2]
        self.directories = ["incoming", "processed", "archive", "failed"]
        
    def make_base_dirs_if_not_exists(self):
        """Creates directories for /incoming/, /processed/, /archive/, and /failed/ if they don't already exist"""
        base = Path.cwd()
        for directory in self.directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)
            try:
                (self.base_path / directory).chmod(mode=0o777)
            except PermissionError:
                print(f"Warning - could not chmod {self.base_path / directory}")
        return None

    def make_sub_dirs_if_not_exists(self):
        """Creates directories for the date of simulation run if they don't already exist"""
        current_date = date.today().isoformat()
        (self.base_path / "incoming" / current_date).mkdir(parents=True, exist_ok=True)
        try:
            (self.base_path / "incoming" / current_date).chmod(mode=0o777)
        except PermissionError:
            print(f"Warning - could not chmod {self.base_path / "incoming" / current_date}")
        return None

    def save_csv(self, df: DataFrame, file_name: str):
        current_date = date.today().isoformat()
        save_path = self.base_path / "incoming" / current_date / file_name
        df.to_csv(path_or_buf=save_path)
        print(f"Simulation data saved at {save_path}")
        return None

    def save_metadata(self, metadata_file, file_name: str):
        current_date = date.today().isoformat()
        save_path = self.base_path / "incoming" / current_date / file_name
        save_path.write_text(json.dumps(metadata_file))
        print(f"Metadata saved as {save_path}")
        return None
    
