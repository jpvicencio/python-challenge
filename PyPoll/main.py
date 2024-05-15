import os
import csv  

# Function to find the path of the target file
def find_path(target_file):
    start_dir = os.getcwd()
    for root, dirs, files in os.walk(start_dir):
        if target_file in files:
            return os.path.relpath(os.path.join(root, target_file), start=start_dir)
    return None

# Set target filename
target_file = "election_data.csv"

# Set path for file
csvpath = find_path("election_data.csv")
if csvpath is None:
    raise FileNotFoundError

# Initialize variables
candidate_votes = {}
total_votes = 0

# Open the CSV file and read its contents
with open(csvpath, 'r') as file:
    # Create a CSV reader object with ',' as the delimiter
    csv_reader = csv.reader(file, delimiter=',')
    # Skip the header row
    next(csv_reader)
    
    # Read each row of the CSV file
    for row in csv_reader:
        # Extract the candidate name from the row
        candidate = row[2]
        # Get the total votes
        total_votes += 1
        # Update the candidate's vote count
        if candidate in candidate_votes:
            candidate_votes[candidate] += 1
        else:
            candidate_votes[candidate] = 1

# Calculate the percentage of votes each candidate won
percentage_votes = {candidate: (votes / total_votes) * 100 for candidate, votes in candidate_votes.items()}

# Display the results
print("Election Results")
print("-------------------------")
print(f"Total Votes: {total_votes}")
print("-------------------------")
for candidate, votes in candidate_votes.items():
    percentage = percentage_votes[candidate]
    print(f"{candidate}: {percentage:.3f}% ({votes})")
print("-------------------------")
winner = max(candidate_votes, key=candidate_votes.get)
print(f"Winner: {winner}")
print("-------------------------")

# Get the directory of the current script file
script_dir = os.path.dirname(__file__)
output_folder = os.path.join(script_dir, "analysis")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_file = os.path.join(output_folder, "election_results.txt")

# Export results to a text file
with open(output_file, "w") as file:
    file.write("Election Results\n")
    file.write("-------------------------\n")
    file.write(f"Total Votes: {total_votes}\n")
    file.write("-------------------------\n")
    for candidate, votes in candidate_votes.items():
        percentage = percentage_votes[candidate]
        file.write(f"{candidate}: {percentage:.3f}% ({votes})\n")
    file.write("-------------------------\n")
    winner = max(candidate_votes, key=candidate_votes.get)
    file.write(f"Winner: {winner}\n")
    file.write("-------------------------\n")

print(f"Election results have been exported to {output_file}")
