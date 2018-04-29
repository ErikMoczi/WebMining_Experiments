import os.path as path
from .CleanUpData import CleanUpData
from .database import SessionDatabase, SQLiteDatabase, STTQLengthHeuristic, RLengthHeuristic

__all__ = ['clean_up_data', 'session_identifier']


def clean_up_data(input_file_name: str, output_file_name: str) -> None:
    cleanup = CleanUpData(input_file_name, output_file_name)
    cleanup.run()


def session_identifier(input_file_name: str, stt_q: float, stt_seconds: int = 3600, navigation_ratio: float = 0.4) -> None:
    db = SQLiteDatabase(path.dirname(path.normpath(input_file_name)))
    session_database = SessionDatabase(db)
    session_database.load_data(input_file_name, stt_seconds)
    session_database.length_heuristic(RLengthHeuristic(navigation_ratio, db))
    session_database.length_heuristic(STTQLengthHeuristic(stt_q, db))
