import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_caliber_data(selected_objects):
    """Generates graphs for the specifically selected Caliber objects."""
    if not selected_objects:
        return
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14))
    distances = [0, 100, 200, 300, 400, 500] # Or Caliber.DISTANCES
    
    for obj in selected_objects:
        label = f"{obj.cartridge} {obj.bullet_weight}gr"
        
        # Plotting Velocity
        ax1.plot(distances, [obj.vel(d) for d in distances], marker='o', label=f'{label} (fps)')
        
        # Plotting Energy
        ax2.plot(distances, [obj.eng(d) for d in distances], marker='o', label=f'{label} (ft-lbs)')
        
        # Plotting Trajectory
        ax3.plot(distances, [obj.drop(d) for d in distances], marker='o', label=f'{label} (in)')

    ax1.set_title('Ballistic Comparison', fontsize=16)
    ax1.set_ylabel('Velocity (fps)')
    ax2.set_ylabel('Energy (ft-lbs)')
    ax3.set_ylabel('Drop (inches)')
    ax3.set_xlabel('Distance (Yards)')

    for ax in [ax1, ax2, ax3]:
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best', fontsize=9)

    plt.tight_layout()
    plt.savefig("ballistics_comparison.png", bbox_inches='tight')
    print("\n" + "!" * 50)
    print("📊 Graph generated: ballistics_comparison.png")
    print("!" * 50)
