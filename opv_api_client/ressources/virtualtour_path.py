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

# Contributors: Simon Archieri
# Email: simon.archieri@openpathview.fr
# Description: Represent Path API ressource.

from opv_api_client.relationship import Relationship
from opv_api_client.ressource import Ressource
from opv_api_client.ressource_list import register, RessourceProxy

@register
class Virtualtour_path(Ressource):
    _api_version = "v1"
    _name = "virtualtour_path"
    _primary_keys = ("id_virtualtour_path", "id_malette")

    class _rel:
        path_details = Relationship(RessourceProxy("path_details"))
        virtualtour = Relationship(RessourceProxy("virtualtour"))
