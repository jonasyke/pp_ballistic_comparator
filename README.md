# PP Ballistic Comparator

Personal project: a simple **ballistic comparator** tool that compares performance characteristics of different calibers using generic/typical ballistic data.

It reads caliber data from a CSV file, processes comparisons (velocity, energy, drop, etc.), and generates a visual graph to show how one caliber stacks up against another.

## What it does

- Loads ballistic coefficient / velocity / bullet weight / etc. data from `ballistics_table.csv`
- Compares up to four calibers side-by-side
- Calculates key metrics (likely muzzle energy, trajectory, sectional density, etc.)
- Outputs a comparison graph saved as `ballistics_comparison.png` (or displayed)

Useful for quick "what if" comparisons when choosing loads, understanding cartridge performance differences, or learning ballistics basics.

## Features (current)

- CSV-based data input
- Modular class/function structure for ballistic calculations
- Matplotlib graphing of results

## Getting Started

### Prerequisites

- Python 3.8+ (developed with Python 3.10–3.12 in mind)
- Git (to clone the repo)

No `requirements.txt` is present yet — common libraries this kind of project uses are:

- matplotlib (for plotting)

### Installation & Setup

1. Clone the repository

   ```bash
   git clone https://github.com/jonasyke/pp_ballistic_comparator.git
   # or with SSH: git clone git@github.com:jonasyke/pp_ballistic_comparator.git


.
