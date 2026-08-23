from file_manager import load_data, save_data
from banking import add_transaction


BTC_PRICE = 100000000


def crypto_menu(account):
    print("-----CRYPTO-----")
    print("This is a simulated crypto service.")
    print("Bitcoin price: ₦", format(BTC_PRICE, ","))

    print("1. Buy Bitcoin")
    print("2. Sell Bitcoin")
    print("3. View Wallet")
    print("4. Back")

    choice = input("Choose: ")

    if choice == "1":
        buy_bitcoin(account)

    elif choice == "2":
        sell_bitcoin(account)

    elif choice == "3":
        view_wallet(account)

    elif choice == "4":
        return

    else:
        print("Invalid option.")


def buy_bitcoin(account):
    try:
        amount = float(input("Amount in naira: ₦"))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if amount > account["balance"]:
            raise ValueError("Insufficient funds.")

        bitcoin = amount / BTC_PRICE

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["balance"] -= amount
                account["balance"] = item["balance"]

        wallets = load_data("crypto_wallets.json")

        wallet = None

        for item in wallets:
            if item["account_number"] == account["account_number"]:
                wallet = item
                break

        if wallet is None:
            wallet = {
                "account_number": account["account_number"],
                "bitcoin": 0
            }
            wallets.append(wallet)

        wallet["bitcoin"] += bitcoin

        save_data("accounts.json", accounts)
        save_data("crypto_wallets.json", wallets)

        add_transaction(
            account["account_number"],
            {
                "type": "Crypto Purchase",
                "amount": amount,
                "bitcoin": bitcoin
            }
        )

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Crypto error:", e)

    else:
        print("Bitcoin purchased successfully!")
        print("Bitcoin received:", bitcoin)

    finally:
        print("Crypto process finished.")


def sell_bitcoin(account):
    try:
        amount = float(input("Bitcoin to sell: "))

        wallets = load_data("crypto_wallets.json")

        wallet = None

        for item in wallets:
            if item["account_number"] == account["account_number"]:
                wallet = item
                break

        if wallet is None or wallet["bitcoin"] < amount:
            raise ValueError("You do not have enough Bitcoin.")

        naira = amount * BTC_PRICE

        wallet["bitcoin"] -= amount

        accounts = load_data("accounts.json")

        for item in accounts:
            if item["account_number"] == account["account_number"]:
                item["balance"] += naira
                account["balance"] = item["balance"]

        save_data("crypto_wallets.json", wallets)
        save_data("accounts.json", accounts)

        add_transaction(
            account["account_number"],
            {
                "type": "Crypto Sale",
                "amount": naira,
                "bitcoin": amount
            }
        )

    except ValueError as e:
        print("Error:", e)

    except Exception as e:
        print("Crypto error:", e)

    else:
        print("Bitcoin sold successfully!")
        print("You received ₦", format(naira, ","))

    finally:
        print("Crypto process finished.")


def view_wallet(account):
    wallets = load_data("crypto_wallets.json")

    for wallet in wallets:
        if wallet["account_number"] == account["account_number"]:
            print("Bitcoin:", wallet["bitcoin"])
            return

    print("Bitcoin: 0")
