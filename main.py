import random
from account import create_account, login
from banking import deposit, withdraw, transfer, check_balance
from bills import pay_bill
from crypto import crypto_menu
from file_manager import load_data


quotes = [
    "Don't forget—God loves you!",
    "Small progress is still progress.",
    "Believe in yourself and keep going.",
    "You are capable of amazing things.",
    "Trust God and keep doing your best.",
    "Your future self will thank you for not giving up."
]


def show_quote():
    print(" While you wait...")
    print(random.choice(quotes))


def show_transactions(account):
    transactions = load_data("transactions.json")

    print("-----TRANSACTION HISTORY-----")

    found = False

    for transaction in transactions:
        if transaction["account_number"] == account["account_number"]:
            print(transaction)
            found = True

    if not found:
        print("No transactions yet.")


def change_pin(account):
    try:
        old_pin = input("Enter old PIN: ")

        if old_pin != account["pin"]:
            raise ValueError("Incorrect old PIN.")

        new_pin = input("Enter new 4-digit PIN: ")

        if not new_pin.isdigit() or len(new_pin) != 4:
            raise ValueError("PIN must be exactly 4 numbers.")

        if new_pin == old_pin:
            raise ValueError(
                "New PIN cannot be the same as the old PIN."
            )

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["pin"] == new_pin:
                raise ValueError(
                    "That PIN is already being used."
                )

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["pin"] = new_pin

        account["pin"] = new_pin

        from file_manager import save_data
        save_data("accounts.json", accounts)

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("PIN change error:", e)

    else:
        print("PIN changed successfully.")

    finally:
        print("PIN change process finished.")


def user_menu(account):
    while True:

        print("--------------------------------------------------")
        print("Welcome,", account["name"])
        print("Balance: ₦", format(account["balance"], " "))
        print("--------------------------------------------------")

        show_quote()

        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Check Balance")
        print("5. Change PIN")
        print("6. Universal Bill Pay")
        print("7. Cryptocurrency")
        print("8. Transaction History")
        print("9. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            deposit(account)

        elif choice == "2":
            withdraw(account)

        elif choice == "3":
            transfer(account)

        elif choice == "4":
            check_balance(account)

        elif choice == "5":
            change_pin(account)

        elif choice == "6":
            pay_bill(account)

        elif choice == "7":
            crypto_menu(account)

        elif choice == "8":
            show_transactions(account)

        elif choice == "9":
            print("You have been logged out.")
            break

        else:
            print("Invalid option. Please choose again.")


def main():
    while True:
        print("---------------------------------------")
        print("SECURE ATM BANKING")
        print("---------------------------------------")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("---------------------------------------")

        choice = input("Choose an option: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            try:
                show_quote()
                account = login()

                if account:
                    user_menu(account)

            except Exception as e:
                print("Login failed:", e)

                print("1. Try Login Again")
                print("2. Exit")

                next_choice = input("Choose: ")

                if next_choice == "2":
                    print("Goodbye!")
                    break

        elif choice == "3":
            print("Thank you for using Secure ATM.")
            break

        else:
            print("Invalid option.")


try:
    main()

except KeyboardInterrupt:
    print("Program stopped safely.")

except Exception as e:
    print("Something unexpected happened:", e)

finally:
    print("Thank you for using Secure ATM.")
