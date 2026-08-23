from file_manager import load_data, save_data
from custom_exceptions import (
    InsufficientFundsError,
    NegativeAmountError,
    AccountNotFoundError,
    SameAccountError
)


MAX_NOTES = 100
DAILY_WITHDRAWAL_LIMIT = 200000


def add_transaction(account_number, transaction):
    transactions = load_data("transactions.json")

    transaction["account_number"] = account_number

    transactions.append(transaction)

    save_data("transactions.json", transactions)


def deposit(account):
    try:
        amount = input("Enter deposit amount: ₦").strip()

        if amount == "":
            raise ValueError("Amount cannot be empty.")

        amount = float(amount)

        if amount <= 0:
            raise NegativeAmountError(
                "Deposit must be greater than zero."
            )

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["balance"] += amount
                account["balance"] = item["balance"]

        save_data("accounts.json", accounts)

        add_transaction(
            account["account_number"],
            {
                "type": "Deposit",
                "amount": amount
            }
        )

    except NegativeAmountError as e:
        print("Error:", e)

    except ValueError:
        print("Please enter a valid number.")

    except Exception as e:
        print("Deposit error:", e)

    else:
        print("Deposit successful!")
        print("New balance: ₦", format(account["balance"], ","))

    finally:
        print("Deposit process finished.")


def withdraw(account):
    try:
        amount = input("Enter withdrawal amount: ₦").strip()

        if amount == "":
            raise ValueError("Amount cannot be empty.")

        amount = float(amount)

        if amount <= 0:
            raise NegativeAmountError(
                "Withdrawal must be greater than zero."
            )

        if amount > account["balance"]:
            raise InsufficientFundsError(
                "You do not have enough money."
            )

        if  amount > account["daily_withdrawal"] or account["daily_withdrawal"] > DAILY_WITHDRAWAL_LIMIT:

            raise ValueError(
                "You have reached your daily withdrawal limit."
            )

        print("Choose your note denomination:")
        print("1. ₦100")
        print("2. ₦200")
        print("3. ₦500")
        print("4. ₦1,000")

        choice = input("Choose: ")

        denominations = {
            "1": 100,
            "2": 200,
            "3": 500,
            "4": 1000
        }

        if choice not in denominations:
            raise ValueError("Invalid denomination.")

        note = denominations[choice]

        if amount % note != 0:
            raise ValueError(
                "That amount cannot be paid using this denomination."
            )

        number_of_notes = int(amount / note)

        print("\nNumber of notes:", number_of_notes)

        if number_of_notes > MAX_NOTES:
            print(
                "Too many notes! The ATM can only dispense",MAX_NOTES,"notes at once."
            )
            print("Try a higher denomination.")
            return

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["balance"] -= amount
                item["daily_withdrawal"] += amount

                account["balance"] = item["balance"]
                account["daily_withdrawal"] = item["daily_withdrawal"]

        save_data("accounts.json", accounts)

        add_transaction(
            account["account_number"],
            {
                "type": "Withdrawal",
                "amount": amount,
                "denomination": note,
                "notes": number_of_notes
            }
        )

    except InsufficientFundsError as e:
        print("Error:", e)

    except NegativeAmountError as e:
        print("Error:", e)

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Withdrawal error:", e)

    else:
        print("Withdrawal successful!")
        print("Please take your cash.")
        print("New balance: ₦", format(account["balance"], ","))

    finally:
        print("Withdrawal process finished.")


def transfer(account):
    try:
        receiver_number = input(
            "Receiver account number: "
        ).strip()

        if receiver_number == account["account_number"]:
            raise SameAccountError(
                "You cannot transfer money to yourself."
            )

        accounts = load_data("accounts.json")

        receiver = None

        for item in accounts:
            if item["account_number"] == receiver_number:
                receiver = item
                break

        if receiver is None:
            raise AccountNotFoundError(
                "Receiver account does not exist."
            )

        amount = input("Amount to transfer: ₦").strip()

        if amount == "":
            raise ValueError("Amount cannot be empty.")

        amount = float(amount)

        if amount <= 0:
            raise NegativeAmountError(
                "Transfer amount must be greater than zero."
            )

        if amount > account["balance"]:
            raise InsufficientFundsError(
                "You do not have enough money."
            )

        account["balance"] -= amount
        receiver["balance"] += amount

        save_data("accounts.json", accounts)

        add_transaction(
            account["account_number"],
            {
                "type": "Transfer Sent",
                "amount": amount,
                "receiver": receiver_number
            }
        )

        add_transaction(
            receiver_number,
            {
                "type": "Transfer Received",
                "amount": amount,
                "sender": account["account_number"]
            }
        )

    except AccountNotFoundError as e:
        print("Error:", e)

    except SameAccountError as e:
        print("Error:", e)

    except InsufficientFundsError as e:
        print("Error:", e)

    except NegativeAmountError as e:
        print("Error:", e)

    except ValueError:
        print("Please enter a valid amount.")

    except Exception as e:
        print("Transfer error:", e)

    else:
        print("Transfer successful!")
        print("New balance: ₦", format(account["balance"], ","))

    finally:
        print("Transfer process finished.")


def check_balance(account):
    print("-----BALANCE-----")
    print("Account:", account["account_number"])
    print("Balance: ₦", format(account["balance"], ","))
