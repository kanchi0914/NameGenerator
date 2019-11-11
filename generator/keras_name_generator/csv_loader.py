import csv

def load_csv(csvPath):
    with open(csvPath, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]