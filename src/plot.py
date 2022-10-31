import subprocess
import pandas as pd
from matplotlib import pyplot as plt
import os
from matplotlib import patches
from matplotlib import colors as mcolors
import numpy as np
import h5py
import json

def plotloss(param, domain = "space"):
    output = subprocess.Popen(["ls", f"logs/{domain}_domain_{param['model']}"], stdout=subprocess.PIPE).communicate()[0]
    lastLogFolder = f"logs/{domain}_domain_{param['model']}/" + output.decode().split("\n")[-2]
    metrics = pd.read_csv(f"{lastLogFolder}/metrics.csv")
    metrics = metrics.set_index("epoch")
    fig, axs = plt.subplots()
    print(metrics["loss"])
    # metrics["val_loss"].plot(ax=axs)
    metrics["loss"].plot(ax=axs)
    axs.set_ylabel("loss")
    axs.set_xlabel("epoch")
    axs.set_title(f"{domain.title()} domain U-Net filter loss over training")
    figsFolder = os.environ['FIGSDIR']
    plt.savefig(figsFolder + f"space_domain_{param['model']}-loss.png", dpi=300)
    plt.show()

def plotvel(param, d, vel):
    fig, ax = plt.subplots(figsize = (8, 5))
    n = vel.shape
    extent = [0, (n[1]-1)*d[0], (n[0]-1)*d[1], 0] # d is inverted since it was defined in julia
    ax.imshow(vel, cmap="jet", extent = extent, aspect = "auto")
    ax.set_xlabel("Offset (meters)")
    ax.set_ylabel("Depth (meters)")
    fig.tight_layout(pad=1.5)
    figsFolder = os.environ['FIGSDIR']
    plt.savefig(figsFolder + f"vel_{param['model']}.png", dpi=300)
    plt.show()


def plotimage(param, d, image, name="rtm", domain="space", xlim=None, ylim=None, xline=None, cmap="gray"):
    fig, ax = plt.subplots(figsize = (8, 5))
    n = image.shape
    extent = [0, (n[1]-1)*d[0], (n[0]-1)*d[1], 0] # d is inverted since it was defined in julia
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

    if type(xlim) == list and type(xlim[0]) == list and type(ylim) == list and type(ylim[0]) == list:
        for xlim_i, ylim_i, i in zip(xlim, ylim, range(len(xlim))):
            fig, ax = plt.subplots(figsize = (8, 5))
            ax.imshow(image, cmap=cmap, extent = extent, aspect = "auto")
            ax.set_xlabel("Offset (meters)")
            ax.set_ylabel("Depth (meters)")
            fig.tight_layout(pad=1.5)
            figsFolder = os.environ['FIGSDIR']
            plt.xlim(*xlim_i)
            plt.ylim(*ylim_i)
            plt.savefig(figsFolder + f"{domain}_domain_{param['model']}-{name}-window{i}.png", dpi=300)

        return

def plottrace(param, d, images, labels, name="trace"):
    fig, ax = plt.subplots(figsize = (8, 5))

    n = images[0].shape
    for image, label in zip(images, labels):
        xindex = int(np.around(param['xline']/d[0]))
        depth = np.arange(0, n[0]*d[1], d[1])
        ax.plot(image[:, xindex], depth)
        ax.xaxis.tick_top()
    ax.legend(labels)
    figsFolder = os.environ['FIGSDIR']
    plt.savefig(figsFolder + f"{name}.png", dpi=300)
    plt.show()

def main(param):
    dataFolder = os.environ["DATADIR"]
    rtm_file = h5py.File(dataFolder + f"rtm_{param['model']}.h5", "r")
    rtm_dset = rtm_file["m"]
    filtered_space_file = h5py.File(dataFolder + f"filtered_space_domain_image-{param['model']}.h5", "r")
    filtered_space_dset = filtered_space_file["m"]

    filtered_curvelet_file = h5py.File(dataFolder + f"filtered_curvelet_domain_image-{param['model']}.h5", "r")
    filtered_curvelet_dset = filtered_curvelet_file["m"]

    images = [rtm_dset, filtered_space_dset, filtered_curvelet_dset]
    labels = ["RTM", "Space Dom. U-Net", "Curvelet Dom. U-Net"]

    plottrace(
        param,
        rtm_file['d'],
        images,
        labels,
        name="trace"
    )

    vel_file = h5py.File(dataFolder + f"vel_{param['model']}.h5", "r")
    plotvel(param, vel_file["d"], vel_file["m0"])


if __name__ == "__main__":
    with open("dataconf/spaceDomain/marmousi.json", "r") as arq:
        marmousi = json.load(arq)
    main(marmousi)

    with open("dataconf/spaceDomain/sigsbee.json", "r") as arq:
        sigsbee = json.load(arq)
    main(sigsbee)
