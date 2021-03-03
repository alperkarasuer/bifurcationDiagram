from tkinter import *
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

def get_airfoil_coords(airfoil: str) -> tuple:
    """
    Get airfoild coords from UIUC website
    https://m-selig.ae.illinois.edu/ads/cood/__.dat
    :param airfoil:
    :return: tuple of ([x coords], [y coords], plot_title)
    """

    url = 'https://m-selig.ae.illinois.edu/ads/coord/{}.dat'.format(airfoil.lower())
    response_text = requests.get(url).text
    if 'Not Found' in response_text:
        raise NameError('{} not found in UIUC database'.format(airfoil))
    all_text = response_text.split('\n')
    x_coordinates, y_coordinates = [], []
    plot_title = ''
    for index, line in enumerate(all_text):
        if index == 0:
            plot_title = line.strip()
        else:
            try:
                line = line.strip()
                x, y = line.split(' ' * line.count(' '))
                x = float(x.strip())
                y = float(y.strip())
                if x <= 1 and y <= 1:
                    x_coordinates.append((x))
                    y_coordinates.append((y))
            except ValueError:
                continue

    return x_coordinates, y_coordinates, plot_title

def plot(airfoil):

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                dpi = 100)

    [xVal, yVal, plot_title] = get_airfoil_coords(airfoil)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(xVal,yVal)
    plot1.axis(xmin = -0.5, xmax = 1.25, ymin = -1, ymax = 1)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                            master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("500x500")
text_font = ('Times New Roman', 14)
airFoilName = StringVar()

input_field = Entry(window, borderwidth = 2, relief = 'sunken', textvariable = airFoilName, font=text_font)
input_field.pack()

# button that displays the plot
plot_button = Button(master = window,
                    command = lambda: plot(airFoilName.get()),
                    height = 2,
                    width = 10,
                    text = "Plot")

# place the button
# in main window
plot_button.pack()

# run the gui
window.mainloop()
