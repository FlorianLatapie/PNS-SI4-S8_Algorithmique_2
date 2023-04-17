from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='cp4_ai',
    version='0.1.6',
    packages=find_packages(),
    url='',
    license='',
    author='Eric Pascual',
    author_email='',
    description='',
    python_requires='>=3.9.2',
    install_requires=Path('requirements.txt').read_text(),
    entry_points={
        'console_scripts': [
            'cp4-ai=cp4_ai.main:main',
            'cp4-play=cp4_ai.play:main'
        ]
    }
)
