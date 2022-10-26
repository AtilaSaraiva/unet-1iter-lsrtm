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
