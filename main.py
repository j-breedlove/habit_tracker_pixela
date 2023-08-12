import datetime as dt
import os
import random

import requests
from dotenv import load_dotenv

load_dotenv("/mnt/data/.env")

USERNAME = os.getenv("PIXELA_USERNAME", input("Enter your Pixela username: "))
TOKEN = os.getenv("PIXELA_TOKEN", input("Enter your Pixela token (Keep this private!): "))
GRAPH_ID = f"graph{random.randint(1, 10000)}"  # Generating a random graph ID to avoid conflicts
pixela_endpoint = "https://pixe.la/v1/users"
headers = {"X-USER-TOKEN": TOKEN}


def create_user():
    """Creates a new user on Pixela and returns a formatted message."""
    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(pixela_endpoint, json=user_params)
    data = response.json()
    if response.status_code == 200:
        return "User created successfully!"
    return data["message"]


def create_graph():
    """Creates a new graph for the user and returns a formatted message."""
    graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
    graph_name = input("Enter the name for your habit graph (e.g., 'Coding Time'): ")
    graph_params = {
        "id": GRAPH_ID,
        "name": graph_name,
        "unit": "hours",
        "type": "float",
        "color": "ajisai",
    }
    response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return f"Graph '{graph_name}' created successfully! Access it here: https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"
    return data["message"]


def post_data():
    """Posts data to the user's graph and returns a formatted message."""
    date_entry = input("Enter the date (YYYY-MM-DD) or press enter for today: ")
    if not date_entry:
        date_entry = dt.datetime.now().strftime("%Y%m%d")
    else:
        date_entry = date_entry.replace("-", "")
    quantity_entry = input("Enter the quantity (e.g., number of hours): ")
    post_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
    post_params = {
        "date": date_entry,
        "quantity": quantity_entry,
    }
    response = requests.post(url=post_endpoint, json=post_params, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return f"Data for {date_entry} posted successfully! Access your graph here: https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"
    return data["message"]


def update_data():
    """Updates data on the user's graph and returns a formatted message."""
    date_entry = input("Enter the date (YYYY-MM-DD) of the entry you want to update: ").replace("-", "")
    quantity_entry = input("Enter the new quantity (e.g., number of hours): ")
    graph_name = input("Enter the new name for your habit graph or press enter to keep the current name: ")
    update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date_entry}"
    update_params = {"quantity": quantity_entry}
    if graph_name:
        update_params["name"] = graph_name
    response = requests.put(url=update_endpoint, json=update_params, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return f"Data for {date_entry} updated successfully! Access your graph here: https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"
    return data["message"]


def delete_data():
    """Deletes data from the user's graph and returns a formatted message."""
    date_entry = input("Enter the date (YYYY-MM-DD) of the entry you want to delete: ").replace("-", "")
    delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date_entry}"
    response = requests.delete(url=delete_endpoint, headers=headers)
    data = response.json()
    if response.status_code == 200:
        return f"Data for {date_entry} deleted successfully!"
    return data["message"]


def display_menu():
    """Displays a menu for the user to choose an action."""
    print("\n===== Pixela Tracker Menu =====")
    print("1. Create User")
    print("2. Create Graph")
    print("3. Post Data")
    print("4. Update Data")
    print("5. Delete Data")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    return choice


def main():
    """Main function to handle user choices."""
    while True:
        choice = display_menu()
        if choice == "1":
            print(create_user())
        elif choice == "2":
            print(create_graph())
        elif choice == "3":
            print(post_data())
        elif choice == "4":
            print(update_data())
        elif choice == "5":
            print(delete_data())
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
