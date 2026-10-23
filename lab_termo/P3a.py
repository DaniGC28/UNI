import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FuncFormatter
from scipy.odr import ODR, Model, RealData

def coma_math(x, fmt=".3f"):
    # per usar dins de $...$: la coma entre claus evita l'espai
    return format(x, fmt).replace(".", "{,}")

def graph(x, y, xerr=[], yerr=[], name="prova", xname="eix X", yname="eix Y", title="Gràfica", autoSave=True, line=False, ax=None, color="red", label=None, size=3.5):

    if len(xerr) == 0:
        xerr = np.zeros(len(x))
    if len(yerr) == 0:
            yerr = np.zeros(len(x))

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    ax.errorbar(
        x, y,
        xerr=xerr,
        yerr=yerr,
        fmt="o",
        color=color,
        ecolor="grey",
        markersize = size,
        label = label
    )

    if line:
        ax.plot(
            np.sort(x), np.sort(y),
            linestyle="--",
            color="red",
            alpha=0.2
        )

    # Eixos
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    # ax.set_title(title)


    # Grid principal i secundària
    ax.grid(True, which="major", linestyle="-", alpha=0.3)
    ax.grid(True, which="minor", linestyle=":", alpha=0.2)

    # Subticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    fmt = FuncFormatter(lambda x, _: f"{x:g}".replace('.', ','))
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)

    # Eixos als quatre costats
    ax.tick_params(
        axis="both",
        which="both",
        direction="in",
        top=True,
        right=True
    )

    plt.tight_layout()
    # plt.axis("equal")
    if autoSave:
        plt.savefig(f"GraficsP1b/{name}.png", dpi=300)
    else:
         return fig, ax


import numpy as np


### Questió 4 ###

P1_1 = np.array([189.7, 189.4, 189.9, 190.2, 190.3, 192.1, 191.1, 190.7, 189.9, 192])
T1_1 = np.array([26.72, 26.76, 26.8, 26.83, 26.87, 26.98, 27.02, 27.05, 27.11, 27.14])
P2_1 = np.array([11.4, 21.9, 31.5, 41, 50.9, 63.1, 69.9, 80.2, 90.2, 101.2])
T2_1 = np.array([24.5, 24.75, 24.84, 25.02, 25.17, 25.53, 25.81, 25.98, 26.28, 26.49])

inc_T1 = np.zeros(len(T1_1))+0.01
inc_T2 = np.zeros(len(T2_1))+0.05
inc_P = np.zeros(len(P1_1))+0.1

part1 = {"P1": P1_1, "P2": P2_1, "T1": T1_1, "T2": T2_1, "inc_T1": inc_T1, "inc_T2": inc_T2, "inc_P": inc_P}

P1_2 = np.array([191.9, 181.8, 170.3, 161.8, 151.4, 140.9, 128.7, 120.2, 110.3])
T1_2 = np.array([27.2, 27.22, 27.24, 27.28, 27.33, 27.35, 27.38, 27.43, 27.45])
P2_2 = np.array([101.3, 101.4, 101.2, 101.4, 101.2, 101.3, 101.2, 101.4, 101.1])
T2_2 = np.array([26.63, 26.75, 26.92, 27.09, 27.31, 27.51, 27.62, 27.73, 27.84])

part2 = {"P1": P1_2, "P2": P2_2, "T1": T1_2, "T2": T2_2, "inc_T1": inc_T1[:-1], "inc_T2": inc_T2[:-1], "inc_P": inc_P[:-1]}

import csv
from pathlib import Path


output_dir = Path("lab_termo/GraficsP3a")
output_dir.mkdir(parents=True, exist_ok=True)

for part_name, data in (("Part1", part1), ("Part2", part2)):
    table_path = output_dir / f"Q4-{part_name}.csv"
    with table_path.open("w", newline="", encoding="utf-8") as table_file:
        writer = csv.writer(table_file, delimiter=";")
        writer.writerow([
            "Mesura",
            "P1 (kPa)", "Incertesa P1 (kPa)",
            "T1 (°C)", "Incertesa T1 (°C)",
            "P2 (kPa)", "Incertesa P2 (kPa)",
            "T2 (°C)", "Incertesa T2 (°C)",
        ])
        for i in range(len(data["P1"])):
            values = (
                data["P1"][i], data["inc_P"][i],
                data["T1"][i], data["inc_T1"][i],
                data["P2"][i], data["inc_P"][i],
                data["T2"][i], data["inc_T2"][i],
            )
            writer.writerow(
                [i + 1] + [f"{value:.2f}".replace(".", ",") for value in values]
            )

    print(f"\n{part_name}: estats d'entrada i sortida")
    print("Mesura |  P1 (kPa) | T1 (°C) |  P2 (kPa) | T2 (°C)")
    for i in range(len(data["P1"])):
        print(
            f"{i + 1:>6} | {data['P1'][i]:>9.2f} | {data['T1'][i]:>7.2f} | "
            f"{data['P2'][i]:>9.2f} | {data['T2'][i]:>7.2f}"
        )

    fig, ax = graph(
        data["P1"], data["T1"],
        xerr=data["inc_P"], yerr=data["inc_T1"],
        autoSave=False, color="red", label="Entrada (P1, T1)",
    )
    graph(
        data["P2"], data["T2"],
        xerr=data["inc_P"], yerr=data["inc_T2"],
        autoSave=False, color="blue", label="Sortida (P2, T2)",
        ax=ax, xname="Pressió (kPa)", yname="Temperatura (°C)",
    )

    # Cada fila és una parella d'estats entrada-sortida del mateix procés.
    for i in range(len(data["P1"])):
        ax.plot(
            [data["P1"][i], data["P2"][i]],
            [data["T1"][i], data["T2"][i]],
            linestyle="--",
            color="grey",
            alpha=0.55,
            label="Parell isentàlpic (mateixa mesura)" if i == 0 else None,
        )

    ax.legend(loc="best")
    fig.savefig(output_dir / f"Q4-{part_name}.png", dpi=300)

### Questió 5 ###

part1["delta_P"] = part1["P2"] - part1["P1"]
part1["delta_T"] = part1["T2"] - part1["T1"]
part2["delta_P"] = part2["P2"] - part2["P1"]
part2["delta_T"] = part2["T2"] - part2["T1"]
part1["inc_delta_P"] = np.sqrt(2) * part1["inc_P"]
part1["inc_delta_T"] = np.sqrt(2) * part1["inc_T1"]
part2["inc_delta_P"] = np.sqrt(2) * part2["inc_P"]
part2["inc_delta_T"] = np.sqrt(2) * part2["inc_T1"]

fig, ax = graph(part1["delta_P"], part1["delta_T"], xerr=part1["inc_delta_P"], yerr=part1["inc_delta_T"],
                autoSave=False, color="red")
fig, ax = graph(part2["delta_P"], part2["delta_T"], xerr=part2["inc_delta_P"], yerr=part2["inc_delta_T"],
      autoSave=False, color="blue", ax=ax, xname="ΔP (kPa)", yname="ΔT (°C)")


#--------------------#
x = part1["delta_P"]
y = part1["delta_T"]

coef, cov = np.polyfit(x, y, 1, cov=True)
slope, intercept = coef[0], coef[1]
inc_slope, inc_intercept = np.sqrt(cov[0][0]), np.sqrt(cov[1][1])
r_squared = 1 - np.sum((y - (slope * x + intercept)) ** 2) / np.sum((y - np.mean(y)) ** 2)

plt.plot(
    x, slope * x + intercept,
    color="red", alpha=0.5,
    label=(
        "Part 1:\n"
        fr"$\mu = {coma_math(slope, '.5f')}\pm {coma_math(inc_slope, '.5f')}$" "\n"
        fr"ordenada = ${coma_math(intercept, '.2f')}\pm {coma_math(inc_intercept, '.2f')}$" "\n"
        fr"$R^2 = {coma_math(r_squared, '.4f')}$"
    )
)
#--------------------#
#--------------------#
x = part2["delta_P"]
y = part2["delta_T"]

coef, cov = np.polyfit(x, y, 1, cov=True)
slope, intercept = coef[0], coef[1]
inc_slope, inc_intercept = np.sqrt(cov[0][0]), np.sqrt(cov[1][1])
r_squared = 1 - np.sum((y - (slope * x + intercept)) ** 2) / np.sum((y - np.mean(y)) ** 2)

plt.plot(
    x, slope * x + intercept,
    color="blue", alpha=0.5,
    label = (
        "Part 2:\n"
        fr"$\mu = {coma_math(slope, '.5f')}\pm {coma_math(inc_slope, '.5f')}$" "\n"
        fr"ordenada = ${coma_math(intercept, '.3f')}\pm {coma_math(inc_intercept, '.3f')}$" "\n"
        fr"$R^2 = {coma_math(r_squared, '.4f')}$"
    )
)
#--------------------#




plt.legend(loc="best")
plt.savefig(output_dir / "Q5.png", dpi=300)