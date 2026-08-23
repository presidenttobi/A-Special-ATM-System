from file_manager import load_data, save_data
from banking import add_transaction


def pay_bill(account):
    print("-----UNIVERSAL BILL PAY-----")

    print("1. Electricity")
    print("2. Water")
    print("3. Internet")
    print("4. Cable TV")
    print("5. Airtime")
    print("6. Traffic Fine")
    print("7. Government Fee")

    services = {
        "1": "Electricity",
        "2": "Water",
        "3": "Internet",
        "4": "Cable TV",
        "5": "Airtime",
        "6": "Traffic Fine",
        "7": "Government Fee"
    }

    try:
        choice = input("Choose a service: ")

        if choice not in services:
            raise ValueError("Invalid service.")

        reference = input("Reference number: ").strip()

        if reference == "":
            raise ValueError("Reference number cannot be empty.")

        amount = input("Amount: ₦").strip()

        if amount == "":
            raise ValueError("Amount cannot be empty.")

        amount = float(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if amount > account["balance"]:
            raise ValueError("Insufficient funds.")

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["balance"] -= amount
                account["balance"] = item["balance"]

        save_data("accounts.json", accounts)

        bills = load_data("bills.json")

        bill = {
            "account_number": account["account_number"],
            "service": services[choice],
            "reference": reference,
            "amount": amount
        }

        bills.append(bill)

        save_data("bills.json", bills)

        add_transaction(
            account["account_number"],
            {
                "type": "Bill Payment",
                "service": services[choice],
                "amount": amount
            }
        )

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Bill payment error:", e)

    else:
        print("Bill payment successful!")
        print("Service:", services[choice])
        print("Amount: ₦", format(amount, ","))
        print("New balance: ₦", format(account["balance"], ","))

    finally:
        print("Bill payment process finished.")
