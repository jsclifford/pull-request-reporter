# Pull Request Reporter

This is a python based reporter that gets pull request data from  github and sends an email summary of a repos pull requests.

## Getting Started

In order to run this script you must install the required packages

### Pre-Requisites

* Python version 3.8.x
* Pip version 20.0.x

## Install

Run the following commands to install the required modules to run this script.

1. Run below commands
  ```python
  #Install Pylint
  pip install pylint

  # Setup virtualenv (optional)
  pip install virtualenv
  python3 -m venv env
  source env/bin/activate

  # Install required modules
  pip install -r requirements.txt
  ```
2. Rename file `.env.example` to `.env`
    * Add appropriate api keys and default email address to the file.

## Running the script

```bash
python3 pull_request_reporter.py --repository <your-repo-here> --email <your-email-address> --daysago 7
```
### Cleanup

Deactivate your python environment

```bash
deactivate
```
