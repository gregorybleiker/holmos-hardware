# -*- coding: utf-8 -*-
"""
Created on 16.01.2019

@author: beckmann

Demo of how all parts go together
"""
import os

from solid import *
import Holmos
import lens_mounts
import mirror_mount
import base


class HolmosComponent:
    part_func = None
    z_above_cam = None
    name = None

    def __init__(self, z, part_func, name=None, **kwargs):
        self.part_func = part_func
        self.z = z
        self.name = name
        self.kwargs = kwargs  # keyword arguments for part_func


part_list = (HolmosComponent(-35, Holmos.cage_base_plate),
             HolmosComponent(50, Holmos.rpi_mount),
             HolmosComponent(0, Holmos.rpi_cam_mount),
             HolmosComponent(185, lens_mounts.round_mount_light, inner_diam=20, opening_angle=None, stop_inner_diam=19,
                             name="objective_lens_mount"),
             HolmosComponent(216, Holmos.slide_holder),
             HolmosComponent(252, Holmos.slide_holder, angle_deg=45,
                             name="beamsplitter_mount"),
             HolmosComponent(275, mirror_mount.crane_mirror),
             HolmosComponent(306, lens_mounts.round_mount_light, inner_diam=25.4, opening_angle=None, stop_inner_diam=23.4,
                             name="condensor_lens_mount"),
             HolmosComponent(500, Holmos.cage_stabilizer),
             HolmosComponent(550, lens_mounts.round_mount_light, inner_diam=12, opening_angle=None,
                             name="laser_mount")
             )


def holmos_full_assembly():
    z0 = 30
    h = 600

    assembly = translate((15, -25, h/2))(cylinder(d=6, h=h, center=True))
    for component in part_list:
        this_part = component.part_func(assemble=True, **component.kwargs)
        assembly += translate((0, 0, z0+component.z))(this_part)
    return assembly


if __name__ == '__main__':

    _fine = True
    if _fine:
        header = "$fa = 5;"  # minimum face angle
        header += "$fs = 0.1;"  # minimum face size
    else:
        header = ""

    if not os.path.exists("scad"):
        os.mkdir("scad")

    scad_render_to_file(holmos_full_assembly(), "scad/full_assembly.scad", file_header=header)

    if not os.path.exists("scad/complete_setup"):
        os.mkdir("scad/complete_setup")

    print("cleaning output dirs...")
    for file in os.listdir("scad/complete_setup"):
        os.remove(os.path.join("scad/complete_setup", file))

    for number, part in enumerate(part_list):
        name = part.name
        if name is None:
            name = part.part_func.__name__
        filename = "{:02d} - {}.scad".format(number, name)
        print(filename)
        part_scad = part.part_func(assemble=False, **part.kwargs)
        scad_render_to_file(part_scad, os.path.join("scad/complete_setup/", filename), file_header=header)
