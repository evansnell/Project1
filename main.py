import os
import csv
import sys
from PyQt6.QtWidgets import QApplication
from logic import CarWashApp

def read_csv_stats(path):
    """Read transaction data for start of day and end of day messages."""
    total = 0.0
    count = 0
    if os.path.exists(path):
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += float(row["Total Price"])
                count += 1
    # returns total cash amount, number of transactions (rows)
    return total, count


def main():
    data_file = "transactions_data.csv"
    # define total cash amount and number of previous transactions at the...
    # start of the day (just before the app is launched 'for the day')
    sod_revenue, sod_last_transaction = read_csv_stats(data_file)
    # start of day message
    if sod_last_transaction == 0:
        print("Start of day: $0.00 --- *no transactions yet*")
    else:
        print(f"Start of day: ${sod_revenue:.2f} --- "
              f"Last transaction number: {sod_last_transaction}")

    # launch app (starts day)
    app = QApplication(sys.argv)
    window = CarWashApp()
    window.show()
    exit_code = app.exec() # key created when app is closed

    # define total cash amount and number of transactions at the end of the day
    # (when the app is closed)
    eod_revenue, eod_last_transaction = read_csv_stats(data_file)
    # create end of day message based on number of transactions in the day
    if eod_last_transaction == 0:
        print(f"End of day: ${eod_revenue:.2f} --- *still no transactions*")
        print("No sales have been made. ")
    else:
        num_sales = eod_last_transaction - sod_last_transaction
        if num_sales == 0:
            print(f"End of day: ${eod_revenue:.2f} --- "
                  f"Last transaction number: {eod_last_transaction}")
            print("No sales made today. ")
        else:
            print(f"End of day: ${eod_revenue:.2f} --- "
                  f"Last transaction number: {eod_last_transaction}")
            plural = '' if (eod_last_transaction - sod_last_transaction) == 1 else 's'
            print(f"In {num_sales} sale{plural}, "
                  f"we made ${eod_revenue - sod_revenue:.2f} today!")

    sys.exit(exit_code) # ends program with key after the final outputs are finished

if __name__ == '__main__':
    main()
