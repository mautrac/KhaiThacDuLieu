import matplotlib.pyplot as plt

def line_plot(x, y = None, legend_name: str = None, x_formatter = None, file_name: str = None):
    fig, ax = plt.subplots()
    if y is not None:
        ax.plot(x, y)
    else:
        ax.plot(x)
    if legend_name is not None:
        plt.legend([legend_name])
    if x_formatter is not None:
        ax.xaxis.set_major_formatter(x_formatter)
        fig.autofmt_xdate()

    if file_name is not None:
        fig.savefig(file_name)
    else:
        fig.show()

def bar_plot(*data: list, color: list, xlabel, ylabel, legend_name: list, keep_x_axis = True, file_name:str = None):
    if len(data) != len(color):
        raise "Data length and color length are not equal"

    fig, ax = plt.subplots()
    for i in range(len(data)):
        try:
            temp = list(data[i])
        except TypeError as e:
            raise "Invalid data " + e
        n = len(temp)
        #print(n)
        ax.bar(range(1, n + 1), temp, color=color[i])

    if not keep_x_axis:
        ax.set_xticks([])
        ax.set_xticklabels([])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if len(legend_name) > 0:
        colors = {legend_name[i]: color[i] for i in range(len(legend_name))}
        labels = list(colors.keys())
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
        plt.legend(handles, labels)

    if file_name is not None:
        fig.savefig(file_name)
    else:
        fig.show()


def scatter_plot(*xy : list, figsize: tuple, size: list, color: list, xlabel: str = None, ylabel: str = None, legend_name: list = None, x_formatter = None, keep_x_axis = True, file_name: str = None):
    if len(xy) != len(color):
        raise "Data length and color length are not equal"
    if len(xy) != len(size):
        raise "Data length and size length are not equal"

    fig, ax = plt.subplots(figsize=figsize)
    for i in range(len(xy)):
        try:
            x = list(xy[i][0])
            y = list(xy[i][1])
        except TypeError as e:
            raise "Invalid data " + e
        ax.scatter(x=x, y=y, s=size[i], color=color[i])

    if not keep_x_axis:
        ax.set_xticks([])
        ax.set_xticklabels([])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if len(legend_name) > 0:
        fig.legend(["Record", "Null Record"])

    if x_formatter is not None:
        ax.xaxis.set_major_formatter(x_formatter)
        fig.autofmt_xdate()

    if file_name is not None:
        fig.savefig(file_name)
    else:
        fig.show()


def lines_plot(data: list, color: list, title = None, xlabel = None, ylabel = None, legend_name: list = None, file_name: str = None):

    if len(data) != len(color):
        raise "Data length and color length are not equal"
    fig, ax = plt.subplots()
    plt.title(title)

    for i in range(len(data)):
        ax.plot(data[i], color=color[i])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if legend_name is not None:
        plt.legend(legend_name, loc='lower right')

    if file_name is not None:
        fig.savefig(file_name)
    else:
        fig.show()


def multiple_plot(data, rows, cols, suptitle = None, y_labels = None, x_labels = None):

    fig, ax = plt.subplots(rows, cols)
    if suptitle is not None:
        fig.suptitle(suptitle, fontsize=20)

    t = 0
    for i in range(rows):
        for j in range(cols):
            for k in range(len(data[t])):
                if cols > 2:
                    ax[i][j].plot(data[t][k])
                else:
                    ax[i].plot(data[t][k])
            t += 1

    if y_labels is not None:
        for i in range(rows):
            if cols > 1:
                ax[i][0].set_ylabel(y_labels[i])
            else:
                ax[i].set_ylabel(y_labels[i])

    if x_labels is not None:
        for i in range(cols):
            if cols > 1:
                ax[rows - 1][i].set_xlabel(x_labels[i])
            else:
                ax[rows - 1].set_xlabel(x_labels[i])

    fig.show()

