![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Code Coverage](https://codecov.io/gh/pikulo-kama/kama-util/branch/master/graph/badge.svg)
# <img src="assets/kama-logo.svg" alt="Kama Logo" width="auto" height="100"/> kama-util (kutil)

A comprehensive Python utility library built with a **src-layout** to provide clean, modular tools for common development challenges. 
This library streamlines tasks ranging from localized date formatting to advanced unit testing mocks.

---

## Features

* **📅 Date Utilities (`kutil.date`)**: Transform ISO strings into localized objects and generate human-readable date/time strings using `Babel` and `pytz`.
* **📂 File System (`kutil.file`)**: Robust methods for reading/saving JSON, calculating file checksums (SHA256), and recursively cleaning directories.
* **📝 Logging (`kutil.logger`)**: Pre-configured `TimedRotatingFileHandler` with midnight rotation and support for external JSON-based logback configurations.
* **⚙️ Process Tools (`kutil.process`)**: Identify running processes by name and detect duplicate instances while handling `psutil` exceptions.
* **🧪 Testing Tools (`kutil.pytest`)**: Includes a powerful path resolution engine that automatically maps test files to their corresponding source modules for effortless mocking.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
