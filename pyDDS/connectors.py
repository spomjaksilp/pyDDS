class Connector:
    """
    Scaffold class for the connections interface.
    """

    def __init__(self):
        pass

    def read(self, location, width):
        """
        Read (width) bits at location and return them as bytes.
        :param location:
        :param width:
        :return:
        """
        raise NotImplementedError

    def read_all(self):
        """
        Read all registers and return them as bytes.
        :return:
        """
        raise NotImplementedError

    def write(self, location, data):
        """
        Write data to location.
        :param location:
        :param data:
        :return:
        """
        raise NotImplementedError

    def reset_device(self):
        """
        Reset the connected DDS.
        :return:
        """
        raise NotImplementedError

    def update_io(self):
        """
        Update the io (pin)
        :return:
        """
        raise NotImplementedError

    def set_drhold(self, value):
        """
        Pause (True) or unpause (False) the digital ramp generator.
        :param value:
        :return:
        """
        raise NotImplementedError