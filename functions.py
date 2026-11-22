
import pandas as pd
import os

# CSV file names
USER_FILE = "users.csv"
TAX_FILE = "tax_records.csv"

# Column names for tax records
TAX_COLUMNS = [
    "User ID",
    "Test Case ID",
    "Year of Assessment",
    "Annual Income",
    "Total Tax Relief",
    "Chargeable Income",
    "Tax Before Rebate",
    "Tax Rebate",
    "Final Tax Payable"
]


# 1. CREATE CSV FILES

def create_csv_files():

    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(
            columns=["User ID", "IC Number"]
        )
        df.to_csv(USER_FILE, index=False)

    if not os.path.exists(TAX_FILE):
        df = pd.DataFrame(columns=TAX_COLUMNS)
        df.to_csv(TAX_FILE, index=False)


# 2. VALIDATE USER INFORMATION

def validate_ic(ic_number):

    return ic_number.isdigit() and len(ic_number) == 12


def validate_user_id(user_id):

    return len(user_id.strip()) > 0


# 3. REGISTER NEW USER

def register_user():

    df = pd.read_csv(
        USER_FILE,
        dtype=str,
        keep_default_na=False
    )

    print("\n========== USER REGISTRATION ==========")

    user_id = input("Enter User ID: ").strip()

    if not validate_user_id(user_id):
        print("User ID cannot be empty!")
        return False

    if user_id in df["User ID"].values:
        print("User ID already exists!")
        return False

    ic_number = input("Enter 12-digit IC Number: ").strip()

    if not validate_ic(ic_number):
        print("Invalid IC Number! Enter exactly 12 digits.")
        return False

    # Store information in a list
    user_list = [user_id, ic_number]

    # Convert list into dictionary
    user_dict = {
        "User ID": user_list[0],
        "IC Number": user_list[1]
    }

    # Convert dictionary into DataFrame
    new_user = pd.DataFrame([user_dict])

    df = pd.concat(
        [df, new_user],
        ignore_index=True
    )

    # Save information into CSV
    df.to_csv(USER_FILE, index=False)

    print("\nRegistration successful!")

    return True


# 4. USER LOGIN

def login_user():

    df = pd.read_csv(
        USER_FILE,
        dtype=str,
        keep_default_na=False
    )

    print("\n========== USER LOGIN ==========")

    user_id = input("Enter User ID: ").strip()
    password = input("Enter last 4 digits of IC: ").strip()

    for index, user in df.iterrows():

        if user["User ID"] == user_id:

            ic_number = user["IC Number"]

            if password == ic_number[-4:]:
                print("\nLogin successful!")
                return user_id

    print("\nInvalid User ID or password!")

    return None


# 5. GET VALID NUMERICAL INPUT

def get_positive_number(message):

    while True:

        try:
            value = float(input(message))

            if value < 0:
                print("Amount cannot be negative!")

            else:
                return value

        except ValueError:
            print("Invalid input! Please enter numbers only.")


# 6. CALCULATE MALAYSIAN INCOME TAX

def calculate_tax(annual_income, tax_relief):

    # Calculate chargeable income
    chargeable_income = max(
        0,
        annual_income - tax_relief
    )

    # Progressive tax brackets
    tax_brackets = [
        (5000, 0.00),
        (20000, 0.01),
        (35000, 0.03),
        (50000, 0.06),
        (70000, 0.11),
        (100000, 0.19),
        (400000, 0.25),
        (600000, 0.26),
        (2000000, 0.28),
        (float("inf"), 0.30)
    ]

    tax_before_rebate = 0
    previous_limit = 0

    # Calculate progressive tax
    for limit, rate in tax_brackets:

        taxable_amount = min(
            chargeable_income,
            limit
        ) - previous_limit

        if taxable_amount > 0:
            tax_before_rebate += taxable_amount * rate

        previous_limit = limit

        if chargeable_income <= limit:
            break

    # Calculate individual tax rebate
    if chargeable_income <= 35000:
        tax_rebate = min(400, tax_before_rebate)

    else:
        tax_rebate = 0

    # Calculate final tax payable
    final_tax = max(
        0,
        tax_before_rebate - tax_rebate
    )

    # Return calculation results
    result = {
        "Chargeable Income": round(chargeable_income, 2),
        "Tax Before Rebate": round(tax_before_rebate, 2),
        "Tax Rebate": round(tax_rebate, 2),
        "Final Tax Payable": round(final_tax, 2)
    }

    return result


# 7. DISPLAY TAX RESULTS

def display_tax_result(result):

    print("\n========== TAX CALCULATION RESULT ==========")

    print(
        f"Chargeable Income  : RM {result['Chargeable Income']:,.2f}"
    )

    print(
        f"Tax Before Rebate  : RM {result['Tax Before Rebate']:,.2f}"
    )

    print(
        f"Tax Rebate         : RM {result['Tax Rebate']:,.2f}"
    )

    print(
        f"Final Tax Payable  : RM {result['Final Tax Payable']:,.2f}"
    )


# 8. SAVE TAX RECORD

def save_tax_record(record):

    try:

        df = pd.read_csv(
            TAX_FILE,
            keep_default_na=False
        )

        # Convert dictionary into DataFrame
        new_record = pd.DataFrame([record])

        # Combine old and new records
        df = pd.concat(
            [df, new_record],
            ignore_index=True
        )

        # Save into CSV
        df.to_csv(TAX_FILE, index=False)

        print("\nTax record saved successfully!")

    except (OSError, pd.errors.EmptyDataError) as error:

        print("Error saving tax record:", error)


# 9. RETRIEVE TAX RECORDS

def retrieve_tax_records(user_id=None):

    try:

        df = pd.read_csv(TAX_FILE)

        if user_id is not None:

            df = df[
                df["User ID"].astype(str) == str(user_id)
            ]

        if df.empty:

            print("\nNo tax records found.")

        else:

            print("\n========== SAVED TAX RECORDS ==========")

            print(df.to_string(index=False))

    except FileNotFoundError:

        print("Tax records file not found!")

    except pd.errors.EmptyDataError:

        print("Tax records file is empty!")


# 10. RUN FIVE TAX TEST CASES

def run_test_cases():

    test_cases = [

        {
            "Test Case ID": "T01",
            "Annual Income": 9000,
            "Total Tax Relief": 9000
        },

        {
            "Test Case ID": "T02",
            "Annual Income": 40000,
            "Total Tax Relief": 9000
        },

        {
            "Test Case ID": "T03",
            "Annual Income": 65000,
            "Total Tax Relief": 14000
        },

        {
            "Test Case ID": "T04",
            "Annual Income": 120000,
            "Total Tax Relief": 18000
        },

        {
            "Test Case ID": "T05",
            "Annual Income": 83000,
            "Total Tax Relief": 12000
        }

    ]

    records = []

    # Process each test case
    for case in test_cases:

        result = calculate_tax(
            case["Annual Income"],
            case["Total Tax Relief"]
        )

        # Create dictionary
        record = {

            "User ID": "TEST",
            "Test Case ID": case["Test Case ID"],
            "Year of Assessment": 2026,
            "Annual Income": case["Annual Income"],
            "Total Tax Relief": case["Total Tax Relief"],

            **result
        }

        records.append(record)

    # Convert list of dictionaries into DataFrame
    new_df = pd.DataFrame(records)

    print("\n========== FIVE TAX TEST CASES ==========")

    print(new_df.to_string(index=False))

    # Read previously saved records
    try:

        old_df = pd.read_csv(
            TAX_FILE,
            keep_default_na=False
        )

        # Remove previous test cases only
        old_df = old_df[
            old_df["User ID"] != "TEST"
        ]

    except (FileNotFoundError, pd.errors.EmptyDataError):

        old_df = pd.DataFrame(columns=TAX_COLUMNS)

    # Combine previous records and new test cases
    final_df = pd.concat(
        [old_df, new_df],
        ignore_index=True
    )

    # Save all records
    final_df.to_csv(
        TAX_FILE,
        index=False
    )

    print("\nFive test cases saved successfully!")

    return new_df
