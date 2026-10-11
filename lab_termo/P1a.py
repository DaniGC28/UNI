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
        plt.savefig(f"GraficsP1b/{name}.png", dpi=300)
    else:
         return fig, ax


import numpy as np


def punt4_1():
    # Dist. temperatures ferro

    x = np.array([0, 10.2, 20.1, 30, 39.9, 50.2, 60])
    inc_x = 0.5 + + np.zeros(len(x))

    T_ambient = 27.3
    T = np.array([131.7, 79.3, 54.2, 41, 34.2, 31.2, 29.4]) - T_ambient
    inc_T = 0.1 + np.zeros(len(T))

    fig, ax = graph(x, T, xerr=inc_x, yerr=inc_T, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"Temperatura $\theta$ (K)", title="Distribució de temperatures en el ferro")


    lnT = np.log(T)
    inc_lnT = inc_T/T

    # Regressió ODR

    xf = x
    yf = lnT

    def recta(B, x):
        return B[0]*x + B[1]

    model = Model(recta)
    dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
        "Ajust:",
        rf"$p = {coma_math(-pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
        rf"$\ln\theta_0 = {coma_math(ordenada, ".3f")} \pm {coma_math(inc_ordenada, ".3f")}$",
        # rf"$R^2 = {coma_math(r2, ".4f")}$",
    ])

    print("____Ferro____")
    print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
    print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


    eix_x = np.linspace(xf[0]-2, xf[-1]+2, 1000)
    plt.plot(eix_x, np.e**(ordenada) * np.e**(pendent*eix_x), linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

    plt.legend(loc="best")
    plt.savefig("GraficsP1a/g1.png", dpi=300)


    # Dist. temperatures alumini

    x = np.array([0, 9.9, 19.8, 29.7, 39.9, 49.9, 59.8])
    inc_x = 0.5 + + np.zeros(len(x))

    T_ambient = 27.3
    T = np.array([116.1, 92.4, 76.1, 63.6, 54.1, 47.3, 42.3]) - T_ambient
    inc_T = 0.1 + np.zeros(len(T))

    fig, ax = graph(x, T, xerr=inc_x, yerr=inc_T, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"Temperatura $\theta$ (K)", title="Distribució de temperatures en l'alumini")


    lnT = np.log(T)
    inc_lnT = inc_T/T

    # Regressió ODR

    xf = x
    yf = lnT

    def recta(B, x):
        return B[0]*x + B[1]

    model = Model(recta)
    dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
        "Ajust:",
        rf"$p = {coma_math(-pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
        rf"$\ln\theta_0 = {coma_math(ordenada, ".4f")} \pm {coma_math(inc_ordenada, ".4f")}$",
        # rf"$R^2 = {coma_math(r2, ".4f")}$",
    ])

    print("____Alumini____")
    print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
    print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


    eix_x = np.linspace(x[0]-2, x[-1]+2, 1000)
    plt.plot(eix_x, np.e**(ordenada) * np.e**(pendent*eix_x), linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

    plt.legend(loc="best")
    plt.savefig("GraficsP1a/g2.png", dpi=300)


    # Dist. temperatures llautó

    x = np.array([0, 10, 19.9, 29.8, 39.8, 49.8, 59.7])
    inc_x = 0.5 + + np.zeros(len(x))

    T_ambient = 27.3
    T = np.array([126.7, 95.8, 73, 56.9, 47.2, 40.3, 35.3]) - T_ambient
    inc_T = 0.1 + np.zeros(len(T))

    fig, ax = graph(x, T, xerr=inc_x, yerr=inc_T, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"Temperatura $\theta$ (K)", title="Distribució de temperatures en el llautó")


    lnT = np.log(T)
    inc_lnT = inc_T/T

    # Regressió ODR

    xf = x
    yf = lnT

    def recta(B, x):
        return B[0]*x + B[1]

    model = Model(recta)
    dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
        "Ajust:",
        rf"$p = {coma_math(-pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
        rf"$\ln\theta_0 = {coma_math(ordenada, ".3f")} \pm {coma_math(inc_ordenada, ".3f")}$",
        # rf"$R^2 = {coma_math(r2, ".4f")}$",
    ])

    print("____Llautó____")
    print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
    print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


    eix_x = np.linspace(x[0]-2, x[-1]+2, 1000)
    plt.plot(eix_x, np.e**(ordenada) * np.e**(pendent*eix_x), linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

    plt.legend(loc="best")
    plt.savefig("GraficsP1a/g3.png", dpi=300)

punt4_1()

# Dist. temperatures ferro

x = np.array([0, 10.2, 20.1, 30, 39.9, 50.2, 60])
inc_x = 0.5 + + np.zeros(len(x))

T_ambient = 27.3
T = np.array([131.7, 79.3, 54.2, 41, 34.2, 31.2, 29.4]) - T_ambient
inc_T = 0.1 + np.zeros(len(T))
lnT = np.log(T)
inc_lnT = inc_T/T

fig, ax = graph(x, lnT, xerr=inc_x, yerr=inc_lnT, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"$\ln\theta$", title="Distribució de temperatures en el ferro")

# Regressió ODR

xf = x
yf = lnT

def recta(B, x):
    return B[0]*x + B[1]

model = Model(recta)
dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
    rf"$Pendent = {coma_math(pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
    rf"$Ordenada = {coma_math(ordenada, ".3f")} \pm {coma_math(inc_ordenada, ".3f")}$",
    rf"$R^2 = {coma_math(r2, ".4f")}$",
])

print("____Ferro____")
print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


eix_x = np.linspace(xf[0]-2, xf[-1]+2, 1000)
plt.plot(eix_x, pendent*eix_x + ordenada, linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

plt.legend(loc="best")
plt.savefig("GraficsP1a/g1b.png", dpi=300)


# Dist. temperatures alumini

x = np.array([0, 9.9, 19.8, 29.7, 39.9, 49.9, 59.8])
inc_x = 0.5 + + np.zeros(len(x))

T_ambient = 27.3
T = np.array([116.1, 92.4, 76.1, 63.6, 54.1, 47.3, 42.3]) - T_ambient
inc_T = 0.1 + np.zeros(len(T))
lnT = np.log(T)
inc_lnT = inc_T/T

fig, ax = graph(x, lnT, xerr=inc_x, yerr=inc_lnT, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"$\ln\theta$", title="Distribució de temperatures en el ferro")

# Regressió ODR

xf = x
yf = lnT

def recta(B, x):
    return B[0]*x + B[1]

model = Model(recta)
dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
    rf"$Pendent = {coma_math(pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
    rf"$Ordenada = {coma_math(ordenada, ".3f")} \pm {coma_math(inc_ordenada, ".3f")}$",
    rf"$R^2 = {coma_math(r2, ".4f")}$",
])

print("____Alumini____")
print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


eix_x = np.linspace(xf[0]-2, xf[-1]+2, 1000)
plt.plot(eix_x, pendent*eix_x + ordenada, linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

plt.legend(loc="best")
plt.savefig("GraficsP1a/g2b.png", dpi=300)


# Dist. temperatures llautó

x = np.array([0, 10, 19.9, 29.8, 39.8, 49.8, 59.7])
inc_x = 0.5 + + np.zeros(len(x))

T_ambient = 27.3
T = np.array([126.7, 95.8, 73, 56.9, 47.2, 40.3, 35.3]) - T_ambient
inc_T = 0.1 + np.zeros(len(T))

lnT = np.log(T)
inc_lnT = inc_T/T

fig, ax = graph(x, lnT, xerr=inc_x, yerr=inc_lnT, autoSave=False, xname="Distància del extrem calent (cm)", yname=r"$\ln\theta$", title="Distribució de temperatures en el ferro")

# Regressió ODR

xf = x
yf = lnT

def recta(B, x):
    return B[0]*x + B[1]

model = Model(recta)
dades = RealData(xf, yf, sx=inc_x, sy=inc_lnT)

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
    rf"$Pendent = {coma_math(pendent, ".5f")} \pm {coma_math(inc_pendent, ".5f")}$",
    rf"$Ordenada = {coma_math(ordenada, ".3f")} \pm {coma_math(inc_ordenada, ".3f")}$",
    rf"$R^2 = {coma_math(r2, ".4f")}$",
])

print("____Llautò____")
print(f"Pendent = {pendent:.5f} ± {inc_pendent:.5f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")


eix_x = np.linspace(xf[0]-2, xf[-1]+2, 1000)
plt.plot(eix_x, pendent*eix_x + ordenada, linestyle="--", color="crimson", alpha=0.5, label=etiqueta)

plt.legend(loc="best")
plt.savefig("GraficsP1a/g3b.png", dpi=300)