import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow
from db import SessionLocal

def main():
    app = QApplication(sys.argv)
    
    try:
        db = SessionLocal()

    finally:
        window = MainWindow(db)
        window.show()
        app.exec()
        db.close()


if __name__ == "__main__":
    main()