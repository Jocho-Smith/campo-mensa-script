from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
import argparse



class bcolors:
        RESET = "\x1b[0m"
        RED = "\x1b[31m"
        ERROR = "\x1b[5m\x1b[31m"
        MAYO = "\x1b[107m\x1b[30m"

MAYODISHES = [
        "herzoginkartoffeln",
        "kroketten",
        "kartoffelkroketten",
        "pommesfrites",
        "bratkartoffeln",
        "potatowedges",
        "kartoffelbälchen", #this is to cover a typo on the mensa webseite.... bälchen..
        "kartoffelbällchen",
        "rundekartoffelkroketten",
]



# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Define keywords to filter for (case insensitive)
keywords = ["eintopf", "suppe", "minestrone"]

# Create an argument parser
parser = argparse.ArgumentParser(description="This script returns the meals of today in the Campo Mensa")

# Add optional arguments
parser.add_argument("-e", action="store_true", help="Print only when keywords \"suppe\" or \"eintopf\" are found")
parser.add_argument("-d", type=str, help="Specify a custom date in the format 'YYYY-MM-DD'")
parser.add_argument("-c", action="store_true", help="Color the meals according to -e (red) and Mayo-compatibilirt")

# Parse the arguments
args = parser.parse_args()

# Update the current_date if -d argument is provided
if args.d:
    current_date = args.d

# prepare curl command
bash_command = f"curl \"https://www.studierendenwerk-bonn.de/index.php?ajax=meals\" -d \"date={current_date}&canteen=2&L=0\""

# Execute the command
result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode != 0:
    print("Command failed with error:")
    print(result.stderr)
    exit(1)

# Import the HTML into a parser
soup = BeautifulSoup(result.stdout, 'html.parser')



# Function to check if a string contains any of the keywords
def contains_keyword(string, keywords):
    for keyword in keywords:
        if keyword.lower() in string.lower():
            return True
    return False

print(f"The meal for {current_date}:")
print()

# Function to do fancy colored printing
def colored_print(text):
    if contains_keyword(text, keywords):
        print(f"{bcolors.RED}{text}{bcolors.RESET}")
    elif contains_keyword(text, MAYODISHES):
        print(f"{bcolors.MAYO}{text}{bcolors.RESET}")
    else:
        print(text)



# Print 'h5_tag' content based on the -e argument
for h5_tag in soup.find_all('h5'):
    text = h5_tag.text.strip()
    if args.e:
        if contains_keyword(text, keywords):
            if args.c:
                colored_print(text)
            else:
                print(text)
    else:
        if args.c:
            colored_print(text)
        else:
            print(text)


