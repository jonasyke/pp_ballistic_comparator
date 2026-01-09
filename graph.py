import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from class_and_functions import Caliber, load_calibers, print_available_calibers

def plot_caliber_data(calibers, cartridge_name):
    selected_calibers = [cal for cal in calibers if cal.cartridge == cartridge_name]

    if not selected_calibers:
        print(f"No data available for cartridge: {cartridge_name}")
        return
    
    # Create the 3x1 layout
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14))
    
    distances = Caliber.DISTANCES
    
    for caliber in selected_calibers:
        # Plot 1: Velocity
        ax1.plot(distances, [caliber.vel(d) for d in distances], 
                 label=f'{caliber} (fps)')
        
        # Plot 2: Energy
        ax2.plot(distances, [caliber.eng(d) for d in distances], 
                 label=f'{caliber} (ft-lbs)')
        
        # Plot 3: Drop
        ax3.plot(distances, [caliber.drop(d) for d in distances], 
                 label=f'{caliber} (in)')

    # --- Subplot 1: Velocity ---
    ax1.set_title(f'Ballistic Comparison: {cartridge_name}', fontsize=14)
    ax1.set_ylabel('Velocity (fps)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8)

    # --- Subplot 2: Energy ---
    ax2.set_ylabel('Energy (ft-lbs)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8)

    # --- Subplot 3: Drop ---
    ax3.set_xlabel('Distance (Yards)') # Added "Yards" here
    ax3.set_ylabel('Drop (inches)')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc='lower left', fontsize=8) # 'lower left' often avoids the drop line

    # Fix layout and save
    plt.tight_layout()
    plt.savefig("ballistics_comparison.png", bbox_inches='tight')
    print("Plot saved as ballistics_comparison.png")

ballistics_table = "ballistics_table.csv"
calibers = load_calibers(ballistics_table) 
print_available_calibers(ballistics_table, columns=7)

plot_caliber_data(calibers, '6.5 x 55mm')