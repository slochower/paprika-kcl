import numpy as np
import matplotlib.pyplot as plt


def plot_pmf(
    attach,
    pull,
    release=None,
    release_to_std=None,
    attach_sem=None,
    pull_sem=None,
    release_SEM=None,
    attach_lambda=None,
    pull_initial=None,
    pull_final=None,
    release_lambda=None,
    title=None,
):

    fig, ax1 = plt.subplots(1, figsize=(6 * 1.2, 6))

    attach = np.asarray(attach)
    pull = np.asarray(pull)
    if release:
        release = np.asarray(release)

    attach_range = np.arange(len(attach))
    pull_range = np.arange(attach_range[-1], attach_range[-1] + len(pull))

    if release:
        release_range = np.arange(pull_range[-1], pull_range[-1] + len(release))
        analytic_range = [release_range[-1], release_range[-1]]
    else:
        analytic_range = [pull_range[-1], pull_range[-1]]

    if release:
        final_fe = attach[-1] + pull[-1] + release[-1] + release_to_std
        final_sem = np.sqrt(
            attach_sem[-1] ** 2 + pull_sem[-1] ** 2 + release_SEM[-1] ** 2
        )
    else:
        final_fe = attach[-1] + pull[-1] + release_to_std

        final_sem = np.sqrt(attach_sem[-1] ** 2 + pull_sem[-1] ** 2)

    ax1.errorbar(
        attach_range,
        attach,
        yerr=attach_sem,
        marker="o",
        ms=8,
        markeredgecolor="k",
        markeredgewidth=1,
        lw=3,
        label="Attach",
    )
    ax1.errorbar(
        pull_range,
        attach[-1] + pull,
        yerr=pull_sem,
        marker="o",
        ms=8,
        markeredgecolor="k",
        markeredgewidth=1,
        lw=3,
        label="Pull",
    )

    if release:
        ax1.errorbar(
            release_range,
            attach[-1] + pull[-1] + -1 * release,
            yerr=release_SEM,
            marker="o",
            ms=8,
            markeredgecolor="k",
            markeredgewidth=1,
            lw=3,
            label="Release",
        )
        ax1.errorbar(
            analytic_range,
            [attach[-1] + pull[-1] + -1 * release[-1], final_fe],
            yerr=[release_SEM[-1], release_SEM[-1]],
            label="Analytic",
        )

        ax1.scatter(
            release_range[-1], final_fe, c="w", edgecolor="k", lw=2, s=80, zorder=10
        )
        ax1.annotate(
            r"${0:2.2f} \pm {1:2.2f}$".format(final_fe, final_sem),
            xy=(release_range[-1] + 2, final_fe),
            xycoords="data",
        )

        ax1.set_xticks(
            [
                0,
                len(attach) - 1,
                len(attach) - 1,
                len(attach) - 1 + len(pull) - 1,
                len(attach) - 1 + len(pull) - 1,
                len(attach) - 1 + len(pull) - 1 + len(release) - 1,
            ]
        )

        ax1.set_xticklabels([0, 1, pull_initial, pull_final, 0, 1])
        va = [0, 0, -0.05, -0.05, 0, 0]
        for t, y in zip(ax1.get_xticklabels(), va):
            t.set_y(y)

    else:
        ax1.errorbar(
            analytic_range,
            [attach[-1] + pull[-1], final_fe],
            yerr=[pull_sem[-1], pull_sem[-1]],
            label="Analytic",
        )

        ax1.scatter(
            pull_range[-1], final_fe, c="w", edgecolor="k", lw=2, s=80, zorder=10
        )

        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

        #         ax1.annotate(r'${0:2.2f} \pm {1:2.2f}$'.format(final_fe, final_sem),
        #                      xy=(pull_range[-1] - 10, final_fe - 0.5), xycoords='data',
        #                     fontsize=14, bbox=bbox_props)

        ax1.set_xticks(
            [0, len(attach) - 1, len(attach) - 1, len(attach) - 1 + len(pull) - 1]
        )

        ax1.set_xticklabels([0, 1, pull_initial, pull_final])
        va = [0, 0, -0.05, -0.05]
        for t, y in zip(ax1.get_xticklabels(), va):
            t.set_y(y)

    ax1.legend(frameon=True, framealpha=1.0, edgecolor="k")
    ax1.grid(True, which="both")
    ax1.set_xlabel(r"$\lambda$ or distance")
    ax1.set_ylabel("Potential of mean force (kcal/mol)")
    ax1.set_title(
        r"$\Delta G = {0:2.2f} \pm {1:2.2f}$ kcal/mol".format(final_fe, final_sem),
        loc="left",
    )
