# PESUTE Personal Secret Vault

<div align="center">



[![GitHub stars](https://img.shields.io/github/stars/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault?style=for-the-badge)](https://github.com/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault?style=for-the-badge)](https://github.com/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault/network)

[![GitHub issues](https://img.shields.io/github/issues/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault?style=for-the-badge)](https://github.com/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault/issues)

[![GitHub license](https://img.shields.io/github/license/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault?style=for-the-badge)](LICENSE) <!-- TODO: Create a LICENSE file in the repository root -->

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)

**Your personal, secure, and intuitive command-line secret vault.**

</div>

## Overview

The PESUTE Personal Secret Vault is a robust command-line application designed to securely store and manage your sensitive information. Built with Python, it utilizes strong encryption to protect your passwords, API keys, notes, and any other confidential data, ensuring your digital secrets remain private and inaccessible to unauthorized eyes.

This tool provides an interactive terminal interface, allowing you to easily add, retrieve, update, and delete secrets, all secured by a master password. All secrets are stored locally in an encrypted file, giving you full control over your data.

## Features

-   **1. Secure Secret Storage**: Encrypts and stores your personal secrets locally using the powerful `cryptography` library.
-   **2. Master Password Protection**: All vault operations are protected by a single, strong master password set by you.
-   **3. Interactive CLI**: A user-friendly, color-coded command-line interface powered by `colorama` for managing your secrets.
-   **4. Configurable File Paths**: Easily adjust the storage locations for your secrets, encryption key, and master password hash via `config.py`.
-   **5. Add New Secrets**: Store new confidential entries with ease.
-   **6. Retrieve Secrets**: Securely fetch and decrypt your stored information when needed.
-   **7. Delete Secrets**: Permanently remove outdated or unwanted secrets from your vault.
-   **8. List All Secrets**: View a categorized list of all your stored secret entries.

## Tech Stack

**Runtime:**

![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)

**Libraries:**

![Cryptography](https://img.shields.io/badge/Library-Cryptography-60B044.svg?style=for-the-badge&logo=python&logoColor=white)

![Colorama](https://img.shields.io/badge/Library-Colorama-FFD43B.svg?style=for-the-badge&logo=python&logoColor=black)

**Storage:**
File-based encryption (local)

## Quick Start

Follow these steps to get your PESUTE Personal Secret Vault up and running.

### Prerequisites

-   **Python 3.x**: Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault.git
    cd PESUTE_Personal-Secret-Vault
    ```

2.  **Install dependencies**
    Use `pip` to install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    python main.py
    ```
    Upon the first run, the application will guide you through setting up your master password and initializing your secret vault files.

## Usage

After launching the application with `python main.py`, you will be presented with an interactive menu.

```bash
python main.py
```

### Main Menu Options

The main menu typically includes options such as:

-   **Add Secret**: Create a new entry, providing a name and the secret content.
-   **View Secret**: Retrieve a specific secret by its name.
-   **List Secrets**: Display all stored secret names.
-   **Delete Secret**: Remove an existing secret entry.
-   **Change Master Password**: Update your vault's master password.
-   **Exit**: Close the application.

Follow the on-screen prompts to navigate the vault and perform operations.

## Project Structure

```
PESUTE_Personal-Secret-Vault/
├── .gitignore           # Specifies intentionally untracked files to ignore
├── README.md            # Project documentation (this file)
├── config.py            # Configuration settings for the vault
├── core/                # Core logic for encryption, decryption, and file management
│   ├── __init__.py
│   └── # ... other core modules
├── features/            # Modules implementing specific vault features (e.g., add, view, delete)
│   ├── __init__.py
│   └── # ... feature modules
├── main.py              # The main entry point for the application
├── requirements.txt     # List of Python dependencies for the project
└── ui/                  # User interface components for the interactive CLI
    ├── __init__.py
    └── # ... UI related modules (e.g., menu, input handling)
```

## Configuration

The `config.py` file defines important configurable paths used by the vault to store sensitive data. You can modify these paths if you want to change where secrets, encryption keys, or the master password hash are stored.

### Configuration File: `config.py`

| Variable                     | Description                                                | Default Value          |
|-----------------------------|------------------------------------------------------------|------------------------|
| `SECRET_FILE`               | Path to the file where encrypted secrets are stored        | `secrets.enc`          |
| `KEY_FILE`                  | Path to the file that stores the encryption key            | `key.key`              |
| `MASTER_PASSWORD_HASH_FILE` | Path to the file storing the master password hash          | `master_password.hash` |

### Notes

- By default, all files are stored within the project directory for simplicity and ease of setup.
- For personal use, keeping the default configuration is recommended.
- If you modify these paths:
  - Ensure the directories exist before runtime
  - Set appropriate file permissions to protect sensitive data
  - Avoid committing sensitive files to version control (use `.gitignore`)

## Contributing

We welcome contributions to the PESUTE Personal Secret Vault! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  **Fork the repository**.
2.  **Create a new branch** for your feature or bug fix (`git checkout -b feature/your-feature-name`).
3.  **Make your changes**.
4.  **Commit your changes** with a clear message (`git commit -m 'feat: Add new feature X'`).
5.  **Push to your branch** (`git push origin feature/your-feature-name`).
6.  **Open a Pull Request**.

### Development Setup for Contributors

To set up the development environment:

1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run `python main.py` to test your changes.

## License

This project is licensed under the [LICENSE_NAME](LICENSE) - see the [LICENSE](LICENSE) file for details. <!-- TODO: Select and add a LICENSE file (e.g., MIT, Apache 2.0) -->

## Acknowledgments

-   Inspired by the need for simple, local, and secure secret management.
-   Powered by the excellent `cryptography` library for robust encryption.
-   Thanks to `colorama` for making the command-line interface visually appealing.

## Support & Contact

-   Issues: [GitHub Issues](https://github.com/TheLearnerAllTime002/PESUTE_Personal-Secret-Vault/issues) - Report bugs or suggest features here.
-   For general inquiries, you can reach out to the repository owner, TheLearnerAllTime002, via their GitHub profile.

---

<div align="center">

**⭐ Star this repo if you find it helpful for your personal secret management!**

Made with ❤️ by [TheLearnerAllTime002](https://github.com/TheLearnerAllTime002)

</div>

