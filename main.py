import sys
from time import time

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from loguru import logger
from qt_material import apply_stylesheet

from src.constants import app_name, app_version, organization_name, organization_website
from src.utils import QSSLoader


def main() -> None:
    from src.utils.logger import logger_init
    logger_init()

    start_time = time()
    last_time = start_time
    logger.info("Application initializing")
    logger.trace("Creating application")
    app = QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setApplicationVersion(app_version.version)
    app.setOrganizationName(organization_name)
    app.setOrganizationDomain(organization_website)
    apply_stylesheet(app, theme="dark_teal.xml")
    logger.trace(f"Create application cost {time() - last_time:.6f}s")

    last_time = time()
    logger.trace("Importing resource")
    import resource_rc
    app.setWindowIcon(QIcon(":/icon/icon"))
    app.setStyleSheet(QSSLoader.readQssResource(":/style/style/style.qss"))
    logger.trace(f"Import resource cost {time() - last_time:.6f}s")

    last_time = time()
    logger.trace("Creating main window")
    from src.ui.main_window import MainWindow
    from src.signal import Signals, MouseSignals, KeyBoardSignals, AudioSignal
    main_window = MainWindow(Signals(), MouseSignals(), KeyBoardSignals(), AudioSignal())
    logger.trace(f"Create main window cost {time() - last_time:.6f}s")

    logger.info(f"Startup completed in {time() - start_time:.6f}s")

    main_window.show()
    exit_code = app.exec()
    resource_rc.qCleanupResources()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
