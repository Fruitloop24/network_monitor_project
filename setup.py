from setuptools import setup, find_packages

setup(
    name="linux_looker",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'colorama', 
        'netifaces'  # Add any other dependencies
    ],
    entry_points={
        'console_scripts': [
            'linux_looker=linux_monitor:main',
        ],
    },
    description="A Linux diagnostic tool for networking and system analysis.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/<your-username>/network_monitor_project",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
