import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

def knots_to_ftpersec(speed):
    """
        Converts Knots to Feet per Sec
    :param speed: float
    :return: Speed in Feet per Sec
    """
    return speed*1.68781

def thrust_required(rho_inf:float, v_inf:float, s:float, cd0_:float, k:float, w:float)-> float:
    cl = (2*w)/(rho_inf*v_inf**2*s)
    return 0.5*rho_inf*v_inf**2*s*(cd0_ + k*cl**2)

def thrust_required_induced(rho_inf:float, v_inf:float, s:float,k:float, w:float)-> float:
    return k*(2*w**2)/(rho_inf*(v_inf**2)*s)

def thrust_required_parasitic(rho_inf:float, v_inf:float, s:float, cd0_:float)-> float:
    return 0.5*rho_inf*v_inf**2*s*(cd0_)



weight = 200000
wing_area = 1318
wing_span = 117.416666667
cd0 = 0.0185
thrust = 66000
aspect_ratio = wing_span**2/wing_area
e = 0.92
K = 1/(pi*e*aspect_ratio)
rho_sl = 23.77E-4

x_vals_sl = [i for i in range(80,750,10)]


tr_sl = [thrust_required(rho_sl, knots_to_ftpersec(x), wing_area, cd0, K, weight) for x in x_vals_sl]
tr_sl_induced = [thrust_required_induced(rho_sl, knots_to_ftpersec(x), wing_area, K, weight) for x in x_vals_sl]
tr_sl_parasitic = [thrust_required_parasitic(rho_sl, knots_to_ftpersec(x), wing_area, cd0) for x in x_vals_sl]


takeoff_vel_sl = [180, 180]
cruise_velocity_fl350_values = [11000, 46500]

TA_sl = 0.6*thrust
y_coords_sl = [TA_sl for _ in x_vals_sl]
takeoff_vel_sl = [180, 180]

plt.plot(x_vals_sl, y_coords_sl, 'k--', label = '$T_A$ at Sea Level %70 Throttle')
plt.plot(x_vals_sl,tr_sl,'k-',label = r"$T_R$")
plt.plot(x_vals_sl,tr_sl_induced,'r-', label = r"$T_{R}$ due to induced drag")
plt.plot(x_vals_sl,tr_sl_parasitic,'b-', label = r"$T_{R}$ due to parasite drag")

plt.ylabel('Thrust Required (lb)')
plt.xlabel('Velocity (kts)')
plt.legend(loc = 'lower right')
plt.show()

