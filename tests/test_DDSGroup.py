import pyDDS
import numpy as np
import pytest


# dummy classes
class WrongInheritedDDS(pyDDS.DDSGroup):
    pass


class AD9914(pyDDS.DDSGroup):
    FTW_WIDTH = 32
    POW_WIDTH = 16
    ASF_WIDTH = 12


# actual tests
class TestHelperFunctions:

    dds = AD9914(sysclk=3.5e9)

    ftw = (2 ** 12).to_bytes(32, byteorder="big")
    f = 3337.860107421875

    pow = round(1/4*2**16).to_bytes(16, byteorder="big")
    phase = np.pi/2

    asf = int(round(np.power(10, (-3.0/20))*2**12)).to_bytes(12, byteorder="big")
    amp = -3

    def test_ftw_to_f(self):
        assert self.dds.ftw_to_frequency(ftw=self.ftw) == self.f

    def test_f_to_ftw(self):
        assert self.dds.frequency_to_ftw(frequency=self.f) == self.ftw

    def test_pow_to_phase(self):
        assert self.dds.pow_to_phase(pow=self.pow) == self.phase

    def test_phase_to_pow(self):
        assert self.dds.phase_to_pow(phi=self.phase) == self.pow

    def test_asf_to_amp(self):
        assert self.dds.asf_to_amplitude(asf=self.asf) == self.amp

    def test_amp_to_asf(self):
        assert self.dds.amplitude_to_asf(amplitude=self.amp) == self.asf


class TestWrongInheritance:
    @staticmethod
    def test_wrong_inheritance():
        with pytest.raises(AssertionError):
            dds = WrongInheritedDDS(sysclk=3.6e9)
