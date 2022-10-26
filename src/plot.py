import subprocess
import pandas as pd
from matplotlib import pyplot as plt
import os

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

def plotimage(param, d, image, name="rtm", domain="space"):
    fig, ax = plt.subplots(figsize = (8, 5))
    n = image.shape
    extent = [0, (n[0]-1)*d[0], (n[1]-1)*d[1], 0 ]
    ax.imshow(image, cmap="gray", extent = extent, aspect = "auto")
    ax.set_xlabel("Offset (meters)")
    ax.set_ylabel("Depth (meters)")
    fig.tight_layout(pad=1.5)
    figsFolder = os.environ['FIGSDIR']
    plt.savefig(figsFolder + f"{domain}_domain_{param['model']}-{name}.png", dpi=300)
    plt.show()
