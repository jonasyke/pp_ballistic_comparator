from class_and_functions import load_calibers, collect_user_selections
from graph import plot_caliber_data

def print_ballistics_comparison(selected_objects):
    """Prints Velocity, Energy, and Trajectory tables with perfect mathematical alignment."""
    distances = [0, 100, 200, 300, 400, 500]
    
    name_width = 38
    data_width = 12
    total_width = name_width + (len(distances) * data_width)
    
    sections = [
        ("VELOCITY (fps)", "vel"),
        ("ENERGY (ft-lb)", "eng"),
        ("TRAJECTORY (in)", "drop")
    ]

    for title, method_name in sections:

        print(f"\n{title.center(total_width)}")
        
        header = f"{'Cartridge':<{name_width}}" 
        header += "".join([f"{str(d)+'yd':>{data_width}}" for d in distances])
        print(header)
        
        print("-" * total_width)

        for obj in selected_objects:
            name_label = f"{obj.cartridge} ({obj.bullet_weight}gr)"
            row = f"{name_label:<{name_width}}"
            
            for d in distances:
                val = getattr(obj, method_name)(d)
                if val is None:
                    row += f"{'--':>{data_width}}"
                else:
                    fmt = ".1f" if method_name == "drop" else ".0f"
                    row += f"{val:>{data_width}{fmt}}"
            print(row)
    pass

def main():
    table_file = "ballistics_table.csv"
    all_calibers = load_calibers(table_file)

    width = 110
    print("=" * width)    
    print("Welcome to the Ballistics Comparator".center(width))
    print("=" * width)
    
    selections = collect_user_selections(all_calibers)
    
    if not selections:
        print("\nNo selections made. Exiting.")
        return

    matched_objects = []
    for name, grain in selections:
        target_grain = float(grain)
        for obj in all_calibers:
            if obj.cartridge == name and obj.bullet_weight == target_grain:
                matched_objects.append(obj)
                break

    print("\n" + "=" * width)
    print("FINAL BALLISTICS COMPARISON".center(width))
    print("=" * width)
    print_ballistics_comparison(matched_objects)

    plot_caliber_data(matched_objects)

if __name__ == "__main__":
    main()
