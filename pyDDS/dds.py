import numpy as np


class DDSGroup:
    """Core device Direct Digital Synthesis (DDS) driver.

    Gives access to the DDS functionality of the core device.

    :param sysclk: (int) DDS system clock
    """

    FTW_WIDTH = None  # 32
    POW_WIDTH = None  # 16
    ASF_WIDTH = None  # AD9914: 12  AD9910:14

    def __init__(self, sysclk):
        assert (self.FTW_WIDTH and self.POW_WIDTH and self.ASF_WIDTH) is not None, "tuning word widths have to be set!"
        assert type(sysclk) is float, "sysclk frequency has to be float"
        self.f_sysclk = sysclk

    # helpers
    @staticmethod
    def _ensure_number(value):
        """
        Makes sure that a number is returned.
        :param value: (bytes or float or int) value which should be returned as a number
        :return: (float or int) the converted value
        """
        assert type(value) in [bytes, float, np.float64, int], "value has to be either bytes or float or int"

        return int.from_bytes(value, byteorder="big") if type(value) is bytes else value

    @staticmethod
    def _ensure_bytes(value, width=None):
        """
        Makes sure that a byte object is returned. If a byte object is given, the width is checked.
        :param value: (bytes or float or int) value which should be returned as bytes
        :param width: (int) width of the tuning word. E.g. 32 bit for the frequency tuning word
        :return: (bytes) the converted value
        """
        assert width is not None and type(width) is int, "tuning word width has to be set as integer"
        assert type(value) in [bytes, float, np.float64, int], "value has to be either bytes or float or int"
        if type(value) is bytes:
            assert len(value) == width, "width of value does not match target width"

        return int(round(value)).to_bytes(width, byteorder="big") if type(value) in [float, np.float64, int] else value

    def frequency_to_ftw(self, frequency):
        """Returns the frequency tuning word corresponding to the given
        frequency.
        :param frequency: (float) frequency [Hz]
        """
        ftw = round(2**self.FTW_WIDTH * self._ensure_number(frequency) / self.f_sysclk)
        return self._ensure_bytes(ftw, self.FTW_WIDTH)

    def ftw_to_frequency(self, ftw):
        """Returns the frequency corresponding to the given frequency tuning
        word.
        :param ftw: (bytes) frequency tuning word
        """
        return self._ensure_number(ftw) * self.f_sysclk / 2**self.FTW_WIDTH

    def phase_to_pow(self, phi):
        """Returns the phase offset word corresponding to the given phase
        in radians.
        :param phi: (float) phase offset angle [radians]
        """
        pow = round(self._ensure_number(phi) / (2 * np.pi) * 2 ** self.POW_WIDTH)
        return self._ensure_bytes(pow, self.POW_WIDTH)

    def pow_to_phase(self, pow):
        """Returns the phase in radians corresponding to the given phase offset
        word.
        :param pow: (bytes) phase offset word
        """
        return 2 * np.pi * self._ensure_number(pow) / 2**self.POW_WIDTH

    def amplitude_to_asf(self, amplitude):
        """Returns amplitude scale factor corresponding to given amplitude.
        :param amplitude: (float) amplitude in dB to full scale
        """
        asf = round(np.power(10, self._ensure_number(amplitude) / 20) * 2 ** self.ASF_WIDTH)
        return self._ensure_bytes(asf, self.ASF_WIDTH)

    def asf_to_amplitude(self, asf):
        """
        Returns the relative amplitude corresponding to the given amplitude scale
        factor in dB to full scale.
        :param asf: (bytes) amplitude scale factor
        """
        return 20 * np.log10(self._ensure_number(asf) / 2 ** self.ASF_WIDTH)
