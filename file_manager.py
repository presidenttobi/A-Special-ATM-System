import json
from pathlib import Path

ACCOUNTS_FILE = "accounts.json"
TRANSACTIONS_FILE = "transactions.json"
BILLS_FILE = "bills.json"
CRYPTO_FILE = "crypto_wallets.json"


def load_data(filename):
    try:
        if not Path(filename).exists():
            with open(filename, "w") as file:
                json.dump([], file, indent=4)

        with open(filename, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

    except json.JSONDecodeError:
        print("The file is corrupted or has invalid JSON.")
        return []

    except PermissionError:
        print("You do not have permission to open this file.")
        return []

    except OSError as e:
        print("File error:", e)
        return []

    else:
        return data

    finally:
        pass


def save_data(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    except PermissionError:
        print("You do not have permission to save this file.")

    except OSError as e:
        print("Could not save the file:", e)

    else:
        return True

    finally:
        pass

    return False
