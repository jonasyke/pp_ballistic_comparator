import csv


def _to_float(value):
    if value is None:
        return None
    # strip surrounding whitespace and stray quotes
    s = str(value).strip().strip('"')
    if s == "":
        return None
    try:
        return float(s)
    except Exception:
        return None


class Caliber:
    DISTANCES = [0, 100, 200, 300, 400, 500]

    def __init__(self, row):

        self.product_code = row.get("Product_Code")
        self.cartridge = row.get("Cartridge")
        self.bullet_weight = _to_float(row.get("Bullet_Weight_gr"))
        self.bullet_type = row.get("Bullet_Type")
        self.item_number = row.get("Item_Number")
        self.notes = row.get("Notes")

        self.velocity = {
            d: _to_float(row.get(f"Velocity_{'MUZ' if d == 0 else d}"))
            for d in self.DISTANCES
        }

        self.energy = {
            d: _to_float(row.get(f"Energy_{'MUZ' if d == 0 else d}"))
            for d in self.DISTANCES
        }

        self.trajectory = {
            d: _to_float(row.get(f"Trajectory_{'MUZ' if d == 0 else d}"))
            for d in self.DISTANCES
        }

    def vel(self, yards):
        return self.velocity.get(yards)

    def eng(self, yards):
        return self.energy.get(yards)

    def drop(self, yards):
        return self.trajectory.get(yards)

    def __repr__(self):
        bw = f"{self.bullet_weight}gr" if self.bullet_weight is not None else "?gr"
        return f"<{self.cartridge} {bw} {self.bullet_type}>"


def load_calibers(ballistics_table):
    calibers = []
    try:
        with open(ballistics_table, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                calibers.append(Caliber(row))
    except FileNotFoundError:
        print(f"Error: {ballistics_table} not found.")
    return calibers

def get_unique_cartridge_names(caliber_objects):
    return sorted({c.cartridge for c in caliber_objects if c.cartridge})

def print_available_calibers(caliber_objects, columns=7):
    unique_names = get_unique_cartridge_names(caliber_objects)

    if not unique_names:
        print("No calibers found.")
        return

    max_length = max(len(name) for name in unique_names)
    col_width = max_length + 4

    print("Available Calibers:")
    for i in range(0, len(unique_names), columns):
        row_items = unique_names[i:i + columns]
        print(''.join(item.ljust(col_width) for item in row_items))

def get_available_grains(caliber_objects, target_cartridge):
    grains = {
        c.bullet_weight for c in caliber_objects 
        if c.cartridge == target_cartridge and c.bullet_weight is not None
    }
    return sorted(list(grains))

def print_grains_for_caliber(caliber_objects, target_cartridge):
    grains = get_available_grains(caliber_objects, target_cartridge)
    
    if not grains:
        print(f"No data found for caliber: {target_cartridge}")
        return

    formatted_grains = [f"{g}gr" for g in grains]
    
    print(f"\nAvailable weights for {target_cartridge}:")
    print(", ".join(formatted_grains))

def find_calibers_fuzzy(caliber_objects, search_term):
    search_term = search_term.lower().strip()

    all_names = {c.cartridge for c in caliber_objects if c.cartridge}

    matches = [name for name in all_names if search_term in name.lower()]

    return sorted(matches)

