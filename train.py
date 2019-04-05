import csv
import matplotlib.pyplot as plt

MILEAGE = 0
PRICE = 1
DATA, COST = 0, 1
FIG, PLOT = plt.subplots(2, 1)
AXES_DERIVATION, = PLOT[DATA].plot(0, 0, color='C1')
TO_PLOT = True


def read_file(file_path):
    dataset = []
    with open(file_path, "r") as csvfile:
        f = csv.reader(csvfile, delimiter=',')
        for row in f:
            try:
                dataset.append([float(row[0]), float(row[1])])
            except ValueError:
                pass
    return dataset


def write_file(t_0, t_1, file_path):
    with open(file_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([t_0, t_1])
    print('Saved to file \'results.csv\'')


def estimate_price(t_0, t_1, mileage):
    return t_0 + t_1 * mileage / 10000


def calc_derivates(t_0, t_1, dataset, m):
    d_0 = 0.0
    d_1 = 0.0
    for i in range(0, m):
        d_0 += estimate_price(t_0, t_1, dataset[i][MILEAGE]) - dataset[i][PRICE]
        d_1 += (estimate_price(t_0, t_1, dataset[i][MILEAGE]) - dataset[i][PRICE]) * dataset[i][MILEAGE] / 10000
    return d_0, d_1


def calc_cost(t_0, t_1, m, dataset):
    cost = 0
    for i in range(0, m):
        cost += (estimate_price(t_0, t_1, dataset[i][MILEAGE]) - dataset[i][PRICE]) ** 2
    return (1 / m) * cost


def gradient_descent(dataset, alpha=0.01, iterations=2000):
    m = len(dataset)
    cost_array = [[], []]
    t_0_temp = 0.0
    t_1_temp = 0.0
    mileage = []
    price = []

    sorted_dataset = sorted(dataset_array, key=lambda x: x[MILEAGE])
    for i in range(0, len(sorted_dataset)):
        mileage.append(sorted_dataset[i][MILEAGE])
        price.append(sorted_dataset[i][PRICE])

    for i in range(0, iterations):
        derivates = calc_derivates(t_0_temp, t_1_temp, dataset, m)
        t_0_temp -= alpha * (1.0 / m) * derivates[0]
        t_1_temp -= alpha * (1.0 / m) * derivates[1]
        cost_array[0].append(i)
        cost_array[1].append(calc_cost(t_0_temp, t_1_temp, m, dataset) / 10000)
        if TO_PLOT:
            plot_data(PLOT, mileage, price, t_0_temp, t_1_temp, cost_array[0], cost_array[1], sorted_dataset)
    return t_0_temp, t_1_temp, cost_array


def init_plot():
    PLOT[DATA].set_xlabel('Mileage')
    PLOT[DATA].set_ylabel('Price')
    PLOT[DATA].grid(True)
    PLOT[COST].set_xlabel('Iterations')
    PLOT[COST].set_ylabel('Global cost')
    PLOT[COST].grid(True)
    plt.tight_layout()


def plot_data(plot, mileage, price, t_0, t_1, cost_0, cost_1, dataset):
    PLOT[DATA].plot(mileage, price, color='C0')
    PLOT[COST].plot(cost_0, cost_1, color='C0')
    AXES_DERIVATION.set_xdata([dataset[0][MILEAGE], dataset[-1][MILEAGE]])
    AXES_DERIVATION.set_ydata([t_0 + ((t_1 * 0) / 10000), t_0 + ((t_1 * dataset[-1][MILEAGE]) / 10000)])
    plt.pause(0.00000001)
    plt.draw()


if __name__ == "__main__":
    if (TO_PLOT):
        init_plot()
    dataset_array = read_file("data.csv")
    t_0, t_1, cost = gradient_descent(dataset_array)
    print('Coefficients: T0=%.7f, T1=%.7f' % (t_0, t_1))
    write_file(t_0, t_1, 'results.csv')
    plt.savefig('results.png', dpi=300)
