import subprocess
import pandas as pd
from matplotlib import pyplot as plt
import os
from matplotlib import patches
from matplotlib import colors as mcolors

def plotloss(param, domain = "space"):
    output = subprocess.Popen(["ls", f"logs/{domain}_domain_{param['model']}"], stdout=subprocess.PIPE).communicate()[0]
    lastLogFolder = f"logs/{domain}_domain_{param['model']}/" + output.decode().split("\n")[-2]
    metrics = pd.read_csv(f"{lastLogFolder}/metrics.csv")
    metrics = metrics.set_index("epoch")
    fig, axs = plt.subplots()
    metrics["loss"].plot(ax=axs)
    axs.set_ylabel("loss")
    axs.set_xlabel("epoch")
    axs.set_title(f"{domain.title()} domain U-Net filter loss over training")
    figsFolder = os.environ['FIGSDIR']
    plt.savefig(figsFolder + f"space_domain_{param['model']}-loss.png", dpi=300)
    plt.show()

def plotimage(param, d, image, name="rtm", domain="space", xlim=None, ylim=None, xline=None, cmap="gray"):
    fig, ax = plt.subplots(figsize = (8, 5))
    n = image.shape
    extent = [0, (n[0]-1)*d[0], (n[1]-1)*d[1], 0 ]
    ax.imshow(image, cmap=cmap, extent = extent, aspect = "auto")
    ax.set_xlabel("Offset (meters)")
    ax.set_ylabel("Depth (meters)")
    fig.tight_layout(pad=1.5)
    figsFolder = os.environ['FIGSDIR']
    if type(xlim) == list and type(xlim[0]) == list and type(ylim) == list and type(ylim[0]) == list:
        assert len(xlim) == len(ylim)
        colors = list(mcolors.BASE_COLORS)
        for xlim_i, ylim_i, i in zip(xlim, ylim, range(len(xlim))):
            height = ylim_i[1] - ylim_i[0]
            width  = xlim_i[1] - xlim_i[0]
            rect = patches.Rectangle((xlim_i[0], ylim_i[0]), width, height, edgecolor=colors[i], linewidth=1.3, linestyle=':', facecolor='none')
            ax.add_patch(rect)
    if type(xline) == float:
        ax.axvline(x=xline, color='black', linewidth=0.6, linestyle=':')

    plt.savefig(figsFolder + f"{domain}_domain_{param['model']}-{name}.png", dpi=300)
    plt.show()

    if type(xlim) == list and type(xlim[0]) == list and type(ylim) == list and type(ylim[0]) == list:
        for xlim_i, ylim_i, i in zip(xlim, ylim, range(len(xlim))):
            fig, ax = plt.subplots(figsize = (8, 5))
            n = image.shape
            extent = [0, (n[0]-1)*d[0], (n[1]-1)*d[1], 0 ]
            ax.imshow(image, cmap=cmap, extent = extent, aspect = "auto")
            ax.set_xlabel("Offset (meters)")
            ax.set_ylabel("Depth (meters)")
            fig.tight_layout(pad=1.5)
            figsFolder = os.environ['FIGSDIR']
            plt.xlim(*xlim_i)
            plt.ylim(*ylim_i)
            plt.savefig(figsFolder + f"{domain}_domain_{param['model']}-{name}-window{i}.png", dpi=300)

        return
