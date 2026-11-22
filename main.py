
from functions import *

# Create CSV files
create_csv_files()


# ==========================================
# USER MENU
# ==========================================

def user_menu(user_id):

    while True:

        print("\n================================")
        print("           USER MENU")
        print("================================")
        print("Welcome,", user_id)
        print("1. Calculate Income Tax")
        print("2. View Previous Tax Records")
        print("3. Logout")

        choice = input("\nEnter your choice: ")

        # OPTION 1: Calculate Income Tax
        if choice == "1":

            print("\n========== TAX INFORMATION ==========")

            annual_income = get_positive_number(
                "Enter Annual Income (RM): "
            )

            tax_relief = get_positive_number(
                "Enter Total Tax Relief (RM): "
            )

            if tax_relief > annual_income:

                print("\nWarning: Tax relief exceeds annual income.")
                print("Chargeable income will be RM 0.00.")

            # Calculate income tax
            result = calculate_tax(
                annual_income,
                tax_relief
            )

            # Display tax results
            display_tax_result(result)

            # Store information in a list
            tax_list = [
                user_id,
                "USER",
                2026,
                annual_income,
                tax_relief,
                result["Chargeable Income"],
                result["Tax Before Rebate"],
                result["Tax Rebate"],
                result["Final Tax Payable"]
            ]

            # Convert list into dictionary
            tax_record = {

                "User ID": tax_list[0],
                "Test Case ID": tax_list[1],
                "Year of Assessment": tax_list[2],
                "Annual Income": tax_list[3],
                "Total Tax Relief": tax_list[4],
                "Chargeable Income": tax_list[5],
                "Tax Before Rebate": tax_list[6],
                "Tax Rebate": tax_list[7],
                "Final Tax Payable": tax_list[8]

            }

            print("\n========== TAX RECORD DICTIONARY ==========")
            print(tax_record)

            # Save tax record into CSV
            save_tax_record(tax_record)

        # OPTION 2: View Previous Records
        elif choice == "2":

            retrieve_tax_records(user_id)

        # OPTION 3: Logout
        elif choice == "3":

            print("\nYou have successfully logged out.")
            break

        else:

            print("\nInvalid choice! Please try again.")


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("\n========================================")
    print("       MALAYSIAN TAX INPUT PROGRAM")
    print("                YA 2026")
    print("========================================")

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Register New User")
        print("2. Login")
        print("3. Run Five Tax Test Cases")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        # OPTION 1: Registration
        if choice == "1":

            register_user()

        # OPTION 2: Login
        elif choice == "2":

            user_id = login_user()

            if user_id is not None:

                user_menu(user_id)

        # OPTION 3: Run Test Cases
        elif choice == "3":

            run_test_cases()

        # OPTION 4: Exit
        elif choice == "4":

            print("\nThank you for using Malaysian Tax Input Program!")
            break

        else:

            print("\nInvalid choice! Please select 1, 2, 3 or 4.")


# ==========================================
# EXECUTE MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    main()
