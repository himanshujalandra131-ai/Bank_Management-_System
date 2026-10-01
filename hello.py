
import streamlit as st
import json
import random
import string
from pathlib import Path


# =========================================================
# BANK CLASS
# =========================================================

class Bank:

    database = "data.json"
    data = []

    # ---------------- LOAD DATA ----------------

    @classmethod
    def load_data(cls):

        try:

            if Path(cls.database).exists():

                with open(cls.database, "r") as file:
                    cls.data = json.load(file)

            else:
                cls.data = []

        except Exception as error:

            st.error(f"Error loading database: {error}")
            cls.data = []

    # ---------------- SAVE DATA ----------------

    @classmethod
    def update_data(cls):

        try:

            with open(cls.database, "w") as file:
                json.dump(cls.data, file, indent=4)

        except Exception as error:

            st.error(f"Error saving database: {error}")

    # ---------------- ACCOUNT NUMBER ----------------

    @classmethod
    def account_generator(cls):

        alpha = random.choices(
            string.ascii_uppercase,
            k=3
        )

        digit = random.choices(
            string.digits,
            k=3
        )

        special = random.choices(
            "@#$%^&*",
            k=1
        )

        account = alpha + digit + special

        random.shuffle(account)

        return "".join(account)

    # ---------------- FIND USER ----------------

    @classmethod
    def find_user(cls, account_number, pin):

        for user in cls.data:

            if (
                user["acNo"] == account_number
                and user["pin"] == pin
            ):
                return user

        return None

    # ---------------- CREATE ACCOUNT ----------------

    @classmethod
    def create_account(cls, name, age, email, pin):

        if age < 18:

            return False, "You must be 18 or above."

        if len(pin) != 4 or not pin.isdigit():

            return False, "PIN must contain exactly 4 digits."

        # Check duplicate email

        for user in cls.data:

            if user["email"] == email:

                return False, "An account with this email already exists."

        account_number = cls.account_generator()

        info = {

            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "acNo": account_number,
            "balance": 0
        }

        cls.data.append(info)

        cls.update_data()

        return True, account_number

    # ---------------- DEPOSIT ----------------

    @classmethod
    def deposit_money(cls, account_number, pin, amount):

        user = cls.find_user(account_number, pin)

        if user is None:

            return False, "Account not found or incorrect PIN."

        if amount <= 0:

            return False, "Amount must be greater than 0."

        if amount > 10000:

            return False, "You cannot deposit more than ₹10,000 at once."

        user["balance"] += amount

        cls.update_data()

        return True, user["balance"]

    # ---------------- WITHDRAW ----------------

    @classmethod
    def withdraw_money(cls, account_number, pin, amount):

        user = cls.find_user(account_number, pin)

        if user is None:

            return False, "Account not found or incorrect PIN."

        if amount <= 0:

            return False, "Amount must be greater than 0."

        if amount > user["balance"]:

            return False, "Insufficient balance."

        user["balance"] -= amount

        cls.update_data()

        return True, user["balance"]

    # ---------------- DELETE ----------------

    @classmethod
    def delete_account(cls, account_number, pin):

        user = cls.find_user(account_number, pin)

        if user is None:

            return False, "Account not found or incorrect PIN."

        cls.data.remove(user)

        cls.update_data()

        return True, "Account deleted successfully."

    # ---------------- UPDATE ----------------

    @classmethod
    def update_account(
        cls,
        account_number,
        pin,
        name,
        email,
        new_pin
    ):

        user = cls.find_user(account_number, pin)

        if user is None:

            return False, "Account not found or incorrect PIN."

        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if new_pin:

            if len(new_pin) != 4 or not new_pin.isdigit():

                return False, "PIN must contain exactly 4 digits."

            user["pin"] = new_pin

        cls.update_data()

        return True, "Account updated successfully."


# =========================================================
# LOAD DATABASE
# =========================================================

Bank.load_data()


# =========================================================
# STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)


st.title("🏦 Bank Management System")

st.write("Manage your bank account easily.")


# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("Bank Menu")

option = st.sidebar.selectbox(

    "Choose Operation",

    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Account",
        "Delete Account"
    ]
)


# =========================================================
# CREATE ACCOUNT
# =========================================================

if option == "Create Account":

    st.header("📝 Create Account")

    name = st.text_input("Enter your name")

    age = st.number_input(
        "Enter your age",
        min_value=1,
        max_value=120,
        step=1
    )

    email = st.text_input("Enter your email")

    pin = st.text_input(
        "Create 4 digit PIN",
        type="password",
        max_chars=4
    )

    if st.button("Create Account"):

        if name == "" or email == "" or pin == "":

            st.warning("Please fill all fields.")

        else:

            success, result = Bank.create_account(
                name,
                age,
                email,
                pin
            )

            if success:

                st.success("Account created successfully!")

                st.info(
                    f"Your Account Number is: **{result}**"
                )

            else:

                st.error(result)


# =========================================================
# DEPOSIT
# =========================================================

elif option == "Deposit Money":

    st.header("💰 Deposit Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Deposit Amount",
        min_value=0,
        step=100
    )

    if st.button("Deposit"):

        success, result = Bank.deposit_money(
            account_number,
            pin,
            amount
        )

        if success:

            st.success("Money deposited successfully!")

            st.metric(
                "Current Balance",
                f"₹{result}"
            )

        else:

            st.error(result)


# =========================================================
# WITHDRAW
# =========================================================

elif option == "Withdraw Money":

    st.header("💸 Withdraw Money")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    amount = st.number_input(
        "Withdrawal Amount",
        min_value=0,
        step=100
    )

    if st.button("Withdraw"):

        success, result = Bank.withdraw_money(
            account_number,
            pin,
            amount
        )

        if success:

            st.success("Money withdrawn successfully!")

            st.metric(
                "Remaining Balance",
                f"₹{result}"
            )

        else:

            st.error(result)


# =========================================================
# ACCOUNT DETAILS
# =========================================================

elif option == "Account Details":

    st.header("👤 Account Details")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    if st.button("View Details"):

        user = Bank.find_user(
            account_number,
            pin
        )

        if user is None:

            st.error(
                "Account not found or incorrect PIN."
            )

        else:

            st.success("Account found!")

            st.write("### Your Details")

            st.write(
                f"**Name:** {user['name']}"
            )

            st.write(
                f"**Age:** {user['age']}"
            )

            st.write(
                f"**Email:** {user['email']}"
            )

            st.write(
                f"**Account Number:** {user['acNo']}"
            )

            st.metric(
                "Balance",
                f"₹{user['balance']}"
            )


# =========================================================
# UPDATE ACCOUNT
# =========================================================

elif option == "Update Account":

    st.header("✏️ Update Account")

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "Current PIN",
        type="password",
        max_chars=4
    )

    st.write(
        "Leave any field empty if you don't want to change it."
    )

    new_name = st.text_input(
        "New Name"
    )

    new_email = st.text_input(
        "New Email"
    )

    new_pin = st.text_input(
        "New PIN",
        type="password",
        max_chars=4
    )

    if st.button("Update Account"):

        success, result = Bank.update_account(

            account_number,
            pin,
            new_name,
            new_email,
            new_pin
        )

        if success:

            st.success(result)

        else:

            st.error(result)


# =========================================================
# DELETE ACCOUNT
# =========================================================

elif option == "Delete Account":

    st.header("🗑️ Delete Account")

    st.warning(
        "⚠️ Deleting your account cannot be undone."
    )

    account_number = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password",
        max_chars=4
    )

    confirm = st.checkbox(
        "I understand that my account will be permanently deleted."
    )

    if st.button("Delete Account"):

        if not confirm:

            st.warning(
                "Please confirm account deletion."
            )

        else:

            success, result = Bank.delete_account(
                account_number,
                pin
            )

            if success:

                st.success(result)

            else:

                st.error(result)

