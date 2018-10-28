#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2017 Open Path View
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# Contributors: Benjamin BERNARD
# Email: benjamin.bernard@openpathview.fr
# Description: Panorama with campains and sensors informations.

from opv_api_client.relationship import Relationship
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import register, RessourceProxy

@register
class PanoramaSensors(Ressource):
    _api_version = "v1"
    _name = "panorama_sensors"
    _primary_keys = ("id_panorama", "id_malette")

    class _rel:
        pass
