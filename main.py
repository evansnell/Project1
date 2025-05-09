import os
import csv
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from logic import CarWashApp

def read_csv_stats(path):
    """Read transaction data for start of day and end of day messages. """
    total = 0.0
    count = 0
    if os.path.exists(path):
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += float(row["Total Price"])
                count += 1
    return total, count


def main():
    data_file = "transactions_data.csv"
    sod_revenue, sod_last_transaction = read_csv_stats(data_file)
    if sod_last_transaction == 0:
        print("Start of day: $0.00 --- *no transactions yet*")
    else:
        print(f"Start of day: ${sod_revenue:.2f} --- "
              f"Last transaction number: {sod_last_transaction}")

    app = QApplication(sys.argv)
    window = CarWashApp()
    window.show()
    exit_code = app.exec()

    eod_revenue, eod_last_transaction = read_csv_stats(data_file)
    if eod_last_transaction == 0:
        print(f"End of day: ${eod_revenue:.2f} --- *still no transactions*")
        print("No sales made. ")
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

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
