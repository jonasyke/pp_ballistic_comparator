import csv


def _to_float(value):
    """Convert a CSV field to float or return None for empty/unparseable values."""
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
        # use .get to avoid KeyError on malformed rows
        self.product_code = row.get("Product_Code")
        self.cartridge = row.get("Cartridge")
        self.bullet_weight = _to_float(row.get("Bullet_Weight_gr"))
        self.bullet_type = row.get("Bullet_Type")
        self.item_number = row.get("Item_Number")
        self.notes = row.get("Notes")

        # Load velocity, energy, trajectory into dictionaries (values may be None)
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

    # convenience methods (use .get to avoid KeyError)
    def vel(self, yards):
        return self.velocity.get(yards)

    def eng(self, yards):
        return self.energy.get(yards)

    def drop(self, yards):
        return self.trajectory.get(yards)

    def __repr__(self):
        bw = f"{self.bullet_weight}gr" if self.bullet_weight is not None else "?gr"
        return f"<{self.cartridge} {bw} {self.bullet_type}>"


### CSV Loader


def load_calibers(ballistics_table):
    calibers = []
    with open(ballistics_table, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calibers.append(Caliber(row))
    return calibers


