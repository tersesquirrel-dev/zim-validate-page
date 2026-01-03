from datetime import datetime
import sys


################################################################################
## !!! Must rename the file to validation.py to be used. !!!
################################################################################


################################################################################
## Perform any validations here
##
## These can make inline corrections
## or add error annotations to lines
## or any other validation logic as needed.
##
## This example adds an error annotation if the
## 'Count:' line does not contain a valid
## integer value.
##
## The annotation is indended to stick out by
## using three !!!, being bold, emphasized and
## and superscripted.
################################################################################

page_file = sys.argv[1]

print(f'{datetime.now()}: Validating page file: {page_file}')

lines = open(page_file).readlines()

value_count = False
error_prefix = ' //**^{!!! '
error_suffix = ' !!!}**//'

for i, line in enumerate(lines):
    # strip existing errors
    if error_prefix in line:
        if line.endswith('\n'):
            lines[i] = line.split(error_prefix)[0] + '\n'
        else:
            lines[i] = line.split(error_prefix)[0]

for i, line in enumerate(lines):
    if line.startswith('Count:'):
        value_str = line.split(':', 1)[1]
        try:
            value_int = int(value_str)
        except ValueError:
            print(f"Warning: Invalid count value '{value_str}'")
            error_message = f'{error_prefix}INVALID COUNT{error_suffix}'

            if line.endswith('\n'):
                lines[i] = line.replace('\n', f'{error_message}\n')
            else:
                lines[i] = line + error_message

with open(page_file, 'w') as f:
    f.writelines(lines)

print(f'{datetime.now()}: Validation complete for page file: {page_file}')

