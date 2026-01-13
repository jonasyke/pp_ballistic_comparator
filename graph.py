import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_caliber_data(selected_objects):
    if not selected_objects:
        return
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14))
    distances = [0, 100, 200, 300, 400, 500]
    

    for obj in selected_objects:
        label = f"{obj.cartridge} {obj.bullet_weight}gr"
        
        ax1.plot(distances, [obj.vel(d) for d in distances], marker='o', label=f'{label} (fps)')
        ax2.plot(distances, [obj.eng(d) for d in distances], marker='o', label=f'{label} (ft-lbs)')
        ax3.plot(distances, [obj.drop(d) for d in distances], marker='o', label=f'{label} (in)')


    thresholds = [
        (1500, 'red', '1500 ft-lbs (Large Game)'),
        (1000, 'darkorange', '1000 ft-lbs (Medium Game)')
    ]

    for value, color, text_label in thresholds:

        ax2.axhline(y=value, color=color, linestyle='--', linewidth=1.5, alpha=0.7)

        ax2.text(5, value + 20, text_label, color=color, fontsize=9, fontweight='bold')

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