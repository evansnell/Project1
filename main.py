import sys
from PyQt6.QtWidgets import QApplication
from logic import CarWashApp

def main():
    app = QApplication(sys.argv)
    window = CarWashApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
