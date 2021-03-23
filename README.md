## About The Project

This project allows user to import xls file with desired format and insert them into DB using import_agenda.py.  
After importing, user can search through the db using lookup_agenda.py.

## Getting Started

In order to run this project, please follow this simple steps.

### Prerequisites

1. Must have Python2 or Python3

### Installation

Assuming you have Python setup, to run locally, do the following commands. 

1. Clone the repo
   ```sh
   git clone https://github.com/TonyYounCH/agenda_import.git
   ```
2. Install the project dependencies
    ```sh
    cd agenda_import
    pip3 install pandas xlrd    // Install pandas and xlrd to execute import_agenda.py
    ```

### Usage

1. import_agenda.py  
- Accepts only one argument (xls file)
    ```sh
    python3 import_agenda.py agenda.xls
    ```

2. lookup_agenda.py
- Accepts two arguments (column and value)  
- All arguments after column will considered as one value
- Column can only be one of the following : ["date", "time_start", "time_end", "title", "location", "description", "speaker"]
    ```sh
    python3 lookup_agenda.py date 06/17/2018
    ```

