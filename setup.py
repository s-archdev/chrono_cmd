from setuptools import setup, find_packages

setup(
    name="termtasks",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "windows-curses;platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "termtasks=termtasks.__main__:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A terminal-based task scheduler and calendar",
    keywords="terminal, task scheduler, calendar, productivity",
    url="https://github.com/yourusername/termtasks",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.6",
)
