#!/usr/bin/env python3
import em
import sys
import os


em_file_path = sys.argv[1]

no_em_extension_path = os.path.splitext(em_file_path)[0]
no_extension_path = os.path.splitext(no_em_extension_path)[0]
extension = os.path.splitext(no_em_extension_path)[1]

for arm in [True, False]:
    if arm:
        end_effectors = ["pal-hey5", "pal-gripper", "schunk-wsg", "robotiq-2f-85", "robotiq-2f-140", "custom", "no-ee"]
        ft_sensors = ["schunk-ft", None]
    else:
        end_effectors = [None]
        ft_sensors = [None]
    for end_effector in end_effectors:
        for ft_sensor in ft_sensors:
            cfg = {
                "has_arm": arm,
                "end_effector": end_effector,
                "ft_sensor": ft_sensor,
            }
            with open(em_file_path, "r") as f:
                expanded_contents = em.expand(f.read(), cfg)
            if not arm:
                suffix = "_no-arm"
            elif ft_sensor is None:
                suffix = "_{}".format(end_effector)
            else:
                suffix = "_{}_{}".format(end_effector, ft_sensor)
            expanded_file_name = no_extension_path + suffix + extension
            with open(expanded_file_name, "w") as f:
                msg = "Autogenerated file, don't edit this, edit {} instead".format(
                    os.path.basename(em_file_path))
                if extension == ".yaml":
                    f.write("#" + msg + "\n")
                # If we add a comment at the begining of an xml the format is not correct.
                #elif extension in [".xacro", ".xml", ".srdf"]:
                #    f.write("<!-- " + msg + "-->\n")

                f.write(expanded_contents)
            print("Generated " + expanded_file_name)
