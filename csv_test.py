
from class_and_functions import load_calibers


def main():
    table = "ballistics_table.csv"
    calibers = load_calibers(table)
    print(f"Loaded {len(calibers)} calibers from {table}")

    # Print a small sample with velocities and energy
    for c in calibers[:12]:
        print(c)
        print(f"  Vel MUZ: {c.vel(0)} fps, 100yd: {c.vel(100)} fps, 500yd: {c.vel(500)} fps")
        print(f"  Energy 100: {c.eng(100)}, Drop 200: {c.drop(200)}")
        print("---")

    # Example: find cartridges matching a query
    query = "243"
    matches = [c for c in calibers if c.cartridge and query in c.cartridge]
    print(f"\nFound {len(matches)} entries for '{query}' (showing up to 5):")
    for c in matches:
        print(c, "->", c.velocity)



if __name__ == "__main__":
    main()



