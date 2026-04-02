from setuptools import setup, find_packages

setup(
    name="pesute",
    version="1.0.0",
    description="Personal Secret Vault System (PESUTE)",
    author="Arjun Mitra",
    packages=find_packages(),
    py_modules=["main", "config"],
    include_package_data=True,
    install_requires=[
        # List dependencies from requirements.txt here manually or dynamically, e.g.:
        "cryptography",
        "rich",
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "pesute=main:landing_menu",
        ],
    },
)
