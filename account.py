from getpass import getpass
from datetime import datetime

from file_manager import load_data, save_data
from custom_exceptions import (
    InvalidPinError,
    DuplicateAccountError,
    DuplicatePinError,
    AccountNotFoundError,
    AccountLockedError
)


def check_pin(pin):
    if not pin.isdigit() or len(pin) != 4:
        raise InvalidPinError("PIN must contain exactly 4 numbers.")


def create_account():
    accounts = load_data("accounts.json")

    print("-----CREATE ACCOUNT-----")

    try:
        name = input("Full name: ").strip()

        if name == "":
            raise ValueError("Name cannot be empty.")

        account_number = input("Account number: ").strip()

        if account_number == "":
            raise ValueError("Account number cannot be empty.")

        for account in accounts:
            if account["account_number"] == account_number:
                raise DuplicateAccountError(
                    "That account number already exists."
                )

        pin = input("Create 4-digit PIN: ")
        check_pin(pin)

        for account in accounts:
            if account["pin"] == pin:
                raise DuplicatePinError(
                    "That PIN is already being used."
                )

        confirm_pin = input("Confirm PIN: ")

        if pin != confirm_pin:
            raise InvalidPinError("The PINs do not match.")

        balance_input = input("Starting balance: ₦").strip()

        if balance_input == "":
            raise ValueError("Balance cannot be empty.")

        balance = float(balance_input)

        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")

        new_account = {
            "name": name,
            "account_number": account_number,
            "pin": pin,
            "balance": balance,
            "locked": False,
            "last_login": "Never",
            "daily_withdrawal": 0
        }

        accounts.append(new_account)

        if save_data("accounts.json", accounts):
            print("\nAccount created successfully!")

    except InvalidPinError as e:
        print("Error:", e)

    except DuplicateAccountError as e:
        print("Error:", e)

    except DuplicatePinError as e:
        print("Error:", e)

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Something went wrong:", e)

    else:
        print("You can now log in.")

    finally:
        print("----------------------------------")


def login():
    accounts = load_data("accounts.json")

    print("-----LOGIN-----")

    account_number = input("Account number: ").strip()

    account = None

    for item in accounts:
        if item["account_number"] == account_number:
            account = item
            break

    if account is None:
        raise AccountNotFoundError("Account does not exist.")

    if account["locked"]:
        raise AccountLockedError(
            "This account is currently locked."
        )

    attempts = 3

    while attempts > 0:
        try:
            pin = input("PIN: ")

            if pin != account["pin"]:
                attempts -= 1
                print("Incorrect PIN.")
                print("Attempts remaining:", attempts)

                if attempts == 0:
                    account["locked"] = True
                    save_data("accounts.json", accounts)
                    raise AccountLockedError(
                        "Account locked after 3 failed attempts."
                    )

            else:
                account["locked"] = False
                account["last_login"] = datetime.now().strftime(
                    "%d/%m/%Y %I:%M %p"
                )

                save_data("accounts.json", accounts) 

                print("Login successful!")
                return account

        except AccountLockedError:
            raise

        except Exception as e:
            print("Login error:", e)

    return None


def unlock_account(account):
    account["locked"] = False

    accounts = load_data("accounts.json")

    for item in accounts:
        if item["account_number"] == account["account_number"]:
            item["locked"] = False

    save_data("accounts.json", accounts)
