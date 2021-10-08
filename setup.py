from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='auto_events',
    version='0.0.2',
    url="https://github.com/fedecech/auto_events",
    author="Federico Cecchinato",
    author_email="federicocech@gmail.com",  # use icloud fake email
    description="Automate tasks easily using python",
    long_description=long_description,
    license='MIT',
    packages=['auto_events', 'auto_events.form',
              'auto_events.form.microsoft', 'auto_events.form.microsoft.components'],
    install_requires=['selenium==3.141.0',
                      'O365==2.0.16', 'apscheduler==3.8.0'],
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)
