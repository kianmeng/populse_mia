# -*- coding: utf-8 -*-
"""Define software version, description and requirements

:Contains:
    :Function:
        - get_populse_mia_gitversion

"""

###############################################################################
# Populse_mia - Copyright (C) IRMaGe/CEA, 2018
# Distributed under the terms of the CeCILL license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html
# for details.
###############################################################################

import os
import subprocess
import sys

# Current version
version_major = 2
version_minor = 3
version_micro = 1
version_extra = "dev"  # leave empty for release
# version_extra = ""

# Expected by setup.py: string of form "X.Y.Z"
if version_extra:
    __version__ = "{0}.{1}.{2}-{3}".format(
        version_major, version_minor, version_micro, version_extra
    )

else:
    __version__ = "{0}.{1}.{2}".format(
        version_major, version_minor, version_micro
    )


def get_populse_mia_gitversion():
    """Mia version as reported by the last commit in git

    :returns: the version or None if nothing was found
    """

    try:
        import populse_mia

        dir_mia = os.path.realpath(
            os.path.join(
                os.path.dirname(populse_mia.__file__),
                os.path.pardir,
                os.path.pardir,
            )
        )

    except Exception:
        dir_mia = os.getcwd()

    dir_miagit = os.path.join(dir_mia, ".git")

    if not os.path.exists(dir_miagit):
        return None

    ver = None

    try:
        gitversion, _ = subprocess.Popen(
            "git show -s --format=%h",
            shell=True,
            cwd=dir_mia,
            stdout=subprocess.PIPE,
        ).communicate()

    except Exception:
        pass

    else:
        ver = gitversion.decode().strip().split("-")[-1]

    return ver


if __version__.endswith("-dev"):
    gitversion = get_populse_mia_gitversion()

    if gitversion:
        __version__ = "{0}+{1}".format(__version__, gitversion)

# Expected by setup.py: the status of the project
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: CEA CNRS Inria "
    "Logiciel Libre License, version 2.1 (CeCILL-2.1)",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering",
    "Topic :: Utilities",
]

# project descriptions
DESCRIPTION = "populse mia"
LONG_DESCRIPTION = """
===============
populse_mia
===============
[MIA] Multi parametric Image Analysis:
A complete image processing environment mainly targeted at
the analysis and visualization of large amounts of MRI data
"""

# Other values used in setup.py
NAME = "populse_mia"
ORGANISATION = "populse"
MAINTAINER = "Populse team"
MAINTAINER_EMAIL = "populse-support@univ-grenoble-alpes.fr"
AUTHOR = "Populse team"
AUTHOR_EMAIL = "populse-support@univ-grenoble-alpes.fr"
URL = "http://populse.github.io/populse_mia"
DOWNLOAD_URL = "http://populse.github.io/populse_mia"
LICENSE = "CeCILL"
VERSION = __version__
CLASSIFIERS = CLASSIFIERS
PLATFORMS = "OS Independent"

REQUIRES = [
    "capsul",
    "cryptography",
    "jinja2 == 2.8.1",
    "lark-parser >= 0.7.0, < 1.0.0",
    "matplotlib",
    "mia-processes >= 2.2.0",
    "nibabel",
    "nipype",
    "pillow",
    "populse-db >= 2.1.0",
    "pre-commit",
    "pyqt5",
    "python-dateutil",
    "pyyaml",
    "scikit-image",
    "scipy",
    "snakeviz",
    "soma_workflow",
    "six >= 1.13",
    "traits",  # Remove '==5.2.0' when capsul get a new release
    # (> 2.2.1)
]

EXTRA_REQUIRES = {
    "doc": [
        "sphinx>=1.0",
    ],
}

brainvisa_build_model = "pure_python"

# tests to run
test_commands = ["%s -m populse_mia.test" % sys.executable]