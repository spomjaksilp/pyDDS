import numpy as np
from .connectors import Connector


class DDSCore:
    """
    Direct Digital Synthesis (DDS) driver.
    Manages all channels.
    :param sysclk: (int) DDS system clock
    """

    # tuning word widths for helper functions
    FTW_WIDTH = None  # 32
    POW_WIDTH = None  # 16
    ASF_WIDTH = None  # AD9914: 12  AD9910:14

    # connector object
    _connector = None

    def __init__(self, sysclk, connector):
        assert (self.FTW_WIDTH and self.POW_WIDTH and self.ASF_WIDTH) is not None, "tuning word widths have to be set!"
        assert type(sysclk) is float, "sysclk frequency has to be float"
        self.f_sysclk = sysclk

        assert isinstance(connector, Connector)
        self._connector = connector

    def init_dds(self):
        raise NotImplementedError

    # low level io
    def _write(self, location, data):
        """
        Write method just uses the connector.
        :param location:
        :param data:
        :return:
        """
        self._connector.write(location=location, data=data)

    def _read(self, location, width):
        """
        Read method just uses the connector.
        :param location:
        :param width:
        :return:
        """
        return self._connector.read(location=location, width=width)

    def _read_all(self):
        """
        Read_all method just uses the connector.
        :return:
        """
        return self._connector.read_all()

    # basic operations
    def reset(self):
        """
        Reset DDS device.
        :return:
        """
        raise NotImplementedError

    def update_io(self):
        """
        Trigger IO update.
        :return:
        """
        raise NotImplementedError

    def set_drhold(self, value):
        """
        Pause the digital ramp generator.
        :param value: (bool) True=hold, False=unhold
        :return:
        """
        raise NotImplementedError

    # general device configuration
    def set_refclk(self, refclk):
        """
        Set the reference clock value.
        :param refclk:
        :return:
        """
        raise NotImplementedError

    def set_pll(self, *args, **kwargs):
        """
        Configure the phase locking loop.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def set_sine_ouput(self, value=False):
        """
        Confugure sine (True) or cosine (False, default) output.
        :param value:
        :return:
        """
        raise NotImplementedError


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


class DDSChannel:
    """
    Manages a single channel, to be used in conjunction with DDSCore.
    """

    # every channel has to be attached to a core device
    _core = None

    def __init__(self, core):
        assert isinstance(core, DDSCore), "core parameter must be DDSCore instance or instance of an inherited class"
        self._core = core

    def __del__(self):
        raise NotImplementedError

    def set_singletone(self, frequency, phase, amplitude, profile):
        raise NotImplementedError

    def set_frequency_sweep(self, *args, **kwargs):
        raise NotImplementedError

    def set_amplitude_sweep(self, *args, **kwargs):
        raise NotImplementedError
