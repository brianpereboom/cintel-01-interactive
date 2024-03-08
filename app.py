import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render
from scipy.stats.stats import pearsonr

with ui.sidebar():
    # 1. A string id ("selected_number_of_bins") that uniquely identifies this input value. 
    # 2. A string label ("Number of Bins") to be displayed alongside the slider.
    # 3. An integer representing the minimum number of bins (1).
    # 4. An integer representing the maximum number of bins (100).
    # 5. An integer representing the initial value of the slider (20).
    ui.input_slider("selected_number_of_bins", "Number of Bins", 1, 100, 20)

    # Standard deviation in the x direction (min=0, max=1, default=0.25, step=0.01)
    ui.input_slider("xsd", "XStDev", 0, 1, 0.25, step=0.01)
    # Standard deviation in the y direction (min=0, max=1, default=0.75, step=0.01)
    ui.input_slider("ysd", "YStDev", 0, 1, 0.75, step=0.01)
    # Correlation between x and y (min=-1, max=1, default=0.5, step=0.01)
    ui.input_slider("corr", "Corr", -1, 1, 0.5, step=0.01)

@render.plot(alt="A histogram")
def histogram():
    # Set seed for repeatable outcome
    np.random.seed(19680801)
    x = 100 + 15 * np.random.randn(437)
    plt.hist(x, input.selected_number_of_bins(), density=True)

@render.plot(alt="A scatterplot")
def scatter():
    # Seed not set so x and y will always be different
    x = np.random.randn(input.selected_number_of_bins.get())

    # Generate y such that it has the specified standard deviation and correlation
    y = np.sqrt(1 - input.corr.get() * input.corr.get()) * \
        np.random.randn(input.selected_number_of_bins.get()) + input.corr.get() * x

    # Scale x and y by their standard deviation (np.random.randn() has default standard deviation of 1)
    x = input.xsd.get() * x
    y = input.ysd.get() * y

    # Lock x and y axis
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)

    # Scatter plot (opacity is set as alpha=0.2)
    plt.scatter(x, y, alpha=0.2)
    plt.scatter(0, 0)

    # Plot linear regression (Black dotted line designated by "--k")
    # If the standard deviation of x is 0, plot a vertical line
    if input.xsd.get():
        plt.plot(np.array(range(-1, 2)) * input.xsd.get(), np.array(range(-1, 2)) * \
            np.sign(input.corr.get()) * input.ysd.get(), "--k", label='Linear regression')
    else:
        plt.plot(np.zeros(3), np.array(range(-1, 2)) * input.ysd.get(), "--k", label='Linear regression')
    plt.legend()
