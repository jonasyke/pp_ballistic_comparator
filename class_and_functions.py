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
    with open(ballistics_table, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calibers.append(Caliber(row))
    return calibers


def available_calibers(ballistics_table):

    unique_calibers = set()

    with open(ballistics_table, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            cartridge = row.get("Cartridge")
            if cartridge:
                unique_calibers.add(cartridge.strip())
    return unique_calibers

def print_available_calibers(ballistics_table, columns=4):
    unique_calibers = sorted(available_calibers(ballistics_table))

    if not unique_calibers:
        print("No calibers found.")
        return
    max_length = max(len(cal) for cal in unique_calibers)
    padding = 4
    col_width = max_length + padding

    print("Available Calibers:")

    for i in range(0, len(unique_calibers), columns):
        row_items = unique_calibers[i:i + columns]
        formatted_row = [item.ljust(col_width) for item in row_items]
        print(''.join(formatted_row))

# print_available_calibers("ballistics_table.csv", columns=7)
