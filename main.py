from class_and_functions import load_calibers, print_available_calibers

def main():
    table = "ballistics_table.csv"
    calibers = load_calibers(table)

    print(f"\nLoaded {len(calibers)} calibers from {table}\n")

    print_available_calibers(table, columns=7)



if __name__ == "__main__":
    main()
