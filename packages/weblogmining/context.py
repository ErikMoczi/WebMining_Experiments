from .CleanUpData import CleanUpData

__all__ = ['cleanUpData']


def cleanUpData(input_file_name: str, output_file_name: str) -> None:
    cleanup = CleanUpData(input_file_name, output_file_name)
    cleanup.run()
