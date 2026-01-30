from PySide6.QtCore import QObject, Signal, Slot
from models.results import RenameResult
from pathlib import Path
from services.file_service import FileService

class ReplaceWorker(QObject):
    progress = Signal(int, int)      # current, total
    finished = Signal(ReplaceResult)        # итоговый результат

    def __init__(self, files: list[Path], service: FileService):
        super().__init__()
        self.files = files
        self.service = service


    @Slot()
    def run(self):
        result = ReplaceResult()
        total = len(self.files)

        for index, file in enumerate(self.files, start=1):
            self.service.rename_one_file(file, result)
            self.progress.emit(index, total)

        self.finished.emit(result)

        if result.errors:
            self.service.log_errors(log_path, result.errors)

        return result