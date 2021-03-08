# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     placeholder_regex.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

import re

# regexes to use

project_root_regex = re.compile(r"\$\{(PROJECT_ROOT)\}")
"""Regex to find the placeholder `${PROJECT_ROOT}`.
"""

project_name_regex = re.compile(r"\$\{(PROJECT_NAME)\}")
"""Regex to find the placeholder `${PROJECT_NAME}`.
"""

project_version_regex = re.compile(r"\$\{(PROJECT_VERSION)\}")
"""Regex to find the placeholder `${PROJECT_VERSION}`.
"""

project_author_regex = re.compile(r"\$\{(PROJECT_AUTHOR)\}")
"""Regex to find the placeholder `${PROJECT_AUTHOR}`.
"""

project_company_regex = re.compile(r"\$\{(PROJECT_COMPANY)\}")
"""Regex to find the placeholder `${PROJECT_COMPANY}`.
"""

project_copyright_info_regex = re.compile(r"\$\{(PROJECT_COPYRIGHT_INFO)\}")
"""Regex to find the placeholder `${PROJECT_COPYRIGHT_INFO}`.
"""

project_web_url_regex = re.compile(r"\$\{(PROJECT_WEB_URL)\}")
"""Regex to find the placeholder `${PROJECT_WEB_URL}`.
"""

project_email_regex = re.compile(r"\$\{(PROJECT_EMAIL)\}")
"""Regex to find the placeholder `${PROJECT_EMAIL}`.
"""

project_cfg_dir_regex = re.compile(r"\$\{(PROJECT_CONFIG_DIR_PATH)\}")
"""Regex to find the placeholder `${PROJECT_CONFIG_DIR_PATH}`.
"""

host_os_regex = re.compile(r"\$\{(HOST_OS)\}")
"""Regex to find the placeholder `${HOST_OS}`.
"""

host_name_regex = re.compile(r"\$\{(HOST_NAME)\}")
"""Regex to find the placeholder `${HOST_NAME}`.
"""

host_cpu_arch_regex = re.compile(r"\$\{(HOST_CPU_ARCH)\}")
"""Regex to find the placeholder `${HOST_CPU_ARCH}`.
"""

host_num_cores_regex = re.compile(r"\$\{(HOST_NUM_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_CORES}`.
"""

host_num_log_cores_regex = re.compile(r"\$\{(HOST_NUM_LOG_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_LOG_CORES}`.
"""

os_name_windows_regex = re.compile(r"\$\{(OS_NAME_WINDOWS)\}")
"""Regex to find the placeholder `${OS_NAME_WINDOWS}`.
"""

os_name_linux_regex = re.compile(r"\$\{(OS_NAME_LINUX)\}")
"""Regex to find the placeholder `${OS_NAME_LINUX}`.
"""

os_name_osx_regex = re.compile(r"\$\{(OS_NAME_OSX)\}")
"""Regex to find the placeholder `${OS_NAME_OSX}`.
"""

current_time_regex = re.compile(r"\$\{(TIME)\}")
"""Regex to find the placeholder `${TIME}`.
"""

current_date_regex = re.compile(r"\$\{(DATE)\}")
"""Regex to find the placeholder `${DATE}`.
"""

current_year_regex = re.compile(r"\$\{(YEAR)}")
"""Regex to find the placeholder `${YEAR}`.
"""

current_month_regex = re.compile(r"\$\{(MONTH)}")
"""Regex to find the placeholder `${MONTH}`.
"""

current_day_regex = re.compile(r"\$\{(DAY)}")
"""Regex to find the placeholder `${DAY}`.
"""

placeholder_regex = re.compile(r"\$\{(.*)\}")
"""Regex to find general placefolders, of the form `${STRING}`, where string
is to be substituted for a value of another configuration item.
"""
