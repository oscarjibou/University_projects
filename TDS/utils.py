from matplotlib import pyplot as plt
from numpy.typing import ArrayLike


def continuous_time_plot(*args: ArrayLike, variable_name: str, xlabel="Time (s)"):

    plt.figure(figsize=(10, 5))
    plt.plot(*args)
    plt.title("Señal en el dominio del tiempo continuo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.show()


def discrete_time_plot(*args: ArrayLike, variable_name: str, xlabel="Time (s)"):

    plt.figure(figsize=(10, 5))
    plt.stem(*args)
    plt.title("Señal en el dominio del tiempo discreto")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.show()
