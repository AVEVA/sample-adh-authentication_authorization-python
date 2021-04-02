# pylint: disable=fixme, line-too-long, import-error, no-name-in-module
#
# Copyright (c) 2020 Synopsys, Inc.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Uncomment for debugging. Can't use localhost.
# See: https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config
# import pydevd_pycharm
# pydevd_pycharm.settrace('<Host IP Address>', port=5002, stdoutToServer=True, stderrToServer=True)

"""
A script that inspects the pip cache to determine the hierarchy of dependencies

Usage: pip-inspector.py --projectname=<project_name> --requirements=<requirements_path>
"""

from getopt import getopt, GetoptError
from os import path
import sys
from re import split
from pkg_resources import working_set, Requirement

import pip
# pip_major_version = int(pip.__version__.split(".")[0])
# if pip_major_version >= 20:
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession
# elif pip_major_version >= 10:
#     from pip._internal.req import parse_requirements
#     from pip._internal.download import PipSession
# else:
#     from pip.req import parse_requirements
#     from pip.download import PipSession


def main():
    """Handles commandline args, executes the inspector, and prints the resulting dependency tree"""
    try:
        opts, __ = getopt(sys.argv[1:], 'p:r:', [
                          'projectname=', 'requirements='])
    except GetoptError as error:
        print(str(error))
        print('integration-pip-inspector.py --projectname=<project_name> --requirements=<requirements_path>')
        sys.exit(2)

    project_name = None
    requirements_path = None

    for opt, arg in opts:
        if opt in ('-p', '--projectname'):
            project_name = arg
        elif opt in ('-r', '--requirements'):
            requirements_path = arg

    project_dependency_node = resolve_project_node(project_name)

    if requirements_path is not None:
        try:
            assert path.exists(
                requirements_path), ("The requirements file %s does not exist." % requirements_path)
            populate_dependency_tree(
                project_dependency_node, requirements_path)
        except AssertionError:
            print('r?' + requirements_path)

    print(project_dependency_node.render())


def resolve_project_node(project_name):
    """Attempts to resolve the root DependencyNode from the user provided --projectname argument.
    If it can't, produces a DependencyNode with name 'n?' and version 'v?'"""
    project_dependency_node = None

    if project_name is not None:
        project_dependency_node = recursively_resolve_dependencies(
            project_name, [])

    if project_dependency_node is None:
        project_dependency_node = DependencyNode('n?', 'v?')

    return project_dependency_node


def populate_dependency_tree(project_root_node, requirements_path):
    """Resolves the dependencies of the user-provided requirements.txt and appends them to the dependency tree"""
    try:
        # This line is pretty much the only reason why we call the internal pip APIs anymore. We should consider if we
        # can do this with a more generalized approach.
        # --rotte DEC 2020
        parsed_requirements = parse_requirements(
            requirements_path, session=PipSession())
        for parsed_requirement in parsed_requirements:
            package_name = None

            print('populate_dependency_tree')
            print(parsed_requirements)
            print(requirements_path)

            # In 20.1 of pip, the requirements object changed
            if hasattr(parsed_requirement, 'req'):
                package_name = parsed_requirement.req.name

            print(package_name)

            if package_name is None:
                # Comparators from: https://www.python.org/dev/peps/pep-0508/#grammar
                # (Last updated November 2020)
                #
                # re matches from left to right, so subsets (e.g. ===) should be before supersets (e.g. ==)
                # See: https://docs.python.org/3/library/re.html
                # --rotte NOV 2020
                package_name = split(
                    '===|<=|!=|==|>=|~=|<|>', parsed_requirement.requirement)[0]

            print(package_name)

            dependency_node = recursively_resolve_dependencies(
                package_name, [])

            if dependency_node is not None:
                project_root_node.children = project_root_node.children + \
                    [dependency_node]
            else:
                print('--' + package_name)
    except:
        print('p?' + requirements_path)


def recursively_resolve_dependencies(package_name, history):
    """Forms a DependencyNode by recursively resolving its dependencies. Tracks history for cyclic dependencies."""
    package = get_package_by_name(package_name)
    print('recursively... after get_package_by_name')
    print(package)
    if package is None:
        return None

    dependency_node = DependencyNode(package.project_name, package.version)

    if package_name.lower() not in history:
        for package_dependency in package.requires():
            child_node = recursively_resolve_dependencies(
                package_dependency.key, history + [package_name.lower()])
            if child_node is not None:
                dependency_node.children = dependency_node.children + \
                    [child_node]

    return dependency_node


def get_package_by_name(package_name):
    """Looks up a package from the pip cache"""
    print('get_package_by_name')
    print(package_name)
    if package_name is None:
        return None

    package_dict = working_set.by_key
    try:
        # TODO: By using pkg_resources.Requirement.parse to get the correct key, we may not need to attempt the other
        #     methods. Robust tests are needed to confirm.
        return package_dict[Requirement.parse(package_name).key]
    except:
        print('except')
        pass

    print('variants')
    name_variants = (package_name, package_name.lower(), package_name.replace(
        '-', '_'), package_name.replace('_', '-'))
    for name_variant in name_variants:
        if name_variant in package_dict:
            return package_dict[name_variant]

    return None


class DependencyNode(object):
    """Represents a python dependency in a tree graph with a name, version, and array of children DependencyNodes"""

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.children = []

    def render(self, layer=1):
        """Recursively builds a dependency tree string to be printed to the commandline"""
        result = self.name + "==" + self.version
        for child in self.children:
            result += "\n" + (" " * 4 * layer)
            result += child.render(layer + 1)
        return result


if __name__ == '__main__':
    main()
