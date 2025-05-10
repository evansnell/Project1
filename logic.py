import os
import csv
from PyQt6.QtWidgets import QMainWindow
from gui import Ui_MainWindow

class CarWashApp(QMainWindow):
    """Main application window for the Car Wash POS."""
    tax_rate = 0.07 # 7% sales tax
    csv_file = 'transactions_data.csv'

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set prices for packages and add-ons
        self.package_prices = {
            self.ui.works_radioButton: 25.00,
            self.ui.ultimate_radioButton: 20.00,
            self.ui.super_radioButton: 15.00,
            self.ui.quality_radioButton: 10.00
        }
        self.addon_prices = {
            self.ui.air_freshener_spinBox: 1.00,
            self.ui.detail_kit_spinBox: 5.00
        }

        # ensures CSV file exists with header and determines next transaction #
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Transaction #', 'Wash Package', 'Air Fresheners', 'Detail Kits', 'Total Price'])
            self.next_transaction = 1
        else:
            with open(self.csv_file, 'r', newline='') as f:
                rows = list(csv.reader(f))
            # obtains the current transaction #
            self.next_transaction = len(rows)

        # button functionality
        self.ui.calculate_Button.clicked.connect(self.update_total)
        self.ui.pay_button.clicked.connect(self.process_transaction)

        # corrects display initialization
        self.update_total()
        self.ui.info_label.setStyleSheet(None)
        self.ui.info_label.setText("Make selections")
        self.ui.change_label.setText("")

    def update_total(self):
        """Updates the subtotal, tax_amount, and total values and the total_label display."""
        # resets total to $0.00 to begin recalculating all new inputs from the start
        subtotal = 0.0

        # add wash package cost
        for button, price in self.package_prices.items():
            if button.isChecked():
                subtotal += price
                self.selected_package = button.text()
                break
        else:
            self.selected_package = ''

        # retrieve number of air fresheners and detail kits, then add costs
        for spinbox, price in self.addon_prices.items():
            subtotal += spinbox.value() * price

        # calculate and add tax
        tax_amount = subtotal * CarWashApp.tax_rate
        self.total = subtotal + tax_amount

        # update total_label display
        self.ui.total_label.setText(f"Total: ${self.total:.2f}")

    def process_transaction(self):
        """Validates cash input, calculates change, and updates info_label and change_label. """
        # verify that total_label is updated based on what is currently selected
        self.update_total()

        # validate cash input
        try:
            cash_text = self.ui.cash_input.toPlainText().strip()
            cash_input = float(cash_text)
            if cash_input < 0:
                raise ValueError
        # handle non-numeric or negative inputs
        except ValueError:
            self.ui.info_label.setText("Invalid cash input")
            self.ui.info_label.setStyleSheet("color: red;")
            self.ui.change_label.setText("")
            return

        # check for insufficient cash
        if cash_input < self.total:
            self.ui.info_label.setText("Insufficient cash")
            self.ui.info_label.setStyleSheet("color: red;")
            self.ui.change_label.setText("")
            return

        # calculate change breakdown
        change = round(cash_input - self.total, 2)
        dollars = int(change)
        cents = int(round((change - dollars) * 100))
        quarters = cents // 25
        cents %= 25
        dimes = cents // 10
        cents %= 10
        nickels = cents // 5
        cents %= 5
        pennies = cents

        # update info_label for a successful transaction
        self.ui.info_label.setText("Transaction Successful!")
        self.ui.info_label.setStyleSheet(None)

        # build and update change_label formatted the way I want it
        if change > 0:
            change_parts = []
            if dollars:
                if dollars == 1:
                    change_parts.append('1 Dollar')
                else:
                    change_parts.append(f"{dollars} Dollars")
            if quarters:
                if quarters == 1:
                    change_parts.append('1 Quarter')
                else:
                    change_parts.append(f"{quarters} Quarters")
            if dimes:
                if dimes == 1:
                    change_parts.append('1 Dime')
                else:
                    change_parts.append(f"{dimes} Dimes")
            if nickels:
                if nickels == 1:
                    change_parts.append('1 Nickel')
                else:
                    change_parts.append(f"{nickels} Nickels")
            if pennies:
                if pennies == 1:
                    change_parts.append('1 Penny')
                else:
                    change_parts.append(f"{pennies} Pennies")
            change_text = f"Change is ${change:.2f} - " + ", ".join(change_parts)
        else:
            change_text = "Exact Amount! - No change"
        self.ui.change_label.setText(change_text)

        # append new transaction to CSV as a new row
        with open (self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.next_transaction,
                self.selected_package,
                self.ui.air_freshener_spinBox.value(),
                self.ui.detail_kit_spinBox.value(),
                f"{self.total:.2f}"
            ])
            self.next_transaction += 1

        # clear out all inputs so the program is ready for a new transaction
        for button in self.package_prices:
            button.setAutoExclusive(False)
            button.setChecked(False)
            button.setAutoExclusive(True)
        for spin in self.addon_prices:
            spin.setValue(0)
        self.ui.cash_input.clear()
        self.update_total()