# Reg Magic-RTL Generation

## Overview

This script is designed to automate the generation of Register RTL top. It Processes Excel/IPXACT files, config files, validates them and create top-level verilog register RTL connected with specified Interface in the config file and gives the statistics about total number of flip flops and their characteristics.

## Features

- **Excel Data Processing**: Reads from Excel files, including handling errors and highlighting the errors.
- **Register RTL with AHB/APB interface wrapper**: Integrates the generated RTL 

## Requirements

- Python 3.x
- `openpyxl` library for Excel file operations
- Proper configuration settings in a `config.xlsx` file

## Installation

pip install openpyxl

## Usage

Command Line Arguments
-i, --input <filename>:(Required argument) Relative path/absolute path to the Excel file or IPXACT file 
-o, --output <filename>:(optional argument) Relative Path/absolute path to dump the generated file or archive.
-interface AHB/APB:(Required argument) Interface to generate wrapper for generated Register RTL.


## Example Commands

./xl_reader.py -i file_name.xml -o path/to/output --interface APB
./xl_reader.py -i file_name.xlsx --interface APB

## Script WorkFlow
- Initialization: Reads the file extension and create necessary intermediate files.
- Processing: Generating the Register RTL from the provided/generated excel file by reading it.
- Wrapping: Generating wrapper around the generated register RTL and the provided interface.
- Calculate Statistics: Calculate the Number of Flip flops, among them how many are resettble, non-resettable, clearable, settable Flip flops.

## Troubleshooting

