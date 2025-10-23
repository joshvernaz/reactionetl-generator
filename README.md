# Ethyl Acetate Saponification Simulation

This project numerically simulates the saponification of ethyl acetate with sodium hydroxide in a batch reactor using a Runge–Kutta 4th-order integrator. The model simultaneously solves the coupled mole and energy balances for the system, including heat transfer effects through the reactor wall.

---

## Reaction Overview

The saponification (base hydrolysis) reaction is:

$$
\text{CH}_3\text{COOC}_2\text{H}_5 + \text{NaOH} \rightarrow \text{CH}_3\text{COONa} + \text{C}_2\text{H}_5\text{OH}
$$

This is modeled as an elementary, second-order irreversible reaction:

$$
r_A = A  e^{-\frac{E_A}{R T}}  C_A  C_B
$$

---

## Differential Equations

### Mole Balances

The mole (material) balances are defined using the temperature-dependent Arrhenius equation and the concentrations of reactants $A$ and $B$.

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
A = \frac{10 \cdot 10^6}{1000} \frac{m^3}{mol \cdot s}
$$

Borovinskaya, E.; Khaydarov, V.; Strehle, N.; Musaev, A.; Reschetilowski, W. Experimental Studies of Ethyl Acetate Saponification Using Different Reactor Systems: The Effect of Volume Flow Rate on Reactor Performance and Pressure Drop. *Appl. Sci.* **2019**, *9*, 532. https://doi.org/10.3390/app9030532 

This model assumes perfect mixing, allowing us to use the bulk concentrations of reactants.

### Energy Balance

We begin with the unsteady state energy balance for a closed system:

$$
\rho VC_P\frac{dT}{dt} = \dot{Q} + \dot{W}_S + \Delta H_{Rx}(T)(-r_AV)
$$

We assume shaft work to be negligible compared to heat transfer and enthalpy of reaction.

We then substitute $\dot{Q}$ for $UA(T-T{cool})$, the overall heat transfer coefficient $(U)$ multiplied by the area through which heat is transferred $(A)$ multiplied by the temperature difference between the interior and exterior of the reaction vessel $(T-T_{cool})$.

Finally, rearranging, we get the energy balance:

$$
\frac{dT}{dt} = -\frac{\frac{UA}{V} (T-T_{cool})\Delta H_{Rx}(T) \,r_A}{\rho C_P}
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

This model assumes constant density. Heat losses other than wall conduction/convection are assumed to be negligible.

---

## Key Parameters

| Parameter                                     | Symbol              | Value                        | Units                              | Description                     |
|:--------------------------------------------- |:------------------- |:---------------------------- |:---------------------------------- |:------------------------------- |
| Gas constant                                  | $R$                 | $8.314$                      | $\frac{J}{mol^{-1}\cdot K^{-1}}$   | Ideal gas constant              |
| Pre-exponential factor                        | $A$                 | $\frac{1.0\cdot10^7} {1000}$ | $\frac{m^3}{mol^{-1}\cdot s^{-1}}$ | Arrhenius prefactor             |
| Activation energy                             | $E_A$               | $45380$                      | $\frac{J}{mol^{-1}}$               | From Borovinskaya et al. (2019) |
| Enthalpy of reaction (reference)              | $\Delta H_{Rx,298}$ | $-50210$                     | $\frac{J}{mol^{-1}}$               | From NIST and ANL ATcT          |
| Density                                       | $\rho$              | $1050$                       | $\frac{kg}{m^3}$                   | Approx. water-like solution     |
| Heat capacity (constant pressure)             | $C_P$               | $4100$                       | $\frac{J}{kg^{-1}\cdot K^{-1}}$    | Assumed constant                |
| Thermal conductivity                          | $k_c$               | $1.1$                        | $\frac{W}{m^{-1}\cdot K^{-1}}$     | Reactor wall                    |
| Interior convective heat transfer coefficient | $h_i$               | $500$                        | $\frac{W}{m^{-2}\cdot K^{-1}}$     | Interior                        |
| Exterior convective heat transfer coefficient | $h_o$               | $1000$                       | $\frac{W}{m^{-2}\cdot K^{-1}}$     | Exterior                        |
| Coolant temperature                           | $T_{cool}$          | $295$                        | $K$                                | Jacket water                    |
| Reactor diameter                              | —                   | $0.0635$                     | $m$                                | Interior                        |
| Reactor height                                | —                   | $0.316$                      | $m$                                | Interior                        |
| Wall thickness                                | —                   | $0.005$                      | $m$                                | Steel wall                      |
| Time step                                     | —                   | $0.5$                        | $s$                                | Integration step size           |

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

## Running the Simulation

The simulation can be run from the project root with `python main.py` .

You may also run the simulation from the terminal with `path-to-project-root/run_reaction_simulation.sh`, but the script should be updated to match your file structure. Be sure to update `PROJECT_DIR` to the project directory in your file system, `PYTHON` with the path to a valid interpreter, `LOG_DIR` with where you would like shell simulation logs to be kept. If the paths above are updated, you can set this up to run as a cron job.

---

## Simulation Randomization

Running the simulation will generate random initial conditions in the following ranges:

$$
0 \leq C_A,C_B \leq 1500 \frac{mol}{m^3} 
$$

$$
278K \leq T \leq 353K
$$

$$
20421\leq E_A \leq 34035 \frac{J}{mol} \cup 45380\frac{J}{mol}
$$

Note, the simulation will determine whether to randomize the activation energy, simulating a catalyzed reaction. If catalyzed, the activation energy will range between $0.45E_{A,uncatalyzed}\leq E_{A,catalyzed} \leq 0.75E_{A,uncatalyzed}$



If catalyzed, the activation energy is quantized in increments of $0.001E_{A,uncatalyzed}$

---

## File Structure

```
.
├── incoming
│   └── 2025-10-22
│       ├── metadata_34607759-a0d8-422c-bce2-3d48eca1919f.json
│       ├── metadata_bbce830f-1bec-47f1-963e-3442e012a39f.json
│       ├── results_34607759-a0d8-422c-bce2-3d48eca1919f.csv
│       └── results_bbce830f-1bec-47f1-963e-3442e012a39f.csv
├── logs
│   ├── run_reaction_simulation.sh
│   ├── sim.err
│   └── sim.log
└── src
    └── generator
        ├── file_manager.py
        ├── main.py
        ├── __pycache__
        ├── reaction_parameters.py
        ├── README.md
        ├── requirements.txt
        └── run_reaction_simulation.sh
```

---

## Output Data

| Column         | Units             | Description                    |
| -------------- | ----------------- | ------------------------------ |
| `CA (mol/m^3)` | $\frac{mol}{m^3}$ | Ethyl acetate concentration    |
| `CB (mol/m^3)` | $\frac{mol}{m^3}$ | Hydroxide ion concentration    |
| `CC (mol/m^3)` | $\frac{mol}{m^3}$ | Acetate ion concentration      |
| `CD (mol/m^3)` | $\frac{mol}{m^3}$ | Ethanol concentration          |
| `T (K)`        | $K$               | Reactor temperature            |
| `Tsensor (K)`  | K                 | Simulated thermocouple reading |
| `t (sec)`      | $sec$             | Simulation time                |
| `SimulationID` | -                 | UUID for traceability          |

---

## References

- Borovinskaya, E.; Khaydarov, V.; Strehle, N.; Musaev, A.; Reschetilowski, W. Experimental Studies of Ethyl Acetate Saponification Using Different Reactor Systems: The Effect of Volume Flow Rate on Reactor Performance and Pressure Drop. *Appl. Sci.* **2019**, *9*, 532. https://doi.org/10.3390/app9030532

- NIST Chemistry WebBook - Ethyl Acetate, Ethanol

- Argonne National Laboratory, Active Thermochemical Tables - Acetate Ion, Hydroxide Ion
