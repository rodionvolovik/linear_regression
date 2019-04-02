import os
from train import read_file, estimate_price

INPUT_FILE = 'results.csv'

if __name__ == "__main__":
    input_mileage = int(input("Please, enter mileage: "))

    t_0, t_1 = 0.0, 0.0
    if os.path.isfile(INPUT_FILE):
        thetas = read_file(INPUT_FILE)
        t_0, t_1 = thetas[0][0], thetas[0][1]

    print("Estimated price: %d" % estimate_price(t_0, t_1, input_mileage))
