# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 08:19:27 2019

@author: SESA539950
"""

from scipy.optimize import fsolve
import numpy as np

data_center = {
    "Dropped ceiling (with flooded supply)": [
        "Hot-aisle (Ducted)",
        "Ducted Rack",
        "None",
    ],
    "Raised-floor": ["Cold-aisle", "None", "External supply, Cold-aisle"],
    "Raised-floor with dropped ceiling": ["Hot-aisle (Ducted)", "Cold-aisle", "None"],
    "Close-coupled Cooling": ["Hot-aisle", "Cold-aisle"],
}

Q = np.zeros(8)
P = np.zeros(3)

a_tile = 2 * 2 * 0.092903  # Single tile area (m^2)


class FNMsolver:
    def __init__(
        self,
        architecture,
        containment,
        w_area,
        obs_area,
        Q_cool,
        n_rack,
        q_IT,
        b_tile_rf,
        n_tile,
        b_tile_dc,
        f_floor,
        cut_area,
        f_DC,
        a_SP,
        a_RL,
        a_D_HACS,
        a_D_rack,
        rho,
        q_IT_rack,
        Q_c,
        Q_room,
        Q_FP,
    ):
        self.architecture = architecture  # Architecture selected
        self.containment = containment  # Containment selected
        self.w_area = w_area  # Total whitespace area [m^2]
        self.Q_cool = Q_cool * 0.0004719474  # Total cooling airflow rate [m^3/s]
        self.n_rack = n_rack  # Number of racks
        self.q_IT = q_IT * 1000  # IT power per rack [W]
        self.q_IT_rack = q_IT_rack  # Airflow per kW of IT heat [cfm]
        self.Q_IT = (
            self.q_IT_rack * self.q_IT / 1000 * self.n_rack * 0.0004719474
        )  # Total IT airflow rate [m^3/s]
        self.b_tile_rf = b_tile_rf
        if (
            self.containment == "Hot-aisle (Ducted)"
        ):  # Number of tiles in case of Dropped ceiling
            self.n_tile = 0
        else:
            self.n_tile = n_tile
        self.b_tile_dc = b_tile_dc
        self.obs_area = obs_area
        self.f_floor = f_floor  # Base floor leakage loss coefficient
        self.cut_area = cut_area * self.n_rack  # Total cutout tile leakage area
        self.f_DC = f_DC  # Dropped ceiling leakage loss coefficient
        self.a_SP = a_SP
        self.a_RL = a_RL
        self.a_D_HACS = a_D_HACS
        self.a_D_rack = a_D_rack
        self.rho = rho
        self.Q_c = Q_c * 0.0004719474  # External supply in the containment
        self.Q_room = Q_room * 0.0004719474  # External supply in the room
        self.Q_FP = Q_FP * 0.0004719474  # External supply in the floor plenum

    def caseFNM(self):
        if self.architecture == list(data_center)[0]:
            if self.containment == list(data_center.values())[0][0]:
                case_flowResNet = 1
            elif self.containment == list(data_center.values())[0][1]:
                case_flowResNet = 2
            else:
                case_flowResNet = 3
        elif self.architecture == list(data_center)[1]:
            if self.containment == list(data_center.values())[1][0]:
                case_flowResNet = 4
            elif self.containment == list(data_center.values())[1][1]:
                case_flowResNet = 5
            else:
                case_flowResNet = 6
        elif self.architecture == list(data_center)[2]:
            if self.containment == list(data_center.values())[2][0]:
                case_flowResNet = 7
            elif self.containment == list(data_center.values())[2][1]:
                case_flowResNet = 8
            else:
                case_flowResNet = 9
        elif self.architecture == list(data_center)[3]:
            if self.containment == list(data_center.values())[3][0]:
                case_flowResNet = 10
            else:
                case_flowResNet = 11

        return case_flowResNet

    def flowRes(self):
        global_ar = self.Q_cool / self.Q_IT
        if (
            self.architecture == list(data_center)[1]
            or self.architecture == list(data_center)[2]
        ):
            net_f_area = (
                self.w_area - self.obs_area - (self.n_rack * (2 * 3.5 + 2 * 2))
            ) * 0.092903  # Rack area = 2*3.5 ft^2 and Tile area = 2*2 ft^2
        else:
            net_f_area = (self.w_area - self.obs_area) * 0.092903

        if (
            self.architecture == list(data_center)[0]
            or self.architecture == list(data_center)[2]
        ):
            if self.containment == "Hot-aisle (Ducted)":
                net_c_area = (
                    self.w_area - self.obs_area - (self.n_rack * 2 * 3.5)
                ) * 0.092903  # Duct area = Rack area
            else:
                net_c_area = (
                    self.w_area - self.obs_area - (self.n_tile * 2 * 2)
                ) * 0.092903  # Ceiling tile area = 2*2 ft^2
        else:
            net_c_area = (self.w_area - self.obs_area) * 0.092903

        a_SP = self.a_SP / (self.n_rack ** 2)

        a_RL = self.a_RL / self.n_rack ** 2

        f_t_rf = (
            1
            + 0.5 * (1 - self.b_tile_rf) ** 0.75
            + 1.414 * (1 - self.b_tile_rf) ** 0.375
        ) / self.b_tile_rf ** 2
        a_FT = 0.5 * f_t_rf * self.rho / ((a_tile * self.n_rack) ** 2)

        f_t_dc = (
            1
            + 0.5 * (1 - self.b_tile_dc) ** 0.75
            + 1.414 * (1 - self.b_tile_dc) ** 0.375
        ) / self.b_tile_dc ** 2
        if self.containment == "Hot-aisle (Ducted)":
            a_CT = 0
        else:
            a_CT = 0.5 * f_t_dc * self.rho / ((a_tile * self.n_tile) ** 2)

        if self.containment == "Ducted Rack":
            a_D = self.a_D_rack
        else:
            a_D = self.a_D_HACS / (self.n_rack ** 2)

        if net_f_area == 0:
            a_RF = 10 ** 10
        else:
            b_cut = self.cut_area / net_f_area
            f_cut = (
                1 + 0.5 * (1 - b_cut) ** 0.75 + 1.414 * (1 - b_cut) ** 0.375
            ) / b_cut ** 2
            f_RF = self.f_floor * f_cut / (np.sqrt(self.f_floor) + np.sqrt(f_cut)) ** 2
            a_RF = 0.5 * f_RF * self.rho / (net_f_area ** 2)

        if net_c_area == 0:
            a_DC = 10 ** 10
        else:
            a_DC = 0.5 * self.f_DC * self.rho / (net_c_area ** 2)

        a = [a_SP, a_RL, a_FT, a_CT, a_D, a_RF, a_DC]
        return global_ar, net_f_area, net_c_area, self.Q_IT, a

    # =============================================================================
    #     a_SP = a[0]           # Server plane resistance
    #     a_RL = a[1]           # Rack leakage resistance
    #     a_FT = a[2]           # Tile leakage resistance (Raised-floor)
    #     a_CT = a[3]           # Tile leakage resistance (Dropped ceiling)
    #     a_D = a[4]            # Duct leakage resistance
    #     a_RF = a[5]           # Raised-floor leakage resistance
    #     a_DC = a[6]           # Dropped ceiling leakage resistance
    #
    #     Q_IT = Q[0]           # Total IT airflow
    #     Q_cool = Q[1]         # Total cooling airflow
    #     Q_SP = Q[2]           # Server plane leakage
    #     Q_RL = Q[3]           # Rear-to-top leakage
    #     Q_D = Q[4]            # Duct leakage
    #     Q_T_rf = Q[5]         # Tile leakage (Raised-floor)
    #     Q_T_dc = Q[6]         # Tile leakage (Dropped ceiling)
    #     Q_DC = Q[7]           # Dropped ceiling leakage
    #     Q_RF = Q[8]           # Raised floor leakage
    #
    #     P_C = P[0]            # Containment pressure
    #     P_CP = P[1]           # Ceiling plenum pressure
    #     P_FP = P[2]           # Raised-floor plenum pressure
    #     P_rear = P[3]         # Rack-rear pressure
    # =============================================================================

    # Case - 1.1: Dropped ceiling (with flooded supply), Hot-aisle containment

    def case_1(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(-P[0]) * np.sqrt(np.abs(P[0]) / a[0])
        f[3] = Q[3] - np.sign(-P[0]) * np.sqrt(np.abs(P[0]) / a[1])
        f[4] = Q[4] - np.sign(P[0] - P[1]) * np.sqrt(np.abs(P[0] - P[1]) / a[4])
        f[5] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[6] = Q[4] - Q[0] - Q[2] - Q[3]
        f[7] = Q[1] - Q[4] - Q[7]
        f[8] = Q[5]
        f[9] = Q[6]
        f[10] = Q[8]
        f[11] = P[2]
        f[12] = P[3]

        return f

    # Case - 1.2: Dropped ceiling (with flooded supply), Ducted Rack (Individual)

    def case_2(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(-P[3]) * np.sqrt(np.abs(P[3]) / a[0])
        f[3] = Q[3] - np.sign(P[3] - P[0]) * np.sqrt(np.abs(P[3] - P[0]) / a[1])
        f[4] = Q[4] - np.sign(P[0] - P[1]) * np.sqrt(np.abs(P[0] - P[1]) / a[4])
        f[5] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[6] = Q[4] - Q[0] - Q[2]
        f[7] = Q[4] - Q[3]
        f[8] = Q[1] - Q[4] - Q[7]
        f[9] = Q[5]
        f[10] = Q[6]
        f[11] = Q[8]
        f[12] = P[2]

        return f

    # Case - 1.2: Dropped ceiling (with flooded supply), No containment

    def case_3(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[6] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[3])
        f[3] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[4] = Q[1] - Q[6] - Q[7]
        f[5] = Q[2]
        f[6] = Q[3]
        f[7] = Q[4]
        f[8] = Q[5]
        f[9] = Q[8]
        f[10] = P[0]
        f[11] = P[2]
        f[12] = P[3]

        return f

    # Case - 2.1: Raised-floor, Cold-aisle containment

    def case_4(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(P[0]) * np.sqrt(np.abs(P[0]) / a[0])
        f[3] = Q[5] - np.sign(P[2] - P[0]) * np.sqrt(np.abs(P[2] - P[0]) / a[2])
        f[4] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[5] = Q[5] - Q[0] - Q[2]
        f[6] = Q[1] - Q[5] - Q[8]
        f[7] = Q[3]
        f[8] = Q[4]
        f[9] = Q[6]
        f[10] = Q[7]
        f[11] = P[1]
        f[12] = P[3]

        return f

    # Case - 2.2: Raised-floor, No containment

    def case_5(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[5] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[2])
        f[3] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[4] = Q[1] - Q[5] - Q[8]
        f[5] = Q[2]
        f[6] = Q[3]
        f[7] = Q[4]
        f[8] = Q[6]
        f[9] = Q[7]
        f[10] = P[0]
        f[11] = P[1]
        f[12] = P[3]

        return f

    # Case - 2.3: Raised-floor, External supply, Cold-aisle containment

    def case_6(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(P[0]) * np.sqrt(np.abs(P[0]) / a[0])
        f[3] = Q[5] - np.sign(P[2] - P[0]) * np.sqrt(np.abs(P[2] - P[0]) / a[2])
        f[4] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[5] = Q[5] + self.Q_c - Q[0] - Q[2]
        f[6] = Q[1] + self.Q_FP - Q[5] - Q[8]
        f[7] = Q[3]
        f[8] = Q[4]
        f[9] = Q[6]
        f[10] = Q[7]
        f[11] = P[1]
        f[12] = P[3]

        return f

    # Case - 3.1: Raised-floor with dropped ceiling, Hot-aisle containment

    def case_7(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[5] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[2])
        f[3] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[4] = Q[2] - np.sign(-P[0]) * np.sqrt(np.abs(P[0]) / a[0])
        f[5] = Q[3] - np.sign(-P[0]) * np.sqrt(np.abs(P[0]) / a[1])
        f[6] = Q[4] - np.sign(P[0] - P[1]) * np.sqrt(np.abs(P[0] - P[1]) / a[4])
        f[7] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[8] = Q[4] - Q[0] - Q[2] - Q[3]
        f[9] = Q[4] - Q[5] - Q[8]
        f[10] = Q[1] - Q[4] - Q[7]
        f[11] = Q[6]
        f[12] = P[3]

        return f

    # Case - 3.2: Raised-floor with dropped ceiling, Cold-aisle containment

    def case_8(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[5] - np.sign(P[2] - P[0]) * np.sqrt(np.abs(P[2] - P[0]) / a[2])
        f[3] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[4] = Q[2] - np.sign(P[0]) * np.sqrt(np.abs(P[0]) / a[0])
        f[5] = Q[3]
        f[6] = Q[6] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[3])
        f[7] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[8] = Q[5] - Q[0] - Q[2]
        f[9] = Q[5] - Q[6] - Q[7]
        f[10] = Q[1] - Q[5] - Q[8]
        f[11] = Q[4]
        f[12] = P[3]

        return f

    # Case - 3.3: Raised-floor with dropped ceiling, No containment

    def case_9(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[5] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[2])
        f[3] = Q[8] - np.sign(P[2]) * np.sqrt(np.abs(P[2]) / a[5])
        f[4] = Q[6] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[3])
        f[5] = Q[7] - np.sign(-P[1]) * np.sqrt(np.abs(P[1]) / a[6])
        f[6] = Q[1] - Q[6] - Q[7]
        f[7] = Q[1] - Q[5] - Q[8]
        f[8] = Q[2]
        f[9] = Q[3]
        f[10] = Q[4]
        f[11] = P[0]
        f[12] = P[3]

        return f

    # Case - 4.1: Close-coupled Cooling, Hot-aisle containment

    def case_10(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(-P[0]) * np.sqrt(np.abs(P[0] / a[0]))
        f[3] = Q[3] - np.sign(-P[0]) * np.sqrt(np.abs(P[0] / a[1]))
        f[4] = Q[1] - Q[0] - Q[2] - Q[3]
        f[5] = Q[4]
        f[6] = Q[5]
        f[7] = Q[6]
        f[8] = Q[7]
        f[9] = Q[8]
        f[10] = P[1]
        f[11] = P[2]
        f[12] = P[3]

        return f

    # Case - 4.2: Close-coupled Cooling, Cold-aisle containment

    def case_11(self, z):
        Q = z[0:9]
        P = z[9:13]
        f = np.zeros(13)

        a = self.flowRes()[4]

        f[0] = Q[0] - self.Q_IT
        f[1] = Q[1] - self.Q_cool
        f[2] = Q[2] - np.sign(P[0]) * np.sqrt(np.abs(P[0] / a[0]))
        f[3] = Q[3] - np.sign(P[0]) * np.sqrt(np.abs(P[0] / a[1]))
        f[4] = Q[1] - Q[0] - Q[2] - Q[3]
        f[5] = Q[4]
        f[6] = Q[5]
        f[7] = Q[6]
        f[8] = Q[7]
        f[9] = Q[8]
        f[10] = P[1]
        f[11] = P[2]
        f[12] = P[3]

        return f

    def calcAirflow(self):
        case_flowResNet = self.caseFNM()
        if case_flowResNet == 1:
            z = fsolve(self.case_1, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 2:
            z = fsolve(self.case_2, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 3:
            z = fsolve(self.case_3, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 4:
            z = fsolve(self.case_4, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 5:
            z = fsolve(self.case_5, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 6:
            z = fsolve(self.case_6, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 7:
            z = fsolve(self.case_7, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 8:
            z = fsolve(self.case_8, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 9:
            z = fsolve(self.case_9, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 10:
            z = fsolve(self.case_10, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        elif case_flowResNet == 11:
            z = fsolve(self.case_11, np.ones(13))
            Q = z[0:9]
            P = z[9:13]

        return Q, P
