"""Module to facilitate waking devices."""
from ipaddress import IPv4Address

from bmc.cluster import Cluster
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
        if not self._device.connected_too:
            return False
        cluster = Cluster(
            cluster_ip=IPv4Address(self._device.connected_too.ip_address),
            username="root",
            password="turing",
            verify=False,
        )
        nodes = cluster.nodes
        node = nodes[int(self._device.port) - 1]
        return cluster.start_nodes(nodes=[node])

    def _wake_lan(self) -> bool:
        """
        Handle wake on lan for a standard device type.

        Returns: True on success otherwise False
        """
        mac_address = str(self._device.mac_address).replace(":", "")
        send_magic_packet(mac_address, ip_address="255.255.255.255", port=8900)
        return True
