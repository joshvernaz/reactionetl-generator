from datetime import datetime
from reaction_parameters import *
from math import exp, isnan
from pandas import DataFrame
from uuid import uuid4
from numpy.random import normal, default_rng, randint
from file_manager import *
from pathlib import Path
from typing import List, Any

import reaction_parameters

TIME_STEP = .5

"""
This reaction is a system of ODEs that should be solved simultaneously.
dCA/dt = -rA = -k_A(T) * CA * CB
dCB/dt = -rA = -k_A(T) * CA * CB
dCC/dt =  rA =  k_A(T) * CA * CB
dCD/dt =  rA =  k_A(T) * CA * CB

-k_A(T) will be computed at T by using the Arrhenius equation, k_A = Ar * exp(-Ea / (R * T))

Energy balance:
rho*V*CP*dT/dt = Qdot + Wsdot + (-DH_Rx(T)) * (-rA * V); shaft work negligible -> Wsdot = 0
dT/dt = (UA/V * (T - Tcool) + (-DH_Rx(T)) * (-rA)) / (rho*CP)

DH_Rx(T) will be computed at T by using DH_Rx(298 K) + CP * (T - 298 K) and substituted in dT/dt.

dT/dt = ( -UA/V * (T - Tcool) - (DH_Rx(298 K) + CP * (T - 298 K)) * dCA/dt) / (rho*CP)
      = ( -UA/V * (T-Tcool) - (DH_Rx(298K)+CP*(T-298K)) * k_A(T)*CA*CB ) / (rho*CP)
      = ( -UA/V * (T-Tcool) - (DH_Rx(298K)+CP*(T-298K)) * Ar*exp(-Ea/(R*T))*CA*CB ) / (rho*CP)

"""

def current_slopes(t, current_state):
    """Returns functions for calculating slope of each ODE given current conditions (current_state)"""
    [CA, CB, CC, CD, T] = current_state 

    rA = Ar * exp(-Ea/(R*T)) * CA * CB

    dCA_dt = -rA
    dCB_dt = -rA
    dCC_dt = rA
    dCD_dt = rA

    dH = DH_Rx_298 + CP * (T - 298)
    dT_dt = (-UA_V * (T-Tcool) - dH * rA ) / (rho * CP)
    
    return [dCA_dt, dCB_dt, dCC_dt, dCD_dt, dT_dt, 0]

def RK4_step(functions, t, current_state, h):
    """Integrator for system of ODEs to be solved simultaneously"""
    k1 = functions(t, current_state)
    k2 = functions(t + 0.5*h, [current_state[i] + 0.5*h*k1[i] for i in range(len(current_state))])
    k3 = functions(t + 0.5*h, [current_state[i] + 0.5*h*k2[i] for i in range(len(current_state))])
    k4 = functions(t + h, [current_state[i] + h*k3[i] for i in range(len(current_state))])

    next_state = [current_state[i] + (h/6)*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(len(current_state))]
    
    return next_state

def choose_initial_conditions(CA0: float, CB0: float, CC0: float = 0, CD0: float = 0, T0: float = 298.15):
    return [CA0, CB0, CC0, CD0, T0]

def simulate_sensor_noise(T: float, stdev: float = 0.333):
    """
    Simulates thermocouple measurement noise assuming a Type T thermocouple, Gaussian distribution
    Limit of error reported +/- 1.0 K at typical temperatures, so we choose that as the 3*stdev error, including 99.7% of samples
    """
    measurement_error = normal(loc=0, scale=stdev, size=None)
    T += measurement_error
    return T

def stop_conditions(state_history: List[Any], tol: float, h: float, t_check: float, CA_min: float, CB_min: float, current_time: float, max_time: float) -> tuple[bool, str | None]:
    """Defines stopping conditions for the integrator"""
    # Check for absence of reaction progress (w.r.t CA) within a tolerance value (tau) for the last t_check seconds
    data_points_back = int(t_check//h) + 1
    if len(state_history) > data_points_back:
        if state_history[-data_points_back][0] - state_history[-1][0] < tol:
            return True, "steady_state"
    
    # Check for arbitrarily defined full conversion
    if state_history[-1][0] < CA_min or state_history[-1][1] < CB_min:
        return True, "full_conversion"

    # Check for passing safeguard simulation time
    if current_time >= max_time:
        return True, "time_limit"

    # Check for invalid states; only check CA because other materials constrained by material balance
    if isnan(state_history[-1][0]) or state_history[-1][0] < 0:
        return True, "numerical_error"

    # Check for runaway reaction temperature
    if not (50 <= abs(state_history[-1][4]) <= 1000):
        return True, "runaway_reaction"

    return False, None

def generate_random_conditions():
    """
    Generates random starting conditions for the simulation.
    0 mol/m^3 >= CA, CB >= 1500 mol/m^3 (0 M - 1.5 M)
    5 deg C >= T >= 80 deg C
    """
    CA = 1500 * default_rng().random()
    CB = 1500 * default_rng().random()
    CC = 0
    CD = 0
    T = float(randint(low=278, high=353))

    return CA, CB, CC, CD, T

def main():
    # Add chance for reaction to be catalyzed - affect activation energy by factor of 0.45-0.75
    if default_rng().random() <= 0.5:
        Ea = reaction_parameters.Ea * (0.45 + randint(low=0, high=300) * 0.001)
    else:
        Ea = reaction_parameters.Ea
    
    fm = FileManager()
    fm.make_base_dirs_if_not_exists()
    fm.make_sub_dirs_if_not_exists()

    current_state = choose_initial_conditions(*generate_random_conditions())
    CA0, CB0, T0 = current_state[0], current_state[1], current_state[4]
    t = 0
    results = []
    results.append(current_state + [simulate_sensor_noise(current_state[4])] + [t])

    while True:
        stop_flag, reason = stop_conditions(state_history=results, tol=CA0*0.0005, h=TIME_STEP, t_check=15.0, CA_min=CA0*0.005, CB_min=CB0*0.005, current_time=t, max_time=7200)
        if stop_flag:
            break
        
        results.append(current_state + [simulate_sensor_noise(current_state[4])] + [t])
        current_state = RK4_step(functions=current_slopes, t=t, current_state=current_state, h=TIME_STEP)
        t += TIME_STEP

    simulation_id = str(uuid4())
    metadata_file = {
        "simulation_id": simulation_id,
        "reaction_name": "ethyl_acetate_saponification",
        "activation_energy (J/mol)": f"{Ea}",
        "CA0_(mol/m^3)": CA0,
        "CB0_(mol/m^3)": CB0,
        "T0_(K)": T0,
        "date_run": datetime.now().isoformat(),
        "stop_reason": reason,
        "stop_time_(s)": t,
        }

    df = DataFrame(data=results, columns=["CA (mol/m^3)","CB (mol/m^3)","CC (mol/m^3)","CD (mol/m^3)","T (K)","Tsensor (K)","t (sec)"])
    df["SimulationID"] = simulation_id
    # print(df)
    # print(metadata_file)

    fm.save_csv(df=df, file_name=f"results_{simulation_id}.csv")
    fm.save_metadata(metadata_file=metadata_file, file_name=f"metadata_{simulation_id}.json")

    # print(f"Ea used for this simulation was: {Ea}")
    # print(f"Stop reason was {reason}")

# def maintest():
#     print(generate_random_conditions())

if __name__ == "__main__":
    main()
    
    
