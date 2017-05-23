import numpy as np
import matplotlib.pyplot as plt


def NotAvailable(axx):
    axx.set_xticks([])
    #axx.set_yticks([])
    #axx.xaxis.set_visible(False)
    #axx.yaxis.set_visible(False)
    axx.plot(range(10))
    axx.axis('off')
    axx.plot(range(9,-1,-1))
    t='NotAvailable'
    cmap = plt.cm.bwr
    axx.text(5, 5, t, fontsize=8, style='oblique', ha='center',\
                    va='center', wrap=True)

    plt.colorbar(cmap=cmap,vmin=-20,vmax=20,orientation='horizontal',shrink=0.9) # draw colorbar

#=================================================== 
fig, axes = plt.subplots(nrows=11, ncols=4, figsize=(4, 12))
for i in range(11):
    for j in range(4):
        plt.sca(axes[i,j])
        axx=axes[i,j]
        NotAvailable(axx)

#fig.colorbar(im, ax=axes.ravel().tolist())

plt.show()
