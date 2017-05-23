  # demo 2 : shared colorbar

    grid2 = ImageGrid(F, 212,
                      nrows_ncols = (1, 3),
                      direction="row",
                      axes_pad = 0.05,
                      add_all=True,
                      label_mode = "1",
                      share_all = True,
                      cbar_location="right",
                      cbar_mode="single",
                      cbar_size="10%",
                      cbar_pad=0.05,
                      )

    grid2[0].set_xlabel("X")
    grid2[0].set_ylabel("Y")

    vmax, vmin = np.max(ZS), np.min(ZS)
    import matplotlib.colors
    norm = matplotlib.colors.Normalize(vmax=vmax, vmin=vmin)

    for ax, z in zip(grid2, ZS):
        im = ax.imshow(z, norm=norm,
                       origin="lower", extent=extent,
                       interpolation="nearest")

    # With cbar_mode="single", cax attribute of all axes are identical.
    ax.cax.colorbar(im)
    ax.cax.toggle_label(True)

    for ax, im_title in zip(grid2, ["(a)", "(b)", "(c)"]):
        t = add_inner_title(ax, im_title, loc=2)
        t.patch.set_ec("none")
        t.patch.set_alpha(0.5)

    grid2[0].set_xticks([-2, 0])
    grid2[0].set_yticks([-2, 0, 2])

    plt.draw()
    plt.show()
