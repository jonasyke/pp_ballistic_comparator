from class_and_functions import load_calibers, print_available_calibers, print_grains_for_caliber
from graph import plot_caliber_data

def main():
    table = "ballistics_table.csv"
    calibers = load_calibers(table)

    print("--- Caliber Comparison ---")
    print(f"\nLoaded {len(calibers)} calibers from {table}\n")
    print_available_calibers(calibers)
    
    selected_caliber = input("\nWhich caliber are you interested in? \n")
    print_grains_for_caliber(calibers, selected_caliber)

    selected_grain = input("\nWhich Grain weight? ")





if __name__ == "__main__":
    main()
