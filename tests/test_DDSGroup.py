import pyDDS
import pytest


class Wrong_inherited_DDS(pyDDS.DDSGroup):
    pass


def test_wrong_inheritance():
    with pytest.raises(AssertionError):
        dds = Wrong_inherited_DDS(sysclk=3.6e9)


class AD9914(pyDDS.DDSGroup):
    FTW_WIDTH = 32
    POW_WIDTH = 16
    ASF_WIDTH = 12


class Test_helper_functions:

    dds = AD9914(sysclk=3.5e9)

    ftw = (2 ** 12).to_bytes(32, byteorder="big")
    f = 3337.860107421875

    def test_ftw_to_f_kwargs(self):
        assert self.dds.ftw_to_frequency(ftw=self.ftw) == self.f

    def test_f_to_ftw_kwargs(self):
        assert self.dds.frequency_to_ftw(frequency=self.f) == self.ftw

