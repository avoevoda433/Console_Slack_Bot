from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Slack-App',
    version='1.0.0',
    package_dir={'message_slack_bot': 'message_slack_bot',
                 'message_slack_bot.app': 'message_slack_bot/app',
                 'message_slack_bot.menu': 'message_slack_bot/menu'},
    packages=['message_slack_bot', 'message_slack_bot.app', 'message_slack_bot.menu'],
    package_data={'message_slack_bot': ['.env']},
    install_requires=requirements,
    author="Alexey Voevoda",
    author_email="AVayavoda@gomel.iba.by",
    description="App for the Slack workspace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'message_slack_bot = message_slack_bot.start:main'
        ]
    })
