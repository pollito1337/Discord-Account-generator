import os
import random
import string
import time
import webbrowser

VERSION = "3.1"
KEY_FILE = ".activated"

VALID_KEYS = [
    "KEY-XXXX-XXXX-XXXX",
    "KEY-1234-5678-ABCD",
    "PREMIUM-9999-8888-7777",
    "FREE-1111-2222-3333"
]

DEV_MODE = False
TRIAL_MODE = False
TRIAL_USED = False


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def verify_key(key):
    prefixes = ("KEY-", "PREMIUM-", "FREE-", "MASTER-", "UNLIMITED-")

    if not key.startswith(prefixes):
        return False

    return key.upper() in [x.upper() for x in VALID_KEYS]


def activate_key():
    global TRIAL_MODE

    clear()
    print("=" * 60)
    print("             LICENSE ACTIVATION")
    print("=" * 60)

    key = input("\nEnter Key: ").strip()

    print("\nValidating key...")
    time.sleep(1)

    if verify_key(key):
        with open(KEY_FILE, "w") as f:
            f.write(key)

        TRIAL_MODE = False

        print("\n[SUCCESS] Key validated!")
        print("License activated successfully.")
        input("\nPress ENTER to continue...")
        main_menu()
    else:
        print("\n[FAILED] Invalid key!")
        input("\nPress ENTER to try again...")
        key_screen()


def trial_mode():
    global TRIAL_MODE, TRIAL_USED

    TRIAL_MODE = True
    TRIAL_USED = False

    clear()
    print("=" * 60)
    print("              TRIAL MODE ACTIVATED")
    print("=" * 60)

    print("\nTrial allows 1 test account generation.")
    input("\nPress ENTER to continue...")

    main_menu()


def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def generate_test_account():
    """
    Genera datos de prueba ficticios.
    No registra ninguna cuenta ni interactúa con Discord.
    """

    username = "TestUser" + str(random.randint(10000, 99999))
    email = f"{username.lower()}@example.com"
    password = random_string(16)

    year = random.randint(1990, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    dob = f"{year}-{month:02d}-{day:02d}"

    print("\n" + "=" * 50)
    print("           TEST ACCOUNT")
    print("=" * 50)

    print(f"\nEmail:    {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"DOB:      {dob}")

    print("\n" + "=" * 50)

    with open("Test_Accounts.txt", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write(f"Email: {email}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Password: {password}\n")
        f.write(f"DOB: {dob}\n")
        f.write("-" * 40 + "\n")

    print("\n[SAVED] Test account stored in Test_Accounts.txt")
    input("\nPress ENTER to continue...")


def generate_multiple():
    global TRIAL_USED

    if TRIAL_MODE and TRIAL_USED:
        print("\nTRIAL EXPIRED!")
        input("\nPress ENTER...")
        return

    if TRIAL_MODE:
        TRIAL_USED = True
        generate_test_account()
        return

    try:
        count = int(input("\nHow many test accounts: "))

        if count < 1:
            return

        for i in range(count):
            clear()
            print(f"Test account {i + 1} of {count}")
            generate_test_account()

    except ValueError:
        print("\nInvalid number.")
        input("Press ENTER...")


def view_accounts():
    clear()

    print("=" * 60)
    print("                 GENERATED ACCOUNTS")
    print("=" * 60)

    if os.path.exists("Test_Accounts.txt"):
        with open("Test_Accounts.txt", "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("\nNo test accounts generated yet.")

    input("\nPress ENTER...")


def instructions():
    clear()

    print("""
HOW TO USE
----------

1. Enter a license key or activate trial mode.
2. Select the test account generator.
3. Choose how many test accounts to generate.
4. The generated data is saved locally.
5. No real Discord account is created.

DEFAULT KEYS
------------

KEY-1234-5678-ABCD
PREMIUM-9999-8888-7777
FREE-1111-2222-3333
""")

    input("\nPress ENTER...")


def main_menu():
    while True:
        clear()

        status = "TRIAL MODE" if TRIAL_MODE else "ACTIVATED"

        print("=" * 60)
        print(f"       TEST ACCOUNT GENERATOR v{VERSION}")
        print("=" * 60)

        print(f"\nSTATUS: {status}")

        print("""
        [1] Generate Test Account
        [2] Generate Multiple Test Accounts
        [3] View Generated Accounts
        [4] Instructions
        [5] Exit
        """)

        choice = input("Select: ")

        if choice == "1":
            generate_multiple()

        elif choice == "2":
            generate_multiple()

        elif choice == "3":
            view_accounts()

        elif choice == "4":
            instructions()

        elif choice == "5":
            break


def key_screen():
    while True:
        clear()

        print("=" * 60)
        print(f"       TEST ACCOUNT GENERATOR v{VERSION}")
        print("=" * 60)

        print("""
        [1] Enter License Key
        [2] Activate Trial
        [3] Exit
        """)

        choice = input("Select: ")

        if choice == "1":
            activate_key()

        elif choice == "2":
            trial_mode()

        elif choice == "3":
            break


def startup():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            saved_key = f.read().strip()

        if verify_key(saved_key):
            main_menu()
            return

    key_screen()


if __name__ == "__main__":
    startup()