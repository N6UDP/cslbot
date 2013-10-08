# Copyright (C) 2013 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek, James Forcier and Reed Koser
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from helpers.command import Command


@Command('cidr', [])
def cmd(send, msg, args):
    """Gets a CIDR range.
    Syntax: !cidr <range>
    """
    ip = msg.split('/')
    if len(ip) != 2:
        send("Not a valid CIDR range.")
        return
    # Get address string and CIDR string from command line
    (addrString, cidrString) = ip

    # Split address into octets and turn CIDR into int
    addr = [int(x) for x in addrString.split('.')]
    for x in addr:
        if x > 255 or x < 0:
            send("Invalid IP.")
            return
    cidr = int(cidrString)
    if cidr < 0 or cidr > 32:
        send("Invalid CIDR mask.")
        return

    # Initialize the netmask and calculate based on CIDR mask
    mask = [0, 0, 0, 0]
    for i in range(cidr):
        mask[i // 8] = mask[i // 8] + (1 << (7 - i % 8))

    # Initialize net and binary and netmask with addr to get network
    net = []
    for i in range(4):
        net.append(addr[i] & mask[i])

    # Duplicate net into broad array, gather host bits, and generate broadcast
    broad = list(net)
    brange = 32 - cidr
    for i in range(brange):
        broad[3 - i // 8] = broad[3 - i // 8] + (1 << (i % 8))

    # Print information, mapping integer lists to strings for easy printing
    send("%s-%s" % (".".join(map(str, net)), ".".join(map(str, broad))))