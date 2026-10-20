# Archivo: setup.py
from setuptools import setup, find_packages

setup(
    name='bot_trm_usd',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "unidecode>=1.3.8"
    ],
    entry_points={
        'console_scripts': [
            'trm_usd = bot_trm_usd.main:main',
        ],
    },
)