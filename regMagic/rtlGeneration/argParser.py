import argparse
import sys


class argParser():
    def __init__(self):
        self.args = self.parseArgs()

    def checkNoArgs(self):
        if len(sys.argv) == 1:
            print("No options passed to tcg. Please use \"<script> -h\" to check command-line options.")
            sys.exit(1)

    def parseArgs(self):
        self.checkNoArgs()
        parser = argparse.ArgumentParser(description='Process register blocks from an Excel file.\n\n', formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--block', type=str, required=True, help='Block name in the Excel file.\n\n', metavar='<block>')
        parser.add_argument('-i', '--input', type=str, required=True, help='Excel file to read from.\n\n', metavar='<INPUT_FILENAME>')
        parser.add_argument('--mname', type=str, required=False, help='Macro name for the register block.\n\n', metavar='<mname>')
        parser.add_argument('--fname', type=str, required=False, help='Filename for the register specification.\n\n', metavar='<fname>')
        parser.add_argument('--dname', type=str, required=False, help='Filename for the register macros.\n\n', metavar='<dname>')
        parser.add_argument('--cname', type=str, required=False, help='Filename for the client macros.\n\n', metavar='<cname>')
        parser.add_argument('--block_addr', type = str, required=True, help='Block address')
        parser.add_argument('-o', '--output', type = str, required = True, help='Path to output the generated files', metavar = '<OUTPUT_PATH>')
        try:
            # Parse arguments
            return parser.parse_args()
        except argparse.ArgumentError as e:
            #print(f"Argument Error: {str(e)}\n")
            self.handle_error(str(e))

    def handle_error(self, message):
        print(f"Error: {message}")
        print("\nUsage: xl_reader [-h]")
        print("\nPlease refer to the documentation or use 'tcg -h' for more information.")
        sys.exit(1)

    def getArgs(self):
        return self.args
