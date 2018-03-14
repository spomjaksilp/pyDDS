import numpy as np


class DDSGroup:
    """Core device Direct Digital Synthesis (DDS) driver.

    Gives access to the DDS functionality of the core device.

    :param sysclk: (int) DDS system clock
    """

    FTW_WIDTH = None  # 32
    POW_WIDTH = None  # 16
    ASF_WIDTH = None  # AD9914: 12  AD9912:14

    def __init__(self, sysclk):
        assert (self.FTW_WIDTH and self.POW_WIDTH and self.ASF_WIDTH) is not None, "tuning word widths have to be set!"
        self.f_sysclk = sysclk

    @staticmethod
    def from_bytes(func):
        def wrapper(*args, **kwargs):
            instance, *actual_args = args
            new_args = [int.from_bytes(x, byteorder="big") for x in actual_args]
            # empty dicts evaluate to false, if kwargs is empty, just pass to old one
            new_kwargs = {key: int.from_bytes(value, byteorder="big") for key, value in
                          kwargs.items()} if kwargs else kwargs
            return func(instance, *new_args, **new_kwargs)

        return wrapper

    @staticmethod
    def to_bytes(width):
        def actual_decorator(func):
            def wrapper(*args, **kwargs):
                result_int = func(*args, **kwargs)
                result_bytes = result_int.to_bytes(width, byteorder="big")
                return result_bytes

            return wrapper

        return actual_decorator

    @to_bytes(FTW_WIDTH)
    def frequency_to_ftw(self, frequency):
        """Returns the frequency tuning word corresponding to the given
        frequency.
        :param frequency: (float) frequency [Hz]
        """
        return round(2**self.FTW_WIDTH * frequency / self.f_sysclk)

    @from_bytes
    def ftw_to_frequency(self, ftw):
        """Returns the frequency corresponding to the given frequency tuning
        word.
        :param ftw: (bytes) frequency tuning word
        """
        return ftw * self.f_sysclk / 2**self.FTW_WIDTH

    @to_bytes(POW_WIDTH)
    def turns_to_pow(self, phi):
        """Returns the phase offset word corresponding to the given phase
        in radians.
        :param phi: (float) phase offset angle [radians]
        """
        return round(phi * 2 ** self.POW_WIDTH)

    @from_bytes
    def pow_to_turns(self, pow):
        """Returns the phase in radians corresponding to the given phase offset
        word.
        :param pow: (bytes) phase offset word
        """
        return 2 * np.pi * pow / 2**self.POW_WIDTH

    @to_bytes(ASF_WIDTH)
    def amplitude_to_asf(self, amplitude):
        """Returns amplitude scale factor corresponding to given amplitude.
        :param amplitude: (float) amplitude in dB to full scale
        """
        return round(np.power(amplitude / 20, 10) * self.ASF_WIDTH)

    @from_bytes
    def asf_to_amplitude(self, asf):
        """
        Returns the relative amplitude corresponding to the given amplitude scale
        factor in dB to full scale.
        :param asf: (bytes) amplitude scale factor
        """
        return 20 * np.log10(asf / self.ASF_WIDTH)
