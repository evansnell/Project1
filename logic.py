from PyQt6.QtWidgets import QMainWindow
from gui import Ui_MainWindow

class CarWashApp(QMainWindow):
    tax_rate = 0.07 # 7% sales tax

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

        # button functionality - button presses connect by calling the appropriate logic functions
        self.ui.cash_input.returnPressed.connect(self.process_transaction)
        self.ui.works_radioButton.toggled.connect(self.update_total)
        self.ui.ultimate_radioButton.toggled.connect(self.update_total)
        self.ui.super_radioButton.toggled.connect(self.update_total)
        self.ui.quality_radioButton.toggled.connect(self.update_total)
        self.ui.air_freshener_spinBox.valueChanged.connect(self.update_total)
        self.ui.detail_kit_spinBox.valueChanged.connect(self.update_total)

        # corrects display initialization
        self.update_total()
        self.ui.info_label.setText("Make selections")
        self.ui.change_label.setText("")

    def update_total(self):
        """Updates the subtotal, tax_amount, and total values and the total_label display.
        Recalculates everything from the start because it is called every time a new selection or deselection is made."""
        # resets totals to $0.00
        subtotal = 0.0
        total = 0.0

        # add wash package cost
        for button, price in self.package_prices.items():
            if button.isChecked():
                subtotal += price
                break

        # add add-on costs
        for spinbox, price in self.addon_prices.items():
            subtotal += spinbox.value() * price

        # calculate and add tax
        tax_amount = subtotal * CarWashApp.tax_rate
        total = subtotal + tax_amount

        # update total_label display
        self.ui.total_label.setText(f"Total: ${total:.2f} (incl. tax)")

    def process_transaction(self):
        """Validates cash input, calculates change, and updates info_label and change_label. """
        try:
            # read and convert cash input
            cash_text = self.ui.cash_input.toPlainText().strip()
            cash_input = float(cash_text)

            # verify cash input
            if cash_input < 0:
                raise ValueError

            # extract total price
            total_text = self.ui.total_label.text().replace("Total: $", "").replace(" (incl. tax)", "").strip()
            total = float(total_text)

            # check for insufficient cash
            if cash_input < total:
                self.ui.info_label.setText("Insufficient cash")
                self.ui.change_label.setText("")
                return

            # calculate change breakdown
            change = round(cash_input - total, 2)
            dollars = int(change)
            remaining = round(change - dollars, 2)
            cents = int(round(remaining * 100))

            quarters = cents // 25
            cents %= 25
            dimes = cents // 10
            cents %= 10
            nickels = cents // 5
            cents %= 5
            pennies = cents

            # update info_label for a successful transaction
            self.ui.info_label.setText("Transaction Complete!")

            # build and update change_label formatted the way I want it
            if change > 0:
                change_parts = []
                if dollars:
                    change_parts.append(f"{dollars} Dollars")
                if quarters:
                    change_parts.append(f"{quarters} Quarters")
                if dimes:
                    change_parts.append(f"{dimes} Dimes")
                if nickels:
                    change_parts.append(f"{nickels} Nickels")
                if pennies:
                    change_parts.append(f"{pennies} Pennies")
                change_text = f"Change is ${change:.2f} - " + ", ".join(change_parts)
            else:
                change_text = "Exact Amount! - No change"
            self.ui.change_label.setText(change_text)

            # handle non-numeric or negative inputs
        except ValueError:
            self.ui.info_label.setText("Invalid cash input")
            self.ui.change_label.setText("")