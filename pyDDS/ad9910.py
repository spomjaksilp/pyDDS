import numpy as np
from .dds import DDSCore, DDSChannel


class AD9910Core(DDSCore):
    """
    Core device for Analog Devices 9910 (1Gs/s, 14bit dac resolution).
    """

    FTW_WIDTH = 32
    POW_WIDTH = 16
    ASF_WIDTH = 14

    def init_dds(self,
                 refclk,
                 divider_bypass=False,
                 pll_enable=False,
                 pll_n=None,
                 pll_pfd_input_doubler=None,
                 ):
        pass
