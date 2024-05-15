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
target_file = "budget_data.csv"

# Set path for file
csvpath = find_path("budget_data.csv")
if csvpath is None:
    raise FileNotFoundError

# Initialize variables
unique_dates = set()
net_profit_loss = 0
previous_profit_loss = None
total_change = 0
num_changes = 0
greatest_increase = float('-inf')
greatest_decrease = float('inf')
increase_month = ""
decrease_month = ""

# Open the CSV file and read its contents
with open(csvpath, 'r') as file:
    # Create a CSV reader object with ',' as the delimiter
    csv_reader = csv.reader(file, delimiter=',')
    # Skip the header row
    next(csv_reader)
    
    # Read each row of the CSV file
    for row in csv_reader:
        # Extract the date and profit/loss value from the row
        date = row[0]
        profit_loss = int(row[1])
        # Add the date to the set of unique dates
        unique_dates.add(date)
        # Add the profit/loss value to the net profit/loss
        net_profit_loss += profit_loss
        # If this is not the first row, calculate the change in profit/loss
        if previous_profit_loss is not None:
            change = profit_loss - previous_profit_loss
            # Accumulate the total change and count the number of changes
            total_change += change
            num_changes += 1
            # Check if the change is the greatest increase or decrease so far
            if change > greatest_increase:
                greatest_increase = change
                increase_month = date
            if change < greatest_decrease:
                greatest_decrease = change
                decrease_month = date
        # Update the previous profit/loss for the next iteration
        previous_profit_loss = profit_loss

# Count the number of unique dates
total_unique_dates = len(unique_dates)

# Calculate the average change
average_change = total_change / num_changes if num_changes > 0 else 0

# Print the title, header, and results
print("Financial Analysis")
print("----------------------------")
print("Total Months: ", total_unique_dates)
print("Total: $", net_profit_loss)
print("Average Change: ${:.2f}".format(average_change))
print("Greatest Increase in Profits: {} (${})".format(increase_month, greatest_increase))
print("Greatest Decrease in Profits: {} (${})".format(decrease_month, greatest_decrease))

# Get the directory of the current script file
script_dir = os.path.dirname(__file__)
output_folder = os.path.join(script_dir, "analysis")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_file = os.path.join(output_folder, "financial_analysis.txt")

with open(output_file, "w") as file:
    file.write("Financial Analysis\n")
    file.write("-------------------------\n")
    file.write(f"Total Months: {total_unique_dates}\n")
    file.write(f"Total Profit: ${net_profit_loss}\n")
    file.write(f"Average Change: ${average_change:.2f}\n")
    file.write(f"Greatest Increase in Profits: {increase_month} (${greatest_increase})\n")
    file.write(f"Greatest Decrease in Profits: {decrease_month} (${greatest_decrease})\n")

print(f"Financial analysis have been exported to {output_file}")
