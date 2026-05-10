import sys

from PyQt5 import QtWidgets
from application import HybridCryptoApp


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HybridCryptoApp()
    window.show()
    sys.exit(app.exec_())