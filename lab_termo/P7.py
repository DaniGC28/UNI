import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FuncFormatter
from scipy.odr import ODR, Model, RealData

def coma_math(x, fmt=".3f"):
    # per usar dins de $...$: la coma entre claus evita l'espai
    return format(x, fmt).replace(".", "{,}")

def graph(x, y, xerr=[], yerr=[], name="prova", xname="eix X", yname="eix Y", title="Gràfica", autoSave=True, line=False):

    if len(xerr) == 0:
        xerr = np.zeros(len(x))
    if len(yerr) == 0:
            yerr = np.zeros(len(x))

    fig, ax = plt.subplots()

    ax.errorbar(
        x, y,
        xerr=xerr,
        yerr=yerr,
        fmt="o",
        color="red",
        ecolor="grey",
        markersize = 3.5
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
        plt.savefig(f"GraficsP7/{name}.png", dpi=300)
    else:
         return fig, ax


import numpy as np


T = np.array([90.3, 140.4, 118.5, 104, 100.3, 94.6])
V = np.array([2.93, 4.750, 3.98, 3.4, 3.29, 3.12]) * 10**(3)
inc_T = np.zeros(len(V)) + 1
inc_V = np.zeros(len(V)) + 30

ordre = np.argsort(T)

T = T[ordre]
V = V[ordre]

fig, ax = graph(T, V, xerr=inc_T, yerr=inc_V, name="Q2", yname=r"Força electromotriu ($\mu$V)", xname="Temperatura (ºC)", autoSave=False)

# Regressió ODR

xf = T
yf = V

def recta(B, x):
    return B[0]*x + B[1]

model = Model(recta)
dades = RealData(xf, yf, sx=inc_T, sy=inc_V)

# Estimació inicial amb regressió lineal ordinària
coef_inicial = np.polyfit(xf, yf, 1)

regressio = ODR(dades, model, beta0=coef_inicial)
resultat = regressio.run()

pendent, ordenada = resultat.beta

# Incerteses dels paràmetres segons l'ODR
inc_pendent, inc_ordenada = resultat.sd_beta

y_ajust = pendent * xf + ordenada
ss_res = np.sum((yf - y_ajust) ** 2)
ss_tot = np.sum((yf - np.mean(yf)) ** 2)
r2 = 1 - ss_res / ss_tot

etiqueta = "\n".join([
    "Resultats regressió lineal:",
    rf"Pendent $= {coma_math(pendent, ".2f")} \pm {coma_math(inc_pendent, ".2f")}$",
    # rf"Ordenada $= {coma_math(ordenada, ".0f")} \pm {coma_math(inc_ordenada, ".0f")}$",
    rf"$R^2 = {coma_math(r2, ".4f")}$",
])

print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


eix_x = np.linspace(xf[0]-2, xf[-1]+2, 1000)
plt.plot(eix_x, pendent*eix_x + ordenada, linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

plt.legend(loc="best")
plt.savefig("GraficsP7/Q2.png", dpi=300)