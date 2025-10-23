# Ethyl Acetate Saponification Simulation

This project numerically simulates the saponification of ethyl acetate with sodium hydroxide in a batch reactor using a Runge–Kutta 4th-order integrator. The model simultaneously solves the coupled mole and energy balances for the system, including heat transfer effects through the reactor wall.

---

## Reaction Overview

The saponification (base hydrolysis) reaction is:

$$
\text{CH}_3\text{COOC}_2\text{H}_5 + \text{NaOH} \rightarrow \text{CH}_3\text{COONa} + \text{C}_2\text{H}_5\text{OH}
$$

This is modeled as an **elementary, second-order irreversible reaction**:

$$
r_A = A \, e^{-\frac{E_A}{R T}} \, C_A \, C_B
$$

---

## Differential Equations

### Mole Balances

$$
\frac{dC_A}{dt} = -r_A = -k_A(T)C_AC_B
$$

$$
\frac{dC_B}{dt} = -r_A = -k_A(T)C_AC_B
$$

$$
\frac{dC_C}{dt} = r_A = k_A(T)C_AC_B
$$

$$
\frac{dC_D}{dt} = r_A = k_A(T)C_AC_B
$$

$$
k_A(T) = Ae^{\frac{E_A}{RT}}
$$

We assume the following pre-exponential factor:

$$
A = \frac{10 * 10^6}{1000} \frac{m^3}{mol * s}
$$

Borovinskaya, E.; Khaydarov, V.; Strehle, N.; Musaev, A.; Reschetilowski, W. Experimental Studies of Ethyl Acetate Saponification Using Different Reactor Systems: The Effect of Volume Flow Rate on Reactor Performance and Pressure Drop. *Appl. Sci.* **2019**, *9*, 532. https://doi.org/10.3390/app9030532 

### Energy Balance

We begin with the unsteady state energy balance for a closed system:

$$
\rho VC_P\frac{dT}{dt} = \dot{Q} + \dot{W}_S + \Delta H_{Rx}(T)(-r_AV)
$$

We assume shaft work to be negligible compared to heat transfer and enthalpy of reaction.

We then substitute $\dot{Q}$ for $UA(T-T{cool})$, the overall heat transfer coefficient $(U)$ multiplied by the area through which heat is transferred $(A)$ multiplied by the temperature difference between the interior and exterior of the reaction vessel $(T-T_{cool})$.

Finally, rearranging, we get the energy balance:

$$
\frac{dT}{dt} = -\frac{\frac{UA}{V} (T-T_{cool})\Delta H_{Rx}(T) r_A}{\rho C_P}
$$


$U$ is calculated by:

$$
U = \left(\frac{1}{h_i} + \frac{\delta}{k_c} + \frac{1}{h_o}\right)^{-1}
$$

where $h_i$ is the convective heat transfer coefficient inside the reactor, $h_o$ is the convective heat transfer coefficient outside the reactor, $\delta$ is the thickness of the reactor wall, and $k_c$ is the conductive heat transfer coefficient for the reactor material.

$\Delta H_{Rx}(T)$ is calculated using a reference enthalpy of reaction at $298$ $K$, a reference constant-pressure heat capacity assumed to be constant $(C_P)$, and the temperature difference between the reactants and the reference temperature $(T-298$ $K)$:

$$
\Delta{H_{Rx}}=\Delta H_{Rx,298 K}C_P(T-298K)
$$

---

## Key Parameters

| Parameter                                     | Symbol              | Value               | Units        | Description                     |
|:--------------------------------------------- |:------------------- |:------------------- |:------------ |:------------------------------- |
| Gas constant                                  | $R$                 | 8.314               | J mol⁻¹ K⁻¹  | Ideal gas constant              |
| Pre-exponential factor                        | $A$                 | \(1.0*10^7 / 1000\) | m³ mol⁻¹ s⁻¹ | Arrhenius prefactor             |
| Activation energy                             | $E_A$               | 45 380              | J mol⁻¹      | From Borovinskaya et al. (2019) |
| Enthalpy of reaction (reference)              | $\Delta H_{Rx,298}$ | −50 210             | J mol⁻¹      | From NIST and ANL ATcT          |
| Density                                       | $\rho$              | 1050                | kg m⁻³       | Approx. water-like solution     |
| Heat capacity (constant pressure)             | $C_P$               | 4100                | J kg⁻¹ K⁻¹   | Assumed constant                |
| Thermal conductivity                          | $k_c$               | 1.1                 | W m⁻¹ K⁻¹    | Reactor wall                    |
| Interior convective heat transfer coefficient | $h_i$               | 500                 | W m⁻² K⁻¹    | Interior                        |
| Exterior convective heat transfer coefficient | $h_o$               | 1000                | W m⁻² K⁻¹    | Exterior                        |
| Coolant temperature                           | $T_{cool}$          | 295                 | K            | Jacket water                    |
| Reactor diameter                              | —                   | 0.0635              | m            | Interior                        |
| Reactor height                                | —                   | 0.316               | m            | Interior                        |
| Wall thickness                                | —                   | 0.005               | m            | Steel wall                      |
| Time step                                     | —                   | 0.5                 | s            | Integration step size           |

---

## Model Features

- Arrhenius temperature dependence for the rate constant

- Dynamic reaction enthalpy correction using a heat capacity term

- Heat transfer modeled with interior/exterior convection and conduction through the reactor wall

- Noise simulation for thermocouple readings (Gaussian, Type T thermocouple)

- Automatic stop conditions:
  
  - Steady-state detection
  
  - Full conversion, defined as 99.5% conversion
  
  - Runaway reactions or numerical instability
  
  - Simulation time limits

---

## ODE Solver File Structure

`.
├── file_manager.py
├── main.py
├── reaction_parameters.py
├── README.md
└── requirements.txt`

---

## Generated Data File Structure

`├── logs
│   ├── run_reaction_simulation.sh
│   ├── sim.err
│   └── sim.log
├── incoming
│   ├── YYYY-mm-dd
│   │   ├── results_<uuid>.csv
│   │   ├── metadata_<uuid>.json`


