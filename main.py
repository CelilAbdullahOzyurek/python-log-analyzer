import sys
import readline
from analyzer import analyze_file
from monitor import start_monitoring
from reporter import export_to_csv

def print_menu():

    print("  CLI - Log analysis tool")
    print("1.Static File Analysis (Read & Summarize File)")
    print("2. Live Monitoring Mode (Real-time Tailing)")
    print("3. Create CSV (Exel) Report")
    print("4. Exit")

def main():
    while True:
        print_menu()
        choice = input("Choese between (1-4): ")

        if choice == '1':
            file_path = input("Enter the log path do you want to analysis ( /app/logs/access.log) like this ")
            analyze_file(file_path)
        elif choice == '2':
            file_path = input("Enter the log path you want to monitor live ( /app/logs/access.log) like this ")
            start_monitoring(file_path)
        elif choice == '3':
            file_path = input("Enter the log path do you want get report ( /app/logs/access.log) like this ")
            export_to_csv(file_path)
        elif choice == '4':
            print(":) Altaylardan Tunaya <3 o7 07 07 <3 ")
            sys.exit()
        else:
            print("You choose worng number please choose between (1-4)")

if __name__ == "__main__":
    main()