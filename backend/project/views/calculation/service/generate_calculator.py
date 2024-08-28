from project.views.calculation.inerface import BXActCalculatorBase
from project.views.calculation.dataclass import *


class ClassicActCalculator(BXActCalculatorBase):
    def __init__(self, E, angle, Pad_thickness, clearance, y_offset, Disc_Width, y_move,
                 disc_wear, pad_wear, Lever_length, LLF, Offset_Lever,
                     PHH, WLB, WPHB, DCY, PAC, G_dimension, HTL, BFH,
                     DHB, HUTC, HLPC):
        super().__init__(E, angle, Pad_thickness, clearance, y_offset, Disc_Width, y_move,
                     disc_wear, pad_wear)
        self.Lever_length = Lever_length
        self.LLF = LLF
        self.Offset_Lever = Offset_Lever
        self.PHH = PHH
        self.WLB = WLB
        self.WPHB = WPHB
        self.DCY = DCY
        self.PAC = PAC
        self.G_dimension = G_dimension
        self.HTL = HTL
        self.BFH = BFH
        self.DHB = DHB
        self.HUTC = HUTC
        self.HLPC = HLPC
    @property
    def transfer_list(self):
        G30 = self.Disc_Width + 2 * (self.Pad_thickness + self.PHH + self.clearance)
        G = self.DCY + self.PAC + (self.Lever_length - self.LLF) / self.Lever_length * (
                    G30 - (self.DCY + self.PAC)) + 2 * self.Offset_Lever
        RR = ((self.LLF) ** 2 + (self.Offset_Lever) ** 2) ** 0.5
        L_0 = self.y_offset
        L_L = self.y_move
        G_W = self.WLB
        D_w = self.pad_wear + self.disc_wear + self.WPHB
        Lb = G30
        CR = self.clearance

        yyt = (G - Lb) / 2 + L_0
        xxt = (RR ** 2 - yyt ** 2) ** 0.5

        y_0 = yyt

        yyt_other = (G - Lb) / 2 - L_0
        xxt_other = (RR ** 2 - yyt_other ** 2) ** 0.5
        E_other = round(self.E + xxt - xxt_other, 2)

        y_low = yyt - abs(L_L) + CR
        y_up = (G + G_W - Lb) / 2 + L_0 + abs(L_L) + D_w + CR
        y_low_t = y_low

        if y_low * y_up > 0:
            y_low = y_low
        else:
            y_low = 0
        y_min = min(abs(y_low), abs(y_up))
        y_max = max(abs(y_low_t), abs(y_up))

        if y_min == abs(y_low):
            y_min_with = y_low
        else:
            y_min_with = y_up - self.WPHB - G_W / 2

        if y_max == abs(y_low_t):
            y_max_with = y_low_t
        else:
            y_max_with = y_up - self.WPHB - G_W / 2

        D_w_l_min = xxt - (RR ** 2 - y_min ** 2) ** 0.5
        D_w_l_max = xxt - (RR ** 2 - y_max ** 2) ** 0.5

        if y_max == abs(y_low_t):
            y_Emax = y_low_t
        else:
            y_Emax = y_up

        if y_min == abs(y_low):
            y_Emin = y_low
        else:
            y_Emin = y_up

        y_up_N1 = (G + G_W - Lb) / 2 + L_0 + abs(L_L) + D_w + CR - self.disc_wear
        y_max_N1 = max(abs(y_low_t), abs(y_up_N1))

        D_w_l_w_min = xxt - (RR ** 2 - y_max_N1 ** 2) ** 0.5

        if y_max_N1 == abs(y_low_t):
            y_max_with_N1 = y_low_t
            comment = f" Disc wear:0 \n Pad wear:0 \n Latateral move.:{-abs(L_L)}"

        else:
            y_max_with_N1 = y_up_N1 - self.WPHB - G_W / 2
            comment = f" Disc wear:0 \n Maximum Pad wear \n Latateral move.:{abs(L_L)}"

        yyt_disc_wear = (G - Lb + 2 * self.disc_wear) / 2 + L_0

        y_low_t_N2 = yyt_disc_wear - abs(L_L) + CR
        y_up_N2 = (G + G_W - Lb) / 2 + L_0 + abs(L_L) + D_w + CR

        y_max_N2 = max(abs(y_low_t_N2), abs(y_up_N2))

        D_w_l_w_max = xxt - (RR ** 2 - y_max_N2 ** 2) ** 0.5

        if y_max_N2 == abs(y_low_t_N2):
            y_max_with_N2 = y_low_t_N2
            comment = f" Maximum Disc wear \n Pad wear:0 \n Latateral move.:{-abs(L_L)}"

        else:
            y_max_with_N2 = y_up_N2 - self.WPHB - G_W / 2
            comment = f" Maximum Disc wear \n Maximum Pad wear \n Latateral move.:{abs(L_L)}"

        y_low_L0 = yyt + CR
        y_up_L0 = (G + G_W - Lb) / 2 + L_0 + D_w + CR
        y_low_L0_t = y_low_L0

        if y_low_L0 * y_up_L0 > 0:
            y_low_L0 = y_low_L0
        else:
            y_low_L0 = 0

        y_min = min(abs(y_low_L0), abs(y_up_L0))
        y_max = max(abs(y_low_L0_t), abs(y_up_L0))

        D_w_l_min_L0 = xxt - (RR ** 2 - y_min ** 2) ** 0.5
        D_w_l_max_L0 = xxt - (RR ** 2 - y_max ** 2) ** 0.5

        if y_max == abs(y_low_L0_t):
            y_Emax_D = y_low_L0_t
        else:
            y_Emax_D = y_up_L0

        if y_min == abs(y_low_L0):
            y_Emin_D = y_low_L0
        else:
            y_Emin_D = y_up_L0

        HUC = self.HUTC
        HLP = self.HLPC
        HLI = self.HTL
        HZR = HUC
        HBM = 2 * self.BFH + 2 * self.Pad_thickness + self.Disc_Width + 2 * CR
        HX = self.DHB

        HZ0 = (HLI ** 2 - ((HBM - HX) / 2) ** 2) ** 0.5 + HLP

        Delta_Z = HZR - HZ0

        HZ0 = (HLI ** 2 - ((HBM - HX) / 2) ** 2) ** 0.5

        HZ = (HLI ** 2 - ((HBM - HX) / 2 + yyt - y_max_with) ** 2) ** 0.5

        Delta_Zmax = HZ0 - HZ

        HZ = (HLI ** 2 - ((HBM - HX) / 2 + yyt - y_min_with) ** 2) ** 0.5

        Delta_Zmin = HZ0 - HZ

        HZ_N1 = (HLI ** 2 - ((HBM - HX) / 2 + yyt - y_max_with_N1) ** 2) ** 0.5
        Delta_Z_D_min = HZ0 - HZ_N1
        HZ_N2 = (HLI ** 2 - ((HBM - HX) / 2 + yyt - y_max_with_N2) ** 2) ** 0.5
        Delta_Z_D_max = HZ0 - HZ_N2

        return TransferResult(
            G=G,
            R=round(RR, 2),
            E_other=E_other,
            D_w_l_min=D_w_l_min,
            D_w_l_max=D_w_l_max,
            Delta_Z=Delta_Z,
            Delta_Zmax=Delta_Zmax,
            Delta_Zmin=Delta_Zmin,
            D_w_l_min_L0=D_w_l_min_L0,
            D_w_l_max_L0=D_w_l_max_L0,
            D_w_l_w_min=D_w_l_w_min,
            D_w_l_w_max=D_w_l_w_max,
            Delta_Z_D_min=Delta_Z_D_min,
            Delta_Z_D_max=Delta_Z_D_max,
            comment=comment
        )

    def transfer_list_instant(self, y_move_instant, disc_wear_instant, pad_wear_instant, WLB_instant, WPHB_instant):
        G30 = self.Disc_Width + 2 * (self.Pad_thickness + self.PHH + self.clearance)
        G = self.DCY + self.PAC + (self.Lever_length - self.LLF) / self.Lever_length * (
                G30 - (self.DCY + self.PAC)) + 2 * self.Offset_Lever
        RR = ((self.LLF) ** 2 + (self.Offset_Lever) ** 2) ** 0.5
        L_0 = self.y_offset
        L_L_instant = y_move_instant
        G_W_instant = WLB_instant
        D_w_instant = pad_wear_instant + disc_wear_instant + WPHB_instant
        Lb = G30
        CR = self.clearance

        yyt = (G - Lb) / 2 + L_0
        xxt = (RR ** 2 - yyt ** 2) ** 0.5

        y_instant = (G + G_W_instant - Lb) / 2 + L_0 - L_L_instant + D_w_instant + CR
        D_w_l_Instant = xxt - (RR ** 2 - y_instant ** 2) ** 0.5

        HUC = self.HUTC
        HLP = self.HLPC
        HLI = self.HTL
        HZR = HUC
        HBM = 2 * self.BFH + 2 * self.Pad_thickness + self.Disc_Width + 2 * CR
        HX = self.DHB

        HZ0 = (HLI ** 2 - ((HBM - HX) / 2) ** 2) ** 0.5 + HLP

        Delta_Z = HZR - HZ0

        HZ0 = (HLI ** 2 - ((HBM - HX) / 2) ** 2) ** 0.5

        HZ = (HLI ** 2 - ((HBM - HX) / 2 + L_L_instant - D_w_instant - CR + WPHB_instant) ** 2) ** 0.5

        Delta_Z_Instant = HZ0 - HZ

        return TransferInstantResult(
            Delta_Z=Delta_Z,
            D_w_l_Instant=D_w_l_Instant,
            Delta_Z_Instant=Delta_Z_Instant
        )

class CompactActCalculator(BXActCalculatorBase):
    def __init__(self, E, angle, Pad_thickness, clearance, y_offset, Disc_Width, y_move,
                 disc_wear, pad_wear, LL, LR, LR1,
                     LR2, D1, D2, D3, H1, H2, H3,Side):
        super().__init__(E, angle, Pad_thickness, clearance, y_offset, Disc_Width, y_move,
                     disc_wear, pad_wear)
        self.LL = LL
        self.LR = LR
        self.LR1 = LR1
        self.LR2 = LR2
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.H1 = H1
        self.H2 = H2
        self.H3 = H3
        self.Side = Side

    @property
    def transfer_list(self):
        E = self.E
        LL = self.LL
        LR = self.LR
        LR1 = self.LR1
        LR2 = self.LR2
        D1 = self.D1
        D2 = self.D2
        D3 = self.D3
        H1 = self.H1
        H2 = self.H2
        H3 = self.H3
        C = self.clearance
        disc_wear = self.disc_wear
        L_0 = self.y_offset
        L_L = -1 * self.y_move
        D_w = disc_wear + self.pad_wear
        Side = self.Side

        if Side == 1:
            yyt = LR + ((LR2) ** 2 - (LR1) ** 2) ** 0.5 - C - H3 / 2 - H1 - H2 + L_0
            yyt_other = LL - C - H3 / 2 - H1 - H2 - L_0
        else:
            yyt = LL - C - H3 / 2 - H1 - H2 + L_0
            yyt_other = LR + ((LR2) ** 2 - (LR1) ** 2) ** 0.5 - C - H3 / 2 - H1 - H2 - L_0
        y_0 = yyt
        xxt = ((D1) ** 2 - (yyt) ** 2) ** 0.5
        xxt_other = ((D1) ** 2 - (yyt_other) ** 2) ** 0.5
        E_other = round(E + xxt - xxt_other, 2)
        RR = D1
        CR = C
        # '===============================
        # 'D_w_l_min, D_w_l_max
        # '===============================
        y_low = yyt - abs(L_L) + CR
        y_up = yyt + abs(L_L) + D_w + CR
        y_low_t = y_low
        if y_low * y_up > 0:
            y_low = y_low
        else:
            y_low = 0

        y_min = min(abs(y_low), abs(y_up))
        y_max = max(abs(y_low_t), abs(y_up))

        if y_max == abs(y_low_t):
            y_Emax = y_low_t
        else:
            y_Emax = y_up

        if y_min == abs(y_low):
            y_Emin = y_low
        else:
            y_Emin = y_up

        D_w_l_min = xxt - (RR ** 2 - y_min ** 2) ** 0.5
        D_w_l_max = xxt - (RR ** 2 - y_max ** 2) ** 0.5

        # 'NEW
        # '===============================
        # 'NEW                 D_w_l_w_min, D_w_l_w_max
        # '===============================
        # 'NEW
        y_up_N1 = y_up - disc_wear
        y_max_N1 = max(abs(y_low_t), abs(y_up_N1))
        D_w_l_w_min = xxt - (RR ** 2 - y_max_N1 ** 2) ** 0.5

        if y_max_N1 == abs(y_low_t):
            # y_max_with_N1 = y_low_t
            comment = f" Disc wear:0 \n Pad wear:0 \n Latateral move.:{-abs(L_L)}"

        else:
            # y_max_with_N1 = y_up_N1 - self.WPHB - G_W / 2
            comment = f" Disc wear:0 \n Maximum Pad wear \n Latateral move.:{abs(L_L)}"

        yyt_disc_wear = yyt + disc_wear
        y_low_t_N2 = yyt_disc_wear - abs(L_L) + CR
        y_up_N2 = y_up
        y_max_N2 = max(abs(y_low_t_N2), abs(y_up_N2))
        D_w_l_w_max = xxt - (RR ** 2 - y_max_N2 ** 2) ** 0.5

        if y_max_N2 == abs(y_low_t_N2):
            # y_max_with_N2 = y_low_t_N2
            comment = f" Maximum Disc wear \n Pad wear:0 \n Latateral move.:{-abs(L_L)}"
        else:
            comment = f" Maximum Disc wear \n Maximum Pad wear \n Latateral move.:{abs(L_L)}"

        y_low_L0 = yyt + CR
        y_up_L0 = yyt + D_w + CR
        y_low_L0_t = y_low_L0

        if y_low_L0 * y_up_L0 > 0:
            y_low_L0 = y_low_L0
        else:
            y_low_L0 = 0

        y_min = min(abs(y_low_L0), abs(y_up_L0))
        y_max = max(abs(y_low_L0_t), abs(y_up_L0))

        D_w_l_min_L0 = xxt - (RR ** 2 - y_min ** 2) ** 0.5
        D_w_l_max_L0 = xxt - (RR ** 2 - y_max ** 2) ** 0.5

        if y_max == abs(y_low_L0_t):
            y_Emax_D = y_low_L0_t
        else:
            y_Emax_D = y_up_L0

        if y_min == abs(y_low_L0):
            y_Emin_D = y_low_L0
        else:
            y_Emin_D = y_up_L0

        Delta_Z = 0
        Delta_Zmax = 0
        Delta_Zmin = 0
        Delta_Z_D_min = 0
        Delta_Z_D_max = 0

        return TransferResult(
            G=0,
            R=round(RR, 2),
            E_other=E_other,
            D_w_l_min=D_w_l_min,
            D_w_l_max=D_w_l_max,
            Delta_Z=Delta_Z,
            Delta_Zmax=Delta_Zmax,
            Delta_Zmin=Delta_Zmin,
            D_w_l_min_L0=D_w_l_min_L0,
            D_w_l_max_L0=D_w_l_max_L0,
            D_w_l_w_min=D_w_l_w_min,
            D_w_l_w_max=D_w_l_w_max,
            Delta_Z_D_min=Delta_Z_D_min,
            Delta_Z_D_max=Delta_Z_D_max,
            comment=comment
        )

    def transfer_list_instant(self, y_move_instant, disc_wear_instant, pad_wear_instant, WLB_instant=0, WPHB_instant=0):
        LR = self.LR
        LR1 = self.LR1
        LR2 = self.LR2
        D1 = self.D1
        D2 = self.D2
        D3 = self.D3
        H1 = self.H1
        H2 = self.H2
        H3 = self.H3
        C = self.clearance
        L_0 = self.y_offset

        Side = self.Side
        L_L_instant = y_move_instant
        D_w_instant = pad_wear_instant + disc_wear_instant

        if Side == 1:
            yyt = LR + ((LR2) ** 2 - (LR1) ** 2) ** 0.5 - C - H3 / 2 - H1 - H2 + L_0
        else:
            yyt = L_L_instant - C - H3 / 2 - H1 - H2 + L_0
        y_0 = yyt
        xxt = ((D1) ** 2 - (yyt) ** 2) ** 0.5
        RR = D1
        CR = C

        y_instant = yyt - L_L_instant + CR + D_w_instant
        D_w_l_Instant = xxt - (RR ** 2 - y_instant ** 2) ** 0.5
        Delta_Z = 0
        Delta_Z_Instant = 0

        return TransferInstantResult(
            Delta_Z=Delta_Z,
            D_w_l_Instant=D_w_l_Instant,
            Delta_Z_Instant=Delta_Z_Instant
        )
