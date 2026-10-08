

def coma(x, fmt=".3g"):
    return format(x, fmt).replace(".", ",")

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import FuncFormatter


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
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def graphReg(x, y, xerr=[], yerr=[], name="prova", xname="eix X", yname="eix Y",
             title="Gràfica", n=None):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if len(xerr) == 0:
        xerr = np.zeros(len(x))
    if len(yerr) == 0:
        yerr = np.zeros(len(x))
    xerr = np.asarray(xerr, dtype=float)
    yerr = np.asarray(yerr, dtype=float)

    fig, ax = plt.subplots()

    ax.errorbar(
        x, y,
        xerr=xerr,
        yerr=yerr,
        fmt="o",
        color="red",
        ecolor="grey",
        markersize=3.5,
        label="Dades"
    )

    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]
    xerr = xerr[idx]
    yerr = yerr[idx]

    # Punts usats en l'ajust
    xf = x[:n] if n is not None else x
    yf = y[:n] if n is not None else y

    coef, cov = np.polyfit(xf, yf, 1, cov=True)
    pendent, ordenada = coef
    err_pendent, err_ordenada = np.sqrt(np.diag(cov))

    # Coeficient de determinació R²
    y_ajust = pendent * xf + ordenada
    ss_res = np.sum((yf - y_ajust) ** 2)
    ss_tot = np.sum((yf - np.mean(yf)) ** 2)
    r2 = 1 - ss_res / ss_tot

    eps = 0.2
    etiqueta = (
        f"Regressió lineal:\n"
        f"$Pendent = {coma(pendent, '.3f')} \\pm {coma(err_pendent, '.3f')}$\n"
        f"$Ordenada = {coma(ordenada, '.3f')} \\pm {coma(err_ordenada, '.3f')}$\n"
        f"$R^2 = {coma(r2, ".4f")}$"
    )
    ax.plot(
        [x[0]-eps, x[-1]+eps],
        [pendent*(x[0]-eps)+ordenada, pendent*(x[-1]+eps)+ordenada],
        linestyle="--",
        color="crimson",
        alpha=0.6,
        label=etiqueta
    )

    # Eixos
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    # ax.set_title(title)

    # Llegenda
    ax.legend(loc="best", fontsize=8, framealpha=0.9)

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
    plt.savefig(f"GraficsP1b/{name}.png", dpi=300)
    plt.show()

    return pendent, err_pendent, ordenada, err_ordenada, r2

import numpy as np


P = np.array([0.0798, 0.2412, 0.432, 0.6396, 0.861, 1.0926, 1.3356, 1.5888, 0.515, 1.272, 2.16, 3.192, 4.35, 5.64, 7.042, 8.568, 10.215, 11.95576, 13.65765, 15.7132, 17.615, 19.726, 22.0913, 24.37344, 26.39952, 28.71606, 31.4768, 33.5989, 36.14611, 39.121])

T = np.array([352.7822972, 437.679356, 526.7069832, 614.3250301, 698.550656, 780.5253316, 858.8500914, 934.1505688, 542.2441278, 822.2502998, 1060.148945, 1257.044816, 1428.039953, 1576.050262, 1709.958961, 1829.000868, 1936.044837, 2048.920561, 2141.289148, 2241.278107, 2323.517025, 2403.132707, 2492.781864, 2571.952714, 2641.476896, 2707.877056, 2788.067743, 2844.869901, 2911.316385, 2980.594648])

R = [111.9819549, 148.4537313, 186.7, 224.3407129, 260.5240418, 295.7403624, 329.3886792, 361.7377644, 193.3747573, 313.6654088, 415.8666667, 500.4531328, 573.9126437, 637.4978723, 695.0250497, 746.1654528, 792.1515419, 840.642953, 880.324498, 923.2797546, 958.6095941, 992.8124911, 1031.325769, 1065.337566, 1095.205155, 1123.730663, 1158.180583, 1182.582789, 1211.128199, 1240.890141]

Rad = np.array([3.545454545, 6.272727273, 12.04545455, 15.90909091, 20.90909091, 27.27272727, 34.54545455, 43.18181818, 13.40909091, 32.27272727, 65.90909091, 113.1818182, 182.7272727, 262.7272727, 354.5454545, 460.0, 573.6363636, 709.0909091, 829.0909091, 986.3636364, 1122.727273, 1286.363636, 1463.636364, 1636.363636, 1784.090909, 1954.545455, 2163.636364, 2309.090909, 2486.363636, 2706.818182])

inc_R = [0.5754131132, 0.4579595661, 0.4538619486, 0.4728894105, 0.4976148199, 0.5251729513, 0.551592236, 0.5768258384, 0.435731298, 0.5283895118, 0.6034799915, 0.6482740205, 0.677930628, 0.694559611, 0.7059004014, 0.7107390744, 0.7112344817, 0.7178752026, 0.7192593402, 0.7197679518, 0.7188764001, 0.7157721616, 0.7158088765, 0.7152375682, 0.7161385034, 0.7135304008, 0.7129260538, 0.7118661772, 0.7112037377, 0.7088973264]

inc_T = np.array([1.801130691, 3.112799561, 4.890380379, 6.695314141, 8.445199804, 10.15455587, 11.79039073, 13.36451393, 5.198845241, 11.02290661, 15.99731537, 20.11627822, 23.69419311, 26.79109847, 29.59329286, 32.08429333, 34.32420611, 36.68718736, 38.62064948, 40.71373271, 42.43527714, 44.1018295, 45.97884661, 47.63651737, 49.09238392, 50.48261235, 52.16183804, 53.35129068, 54.7427783, 56.19349683])

inc_P = np.array([0.000721576971, 0.0007400809772, 0.00104569793, 0.001343426797, 0.001639521404, 0.001934994487, 0.002231168531, 0.002527904627, 0.001155668335, 0.00213731444, 0.003128440276, 0.004128234893, 0.005131256923, 0.006137128723, 0.007143966186, 0.008152468587, 0.009162300402, 0.01020003032, 0.01114869959, 0.01223904941, 0.01319875043, 0.01421008873, 0.01532095129, 0.01635136075, 0.01724965678, 0.01822074086, 0.01936238721, 0.02021148247, 0.02121185773, 0.02233469639])

inc_Rad = np.array([0.2272727273, 0.2272727273, 0.2272727273, 0.2272727273, 0.2272727273, 0.2272727273, 0.2272727273, 0.2272727273, 0.9090909091, 0.9090909091, 0.9090909091, 0.9090909091, 0.9090909091, 0.9090909091, 2.272727273, 2.272727273, 2.272727273, 2.272727273, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545, 4.545454545])

T_ambient = 27.3+273.15

#Q7

fig, ax = graph(T, Rad, xerr=inc_T, yerr=inc_Rad, xname=r"Temperatura, $T(K)$", yname=r"Radiació emesa, $P(\mu W$)", title="Regressió de la radiació emesa en funció de la temperatura\n(Sense els 12 primers punts)", autoSave=False)


lnRad = np.log(Rad)

lnT   = np.log(T)


coef, cov = np.polyfit(lnT, lnRad, 1, cov=True)

pendent = coef[0]
ordenada = coef[1]

inc_pendent = np.sqrt(cov[0, 0])
inc_ordenada = np.sqrt(cov[1, 1])

# Coeficient de determinació R²
y_ajust = pendent * lnT + ordenada
ss_res = np.sum((lnRad - y_ajust) ** 2)
ss_tot = np.sum((lnRad - np.mean(lnRad)) ** 2)
r2 = 1 - ss_res / ss_tot

print("___Q7___")
print(f"Pendent = {pendent:.3f} ± {inc_pendent:.3f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")

def coma_math(x, fmt=".3f"):
    # per usar dins de $...$: la coma entre claus evita l'espai
    return format(x, fmt).replace(".", "{,}")

etiqueta = "\n".join([
    "Ajust:",
    rf"$\mathrm{{Exponent}} = {coma_math(pendent)} \pm {coma_math(inc_pendent)}$",
    rf"$\ln(e\sigma A) = {coma_math(ordenada)} \pm {coma_math(inc_ordenada)}$",
    rf"$R^2 = {coma_math(r2, '.4f')}$",
])

eix_x = np.linspace(int(T[0]-50), int(T[-1]+50), 1000)
plt.plot(eix_x, eix_x**pendent * np.e**ordenada, color="crimson", linestyle="--", alpha=0.5, label=etiqueta)

plt.legend(loc="best")

plt.savefig(f"GraficsP1b/Q7a.png", dpi=300)

fig, ax = graph(T[11:], Rad[11:], xerr=inc_T[11:], yerr=inc_Rad[11:], xname=r"Temperatura, $T(K)$", yname=r"Radiació emesa, $P(\mu W$)", title="Regressió de la radiació emesa en funció de la temperatura\n(Sense els 12 primers punts)", autoSave=False)


lnRad = np.log(Rad)

lnT   = np.log(T)


coef, cov = np.polyfit(lnT[11:], lnRad[11:], 1, cov=True)

pendent = coef[0]
ordenada = coef[1]

inc_pendent = np.sqrt(cov[0, 0])
inc_ordenada = np.sqrt(cov[1, 1])

# Coeficient de determinació R²
y_ajust = pendent * lnT[11:] + ordenada
ss_res = np.sum((lnRad[11:] - y_ajust) ** 2)
ss_tot = np.sum((lnRad[11:] - np.mean(lnRad[11:])) ** 2)
r2 = 1 - ss_res / ss_tot

print("___Q7___")
print(f"Pendent = {pendent:.3f} ± {inc_pendent:.3f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")

etiqueta = "\n".join([
    "Ajust:",
    rf"$\mathrm{{Exponent}} = {coma_math(pendent)} \pm {coma_math(inc_pendent)}$",
    rf"$\ln(e\sigma A) = {coma_math(ordenada)} \pm {coma_math(inc_ordenada)}$",
    rf"$R^2 = {coma_math(r2, '.4f')}$",
])

eix_x = np.linspace(int(T[11]-50), int(T[-1]+50), 1000)
plt.plot(eix_x, eix_x**pendent * np.e**ordenada, color="crimson", linestyle="--", alpha=0.5, label=etiqueta)

plt.legend(loc="best")

plt.savefig(f"GraficsP1b/Q7b.png", dpi=300)


graph(lnT, lnRad, line=True, name="Q8", xname=r"$\ln (T)$", yname=r"$\ln (P)$", title=r"$\ln (P)$ en funció de $\ln(T)$")

#Q 2-5

lnP = np.log(P)

lnT = np.log(T-T_ambient)

inc_lnP = inc_P/P

inc_lnT = (inc_T + 0.1)/(T-T_ambient)


graph(lnT, lnP, xerr=inc_lnT, yerr=inc_lnP, name="Q4", xname=r"$\ln(\Delta T)$", yname=r"$\ln(P)$", title=r"$\ln(P)$ en funció de $\ln(\Delta T)$, amb $\Delta T = T-T_a$")

idx = np.argsort(T)
lnT = lnT[idx]
lnP = lnP[idx]

for i in range(len(lnP)-3):
    coef, cov = np.polyfit(lnT[:-i-1], lnP[:-i-1], 1, cov=True)

    pendent = coef[0]
    ordenada = coef[1]

    inc_pendent = np.sqrt(cov[0, 0])
    inc_ordenada = np.sqrt(cov[1, 1])

    # print(f"Agafant desde n={i}:")
    # print(f"Pendent = {pendent:.3f} ± {inc_pendent:.3f}")
    # print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")

coef, cov = np.polyfit(lnT[:10], lnP[:10], 1, cov=True)

pendent = coef[0]
ordenada = coef[1]

inc_pendent = np.sqrt(cov[0, 0])
inc_ordenada = np.sqrt(cov[1, 1])

print("___Q5___")
print(f"Pendent = {pendent:.3f} ± {inc_pendent:.3f}")
print(f"Ordenada = {ordenada:.3f} ± {inc_ordenada:.3f}\n")

graphReg(lnT[:10], lnP[:10], xerr=inc_lnT[idx][:10], yerr=inc_lnP[idx][:10], name="Q5", xname=r"$\ln(\Delta T)$", yname=r"$\ln(P)$", title=r"$\ln(P)$ en funció de $\ln(\Delta T)$, regressió lineal (10 primers punts)")

