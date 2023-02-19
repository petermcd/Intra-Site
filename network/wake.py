"""Module to facilitate waking devices."""
from wakeonlan import send_magic_packet

from network.models import Device


class Wake:
    """Class to facilitate waking a device."""

    __slots__ = ("_device",)

    def __init__(self, device: Device):
        """
        Initialise Wake.

        Args:
            device: Device to be woken
        """
        self._device = device

    def wake(self) -> bool:
        """Wake the device."""
        if not self._device.wol:
            return self._no_wan()
        if (
            self._device.connected_too
            and self._device.connected_too.model.name.lower() in ["turing pi 2"]
        ):
            return self._wake_turing_node()
        else:
            return self._wake_lan()

    @staticmethod
    def _no_wan() -> bool:
        """
        Return False as device cannot handle WOL.

        Returns: False
        """
        return False

    def _wake_turing_node(self) -> bool:
        """
        Handle powering up a Turing Pi node.

        Returns: True on success otherwise False
        """
        # TODO finalise calling url.
        if not self._device.connected_too:
            return False
        turing_pi_ip: str = self._device.connected_too.ip_address
        turing_pi_port = self._device.port - 1
        url = f"http://{turing_pi_ip}/api/bmc?opt=set&type=power&node{turing_pi_port}=1"
        from urllib import request

        req = request.Request(url=url)
        response = ""
        with request.urlopen(req) as f:
            response += f.read().decode("utf-8")
        return True

    def _wake_lan(self) -> bool:
        """
        Handle wake on lan for a standard device type.

        Returns: True on success otherwise False
        """
        mac_address = str(self._device.mac_address).replace(":", "")
        send_magic_packet(mac_address, ip_address="255.255.255.255", port=8900)
        return True
