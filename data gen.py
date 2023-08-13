import random
import csv
from datetime import datetime, timedelta

# Generate random transactions data with categories
def generate_random_transactions(num_transactions):
    categories = ['Appliances', 'Groceries', 'Credit Cards', 'Loans', 'Entertainment', 'Utilities', 'Travel','Restaurant', 'Other']
    transactions = []
    for _ in range(num_transactions):
        transaction_date = datetime(2023, random.randint(1, 7), random.randint(1, 28))
        transaction_type = random.choice(['deposit', 'withdrawal'])
        transaction_category = random.choice(categories)
        
        if transaction_type == 'deposit':
            transaction_amount = round(random.uniform(1, 1000), 2)  # Positive amount for deposits
        else:
            transaction_amount = round(random.uniform(-1000, -1), 2)  # Negative amount for withdrawals
        
        transactions.append([transaction_date.strftime('%Y-%m-%d'), transaction_type, transaction_amount, transaction_category])
    return transactions

# Generate 100 random transactions (you can change this number)
num_transactions = 100
transactions_data = generate_random_transactions(num_transactions)

# Save the transactions data to a CSV file
csv_file_path = 'random_banking_transactions_with_categories.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Transaction Type', 'Amount', 'Category'])
    writer.writerows(transactions_data)

print(f'{num_transactions} random banking transactions with categories saved to {csv_file_path}.')