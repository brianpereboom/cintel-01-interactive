import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render
from scipy.stats.stats import pearsonr

with ui.sidebar():
    ui.input_slider("n", "N", 1, 100, 20)
    ui.input_slider("xsd", "XStDev", 0, 1, 0.25, step=0.01)
    ui.input_slider("ysd", "YStDev", 0, 1, 0.75, step=0.01)
    ui.input_slider("corr", "Corr", -1, 1, 0.5, step=0.01)

@render.plot(alt="A histogram")
def histogram():
    np.random.seed(19680801)
    x = 100 + 15 * np.random.randn(437)
    plt.hist(x, input.n(), density=True)

@render.plot(alt="A scatterplot")
def scatter():
    x = np.random.randn(input.n.get())
    y = np.sqrt(1 - input.corr.get() * input.corr.get()) * np.random.randn(input.n.get()) + input.corr.get() * x
    x = input.xsd.get() * x
    y = input.ysd.get() * y
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.scatter(x, y, alpha=0.2)
    plt.scatter(0, 0)
    if input.xsd.get():
        plt.plot(np.array(range(-1, 2)) * input.xsd.get(), np.array(range(-1, 2)) * np.sign(input.corr.get()) * input.ysd.get(), "--k", label='Linear regression')
    else:
        plt.plot(np.zeros(3), np.array(range(-1, 2)) * input.ysd.get(), "--k", label='Linear regression')
    plt.legend()
