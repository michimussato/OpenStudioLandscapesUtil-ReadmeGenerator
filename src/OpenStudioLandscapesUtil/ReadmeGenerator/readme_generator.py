"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = ReadmeGenerator.readme_generator:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

# Todo:
#  - [ ] This is just a quick and dirty implementation for now.

import argparse
import logging
import pathlib
import tomllib
from typing import Union, List

import sys
import importlib
import textwrap
import snakemd

from OpenStudioLandscapesUtil.ReadmeGenerator import __version__

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


class ReadmeGeneratorError(Exception):
    pass


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from OpenStudioLandscapesUtil.ReadmeGenerator.readme_generator import fib`,
# when using this Python module as a library.


def generate_readme(
        versions: list[str],
):
    """Entry point to generate the Readme file
    for a given OpenStudioLandscapes Feature
    taking Python versions as argument

    Args:
      versions: list of versions

    Returns:
      str: Path to README.md file
    """

    with open("pyproject.toml", "rb") as f:
        toml_dict = tomllib.load(f)

    if toml_dict["project"]["name"] == "OpenStudioLandscapes":
        raise ReadmeGeneratorError("ReadmeGenerator is not built to work with OpenStudioLandscapes engine.")

    # toml_dict["tool"]["setuptools"]["packages"] will contain
    # something like: ["OpenStudioLandscapes.Ayon"]
    namespace, package = toml_dict["tool"]["setuptools"]["packages"][0].split(".")

    _logger.debug(f"{namespace = }")
    _logger.debug(f"{package = }")

    try:
        constants = importlib.import_module(f"{namespace}.{package}.constants")
    except ModuleNotFoundError as e:
        _logger.exception(f"Module OpenStudioLandscapes not found: {e}")
        raise e

    try:
        readme_feature = importlib.import_module(f"{namespace}.{package}.readme_feature")
    except ImportError:
        readme_feature = None

    readme = _generator(
        constants=constants,
        python_versions=versions,
        readme_feature=readme_feature,
    )

    return readme.as_posix()


def _generator(
        constants,
        python_versions: List[str],
        readme_feature: Union[snakemd.Document, None] = None,
) -> pathlib.Path:

    rel_path = pathlib.Path(constants.__file__)
    parts_ = rel_path.parts

    file_ = parts_[-1]
    module_ = parts_[-2]
    repo_ = parts_[-5]

    gh_prefix = "https://github.com/michimussato/"

    gh_repo = f"{gh_prefix}{repo_}.git"

    gh_path_constants = "/".join([
        repo_,
        "tree",
        "main",
        parts_[-4],
        parts_[-3],
        module_,
        file_
    ])

    gh_path_noxfile = "/".join([
        repo_,
        "tree",
        "main",
        "noxfile.py",
    ])

    gh_path_sbom = "/".join([
        repo_,
        "tree",
        "main",
        ".sbom",
    ])

    doc = snakemd.Document()

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo OpenStudioLandscapes
                """
            ),
            image={
                "OpenStudioLandscapes": "https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png",
            }["OpenStudioLandscapes"],
            link="https://github.com/michimussato/OpenStudioLandscapes",
        ).__str__()
    )

    doc.add_horizontal_rule()

    # TOC

    doc.add_table_of_contents(
        levels=range(1, 4)
    )

    doc.add_horizontal_rule()

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            This `README.md` was dynamically created with 
            [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).
            """
        )
    )

    doc.add_horizontal_rule()

    # Title

    doc.add_heading(
        text=f"Feature: {repo_}",
        level=1,
    )

    ## Brief

    doc.add_heading(
        text="Brief",
        level=2,
    )

    ### Text

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of 
            OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).
            """
        )
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            You feel like writing your own Feature? Go and check out the 
            [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template). 
            """
        )
    )

    ## Requirements

    doc.add_heading(
        text="Requirements",
        level=2,
    )

    doc.add_unordered_list(
        [
            "`python-3.11`",
            "`OpenStudioLandscapes`",
        ]
    )

    ## Install

    doc.add_heading(
        text="Install",
        level=2,
    )

    ### This Feature

    doc.add_heading(
        text="This Feature",
        level=3,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Clone this repository into `OpenStudioLandscapes/.features`:
            """
        )
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            # cd .features
            git clone {gh_repo}
            """
        ),
        lang="shell",
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Create `venv`:
            """
        )
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            # cd .features/{repo_}
            python3.11 -m venv .venv
            source .venv/bin/activate
            python -m pip install --upgrade pip setuptools
            """
        ),
        lang="shell",
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Configure `venv`:
            """
        )
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            # cd .features/{repo_}
            pip install -e "../../[dev]"
            pip install -e ".[dev]"
            """
        ),
        lang="shell",
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            For more info see [VCS Support of pip](https://pip.pypa.io/en/stable/topics/vcs-support/).
            """
        )
    )

    ## Add to OpenStudioLandscapes

    doc.add_heading(
        text="Add to OpenStudioLandscapes",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Add the following code to `OpenStudioLandscapes.engine.features.FEATURES`:
            """
        )
    )

    doc.add_code(
        code=textwrap.dedent(
            """
            FEATURES.update(
                "OpenStudioLandscapes-%s": {
                    "enabled": True|False,
                    # - from ENVIRONMENT VARIABLE (.env):
                    #   "enabled": get_bool_env("ENV_VAR")
                    # - combined:
                    #   "enabled": True|False or get_bool_env(
                    #       "OPENSTUDIOLANDSCAPES__ENABLE_FEATURE_OPENSTUDIOLANDSCAPES_%s"
                    #   )
                    "module": "OpenStudioLandscapes.%s.definitions",
                    "compose_scope": ComposeScope.DEFAULT,
                    "feature_config": OpenStudioLandscapesConfig.DEFAULT,
                }
            )
            """
        ) % (
            str(module_).replace("_", "-").replace(".constants", ""),
            str(module_).replace("-", "_").replace(".constants", "").upper(),
            str(module_).replace(".constants", ""),
        ),  # Todo: a bit hacky
        lang="python",
    )

    ## Testing

    doc.add_heading(
        text="Testing",
        level=2,
    )

    ### pre-commit

    doc.add_heading(
        text="pre-commit",
        level=3,
    )

    doc.add_unordered_list(
        [
            "https://pre-commit.com",
            "https://pre-commit.com/hooks.html",
        ]
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            pre-commit install
            """
        ),
        lang="shell",
    )

    ### nox

    doc.add_heading(
        text="nox",
        level=3,
    )

    #### Generate Report

    doc.add_heading(
        text="Generate Report",
        level=4,
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            nox --no-error-on-missing-interpreters --report .nox/nox-report.json
            """
        ),
        lang="shell",
    )

    #### Re-Generate this README

    doc.add_heading(
        text="Re-Generate this README",
        level=4,
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            nox -v --add-timestamp --session readme
            """
        ),
        lang="shell",
    )

    #### Generate Sphinx Documentation

    doc.add_heading(
        text="Generate Sphinx Documentation",
        level=4,
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            nox -v --add-timestamp --session docs
            """
        ),
        lang="shell",
    )

    #### Pylint

    doc.add_heading(
        text="pylint",
        level=4,
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            nox -v --add-timestamp --session lint
            """
        ),
        lang="shell",
    )

    doc.add_heading(
        text="pylint: disable=redefined-outer-name",
        level=5,
    )

    doc.add_unordered_list(
        [
            "[`W0621`](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/redefined-outer-name.html): Due to Dagsters way of piping arguments into assets.",
        ]
    )

    #### SBOM

    doc.add_heading(
        text="SBOM",
        level=4,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Acronym for Software Bill of Materials
            """
        )
    )

    doc.add_code(
        code=textwrap.dedent(
            f"""
            nox -v --add-timestamp --session sbom
            """
        ),
        lang="shell",
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            We create the following SBOMs:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[`cyclonedx-bom`](https://pypi.org/project/cyclonedx-bom/)",
            "[`pipdeptree`](https://pypi.org/project/pipdeptree/) (Dot)",
            "[`pipdeptree`](https://pypi.org/project/pipdeptree/) (Mermaid)",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            f"""
            SBOMs for the different Python interpreters defined in [`.noxfile.VERSIONS`]({gh_prefix}{gh_path_noxfile}) 
            will be created in the [`.sbom`]({gh_prefix}{gh_path_sbom}) directory of
            this repository.
            """
        )
    )

    doc.add_unordered_list(
        [
            "`cyclone-dx`",
            "`pipdeptree` (Dot)",
            "`pipdeptree` (Mermaid)",
        ]
    )
    doc.add_paragraph(
        text=textwrap.dedent(
            f"""
            Currently, the following Python interpreters are enabled for testing:
            """
        )
    )

    # Todo
    #  - [x] make this dynamic (could be achieved by packaging this up into a CLI and then
    #        call it from nox)
    doc.add_unordered_list(
        sorted([f"`python{i}`" for i in python_versions])
        # [
        #     "`python3.11`",
        #     "`python3.12`",
        # ]
    )

    ## Variables

    doc.add_heading(
        text="Variables",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            f"""
            The following variables are being declared in 
            `OpenStudioLandscapes.{module_}.constants` and are accessible 
            throughout the [`{repo_}`]({gh_prefix}{gh_path_constants}) package.
            """
        )
    )

    header = [
        "Variable",
        "Type"
    ]

    rows = []

    for var in constants.__all__:
        val = constants.__dict__[var]

        rows.append(
            [
                snakemd.Inline(
                    text=var,
                ).code(),
                snakemd.Inline(
                    text=type(val).__name__,
                ).code(),
            ]
        )

    doc.add_table(
        header=header,
        data=rows,
        align=[
            snakemd.Table.Align.LEFT,
            snakemd.Table.Align.LEFT,
        ],
        indent=0,
    )

    ### FEATURE_CONFIGS

    doc.add_heading(
        text="Feature Configs",
        level=3,
    )

    header_environment = [
        "Variable",
        "Type",
        "Value"
    ]

    for k_feature_config, v_feature_config in constants.FEATURE_CONFIGS.items():

        doc.add_heading(
            text=f"Feature Config: {k_feature_config}",
            level=4,
        )

        rows_environment = []

        for k, v in v_feature_config.items():

            rows_environment.append(
                [
                    snakemd.Inline(
                        text=k,
                    ).code(),
                    snakemd.Inline(
                        text=type(v).__name__,
                    ).code(),
                    snakemd.Inline(
                        text=v,
                    ).code(),
                ]
            )

        doc.add_table(
            header=header_environment,
            data=rows_environment,
            align=[
                snakemd.Table.Align.LEFT,
                snakemd.Table.Align.LEFT,
                snakemd.Table.Align.LEFT,
            ],
            indent=0,
        )

    discord = "https://discord.com/channels/1357343453364748419"
    # slack = "https://app.slack.com/client/T08L6M6L0S3"

    community_channels = {
        "OpenStudioLandscapes": {
            "github": {
                "repo_name": "OpenStudioLandscapes",
            },
            "discord": {
                "channel_name": "# openstudiolandscapes-general",
                "channel_id": "1357343454065328202",
                "invite": "https://discord.gg/F6bDRWsHac",
            },
            # "slack": {
            #     "channel_name": "# openstudiolandscapes-general",
            #     "channel_id": "C08LK80NBFF",
            # },
        },
        "OpenStudioLandscapes-Ayon": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Ayon",
            },
            "discord": {
                "channel_name": "# openstudiolandscapes-ayon",
                "channel_id": "1357722468336271411",
                "invite": "https://discord.gg/gd6etWAF3v",
            },
            # "slack": {
            #     "channel_name": "# openstudiolandscapes-ayon",
            #     "channel_id": "C08LLBC7CB0",
            # },
        },
        "OpenStudioLandscapes-Dagster": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Dagster",
            },
            "discord": {
                "channel_name": "# openstudiolandscapes-dagster",
                "channel_id": "1358016764608249856",
                "invite": "https://discord.gg/jwB3DwmKvs",
            },
            # "slack": {
            #     "channel_id": "C08LZR5JFA6",
            #     "channel_name": "# openstudiolandscapes-dagster",
            # },
        },
        "OpenStudioLandscapes-Kitsu": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Kitsu",
            },
            "discord": {
                "channel_name": "# openstudiolandscapes-kitsu",
                "channel_id": "1357638253632688231",
                "invite": "https://discord.gg/6cc6mkReJ7",
            },
            # "slack": {
            #     "channel_name": "# openstudiolandscapes-kitsu",
            #     "channel_id": "C08L6M70ZB9",
            # },
        },
        # "OpenStudioLandscapes-Deadline-10-2": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-Deadline-10-2",
        #     },
        #     "discord": {
        #         "channel_id": "1358017409276973088",
        #         "channel_name": "# openstudiolandscapes-deadline-10-2",
        #         "invite": "https://discord.gg/p2UjxHk4Y3",
        #     },
        #     # "slack": {
        #     #     "channel_id": "C08LZR963A6",
        #     #     "channel_name": "# openstudiolandscapes-deadline-10-2",
        #     # },
        # },
        # "OpenStudioLandscapes-Deadline-10-2-Worker": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-Deadline-10-2-Worker",
        #     },
        #     "discord": {
        #         "channel_id": "1358024594409259059",
        #         "channel_name": "# openstudiolandscapes-deadline-10-2-worker",
        #         "invite": "https://discord.gg/ttkbfkzUmf",
        #     },
        #     # "slack": {
        #     #     "channel_id": "C08LZSBM998",
        #     #     "channel_name": "# openstudiolandscapes-deadline-10-2-worker",
        #     # },
        # },
        # "OpenStudioLandscapes-filebrowser": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-filebrowser",
        #     },
        #     "discord": {
        #         "channel_id": "1364746200175083520",
        #         "channel_name": "# openstudiolandscapes-filebrowser",
        #         "invite": "https://discord.gg/stzNsZBmwk",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "",
        #     # },
        # },
        # "OpenStudioLandscapes-NukeRLM-8": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-NukeRLM-8",
        #     },
        #     "discord": {
        #         "channel_id": "1358017656732782672",
        #         "channel_name": "# openstudiolandscapes-nukerlm-8",
        #         "invite": "https://discord.gg/bMVqrNrMg2",
        #     },
        #     # "slack": {
        #     #     "channel_id": "C08LZDLFTMH",
        #     #     "channel_name": "# openstudiolandscapes-nukerlm-8",
        #     # },
        # },
        # "OpenStudioLandscapes-n8n": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-n8n",
        #     },
        #     "discord": {
        #         "channel_id": "1420384480526602320",
        #         "channel_name": "# openstudiolandscapes-n8n",
        #         "channel_name": "https://discord.gg/zVFJUEaAwK",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "# openstudiolandscapes-n8n",
        #     # },
        # },
        # "OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20",
        #     },
        #     "discord": {
        #         "channel_id": "1358018027190484993",
        #         "channel_name": "# openstudiolandscapes-sesi-gcc-9-3-houdini-20",
        #         "invite": "https://discord.gg/Zwmn3VAMDx",
        #     },
        #     # "slack": {
        #     #     "channel_id": "C08LUTR1WG5",
        #     #     "channel_name": "# openstudiolandscapes-sesi-gcc-9-3-houdini-20",
        #     # },
        # },
        "OpenStudioLandscapes-RustDeskServer": {
            "github": {
                "repo_name": "OpenStudioLandscapes-RustDeskServer",
            },
            "discord": {
                "channel_id": "1414567463227621510",
                "channel_name": "# openstudiolandscapes-rustdeskserver",
                "invite": "https://discord.gg/nJ8Ffd2xY3",
            },
            # "slack": {
            #     "channel_id": "C09E6HA0ZPW",
            #     "channel_name": "# openstudiolandscapes-rustdeskserver",
            # },
        },
        "OpenStudioLandscapes-Teleport": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Teleport",
            },
            "discord": {
                "channel_id": "1420385295026884659",
                "channel_name": "# openstudiolandscapes-teleport",
                "invite": "https://discord.gg/SNMCw5aDfm",
            },
            # "slack": {
            #     "channel_id": "C09E6HA0ZPW",
            #     "channel_name": "# openstudiolandscapes-rustdeskserver",
            # },
        },
        "OpenStudioLandscapes-Twingate": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Twingate",
            },
            "discord": {
                "channel_id": "1414768065174044844",
                "channel_name": "# openstudiolandscapes-twingate",
                "invite": "https://discord.gg/tREYa6UNJf",
            },
            # "slack": {
            #     "channel_id": "C09E6HA0ZPW",
            #     "channel_name": "# openstudiolandscapes-rustdeskserver",
            # },
        },
        # "OpenStudioLandscapes-Syncthing": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-Syncthing",
        #     },
        #     "discord": {
        #         "channel_id": "1364746871381168138",
        #         "channel_name": "# openstudiolandscapes-syncthing",
        #         "invite": "https://discord.gg/upb9MCqb3X",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "",
        #     # },
        # },
        # "OpenStudioLandscapes-Watchtower": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-Watchtower",
        #     },
        #     "discord": {
        #         "channel_id": "1364747275938562079",
        #         "channel_name": "# openstudiolandscapes-watchtower",
        #         "invite": "https://discord.gg/5CQEjBaHg8",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "",
        #     # },
        # },
        # "OpenStudioLandscapes-OpenCue": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-OpenCue",
        #     },
        #     "discord": {
        #         "channel_id": "1379799680807997500",
        #         "channel_name": "# openstudiolandscapes-opencue",
        #         "invite": "https://discord.gg/3DdCZKkVyZ",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "",
        #     # },
        # },
        # "OpenStudioLandscapes-Grafana": {
        #     "github": {
        #         "repo_name": "OpenStudioLandscapes-Grafana",
        #     },
        #     "discord": {
        #         "channel_id": "1379800002179760159",
        #         "channel_name": "# openstudiolandscapes-grafana",
        #         "invite": "https://discord.gg/gEDQ8vJWDb",
        #     },
        #     # "slack": {
        #     #     "channel_id": "",
        #     #     "channel_name": "",
        #     # },
        # },
        # Template
        "OpenStudioLandscapes-Template": {
            "github": {
                "repo_name": "OpenStudioLandscapes-Template",
            },
            "discord": {
                "channel_id": "1414568696860512358",
                "channel_name": "# openstudiolandscapes-template",
                "invite": "https://discord.gg/J59GYp3Wpy",
            },
            # "slack": {
            #     "channel_id": "C09DMN2LH71",
            #     "channel_name": "# openstudiolandscapes-rustdeskserver",
            # },
        },
    }

    # Community

    doc.add_heading(
        text="Community",
        level=1,
    )

    header = [
        "Feature",
        "GitHub",
        "Discord",
        # "Slack",
    ]

    rows = []

    for feature, value in sorted(community_channels.items()):
        github_ = value["github"]
        discord_ = value["discord"]
        # slack_ = value["slack"]
        row = [
            # module,
            feature,
            f"[{gh_prefix}{github_['repo_name']}]({gh_prefix}{github_['repo_name']})",  # github
            f"[{discord_['channel_name']}]({discord_['invite']})",  # discord
            # f"[{slack_['channel_name']}]({slack}/{slack_['channel_id']})"  # slack
        ]

        rows.append(row)

    doc.add_table(
        header=header,
        data=rows,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            f"""
            To follow up on the previous LinkedIn publications, visit:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).",
            "[Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).",
        ]
    )

    # Inject Feature specific documentation if there is any
    if readme_feature is not None:
        doc.add_horizontal_rule()
        doc = readme_feature.readme_feature(doc)

    # Dump

    outfile = pathlib.Path(rel_path).parent.parent.parent.parent / "README"

    doc.dump(outfile.as_posix())

    return outfile


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="A tool to generate a README.md")
    parser.add_argument(
        "--version",
        action="version",
        version=f"OpenStudioLandscapesUtil-ReadmeGenerator {__version__}",
    )
    # parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.add_argument(
        # "-vv",
        # https://stackoverflow.com/questions/15753701/how-can-i-pass-a-list-as-a-command-line-argument-with-argparse
        "--versions",
        dest="versions",
        nargs='+',
        help="Python version(s) to use for testing. "
             "You can supply multiple versions (i.e. 3.11), "
             "separated by spaces.",
        required=True,
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    generate_readme(args.versions)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m OpenStudioLandscapesUtil.ReadmeGenerator.readme_generator 42
    #
    run()
