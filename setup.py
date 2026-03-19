from pathlib import Path
from setuptools import setup, find_packages


def read_metadata():
    content = Path(__file__).parent.joinpath("cli_commands", "cli_commands.py").read_text(encoding="utf-8")
    version = None
    project_url = None
    for line in content.splitlines():
        if line.startswith("VERSION ="):
            version = line.split("=", 1)[1].strip().strip('"').strip("'")
        if line.startswith("PROJECT_URL ="):
            project_url = line.split("=", 1)[1].strip().strip('"').strip("'")
    if version is None:
        raise RuntimeError("VERSION not found in cli_commands.py")
    if project_url is None:
        raise RuntimeError("PROJECT_URL not found in cli_commands.py")
    return version, project_url


VERSION, PROJECT_URL = read_metadata()


setup(
    name='cli-commands-kit',
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cmd=cli_commands.cli_commands:main',
            'cli=cli_commands.cli_commands:main',
        ],
    },
    install_requires=[],
    author='Mouxiao Huang',
    author_email='huangmouxiao@gmail.com',
    description='A unified CLI wrapper for common terminal commands.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=PROJECT_URL,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
