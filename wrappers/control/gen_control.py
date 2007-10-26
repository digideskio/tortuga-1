# Copyright (C) 2007 Maryland Robotics Club
# Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:  wrappers/control/gen_control.py

import os

def generate(local_ns, global_ns):

    # Include controller classes
    IController = local_ns.class_('IController')
    IController.include()
    IController.include_files.append(os.environ['RAM_SVN_DIR'] + '/packages/control/include/IController.h')

