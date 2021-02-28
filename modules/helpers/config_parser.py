# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_parser.py
# Date:     28.Feb.2021
###############################################################################

import re
from logging import Logger
from types import SimpleNamespace
from modules.helpers.files import FileCompare
from typing import List

# regexes to use

project_root_regex = re.compile("\$\{(PROJECT_ROOT)\}")
placeholder_regex = re.compile("\$\{(.*)\}")

############################################################################
def expandItem(item: str, parents: List[object]) -> object:
    """Parses the given item, if it contains a placeholder, that placeholder 
        is expanded. If the item doesn't contain a placeholder, the item's 
        unaltered string is returned.

        Args:
            item (str): The item to parse and expand its placeholder
            parents (List[object]): The parents of the item to search for 
                                    the placeholder's content.

        Returns:
            object: The expanded string if the item contained a placeholder, the
                 original string else. Ig the placeholder points to another 
                 object, that is not a string, this object is returned.
    """
    ret_val = item

    result = project_root_regex.search(item)
    if result:
        ret_val = project_root_regex.sub("REPLACED_PROJECT_ROOT", item)
        return ret_val
   
    result = placeholder_regex.search(item)
    parent_to_use_id = 0
    if result:
        print("Found Placeholder: {place}".format(place=result.group(1)))
        placeholder = result.group(1)
        parent_regex = re.compile("(\.\./)")

        result = parent_regex.match(placeholder)
        while result  != None:
            #print("Found ../")
            placeholder = placeholder.removeprefix("../")
            #print(placeholder)
            result = parent_regex.match(placeholder)
            parent_to_use_id -= 1
            #print("Parent id {id}".format(id=parent_to_use_id))

        try:
            parent = parents[parent_to_use_id]          
                      
            substitute = parent[placeholder]
            print("Replace {ph} with: {elem}".format(
                ph=placeholder, elem=substitute))
        except:
            try:
                substitute = getattr(parent, placeholder)
                print("Replace {ph} with: {elem}, class".format(ph=placeholder,
                                                                elem=substitute))
            except: 
                return ret_val

        if isinstance(substitute, str):
            ret_val = placeholder_regex.sub(substitute, item)
        else:
            ret_val = substitute

    return ret_val


###############################################################################
def parseConfigElement(element: object, parents: List[object] = []) -> object:
    """Parses the given config element and replaces placeholders.
    Placeholders are strings of the form `${PLACEHOLDER}`, with start with a
    dollar sign followed by an opening curly brace and end with a curly brace.
    The string between the two curly braces is changed against it's value.

    Args:
        element (object): The configuration element to parse and expand.
        parent (List[object], optional): The parent and the parent's parent and it's 
        parent as a list, starting with the parent as first element. Defaults to None.

    Returns:

        object: The parsed and expanded object.
    """
    print("parseConfigElement: {element}, parents: {parents}".format(element=element.__class__, parents=len(parents)))
    local_parents = parents.copy()
    if isinstance(element, list):
        tmp_list = []        
        for subitem in element:           
            local_parents = parents.copy()           

            if hasattr(subitem, "__dict__"):               
                #print("Is item of list with __dict__: {element}".format(element=subitem))
                tmp_list.append(parseConfigElement(subitem, local_parents))

            elif isinstance(subitem, dict):
                local_parents.append(element)
               # print("Is item of list , dict: {element}".format(
                #    element=subitem))
                for key in subitem:                    
                    subitem[key] = parseConfigElement(
                        subitem[key], local_parents)

                tmp_list.append(subitem)
            else:
                #print("Is item of list: {element}".format(element=subitem))
                if isinstance(subitem, str):
                    tmp_list.append(expandItem(subitem, local_parents))
                else:
                    tmp_list.append(subitem)
        return tmp_list    
                

    elif hasattr(element, "__dict__"):
        local_parents = parents.copy()               
        for key in element.__dict__:          
            element.__dict__[key] = parseConfigElement(element.__dict__[key], local_parents)
        return element

    elif isinstance(element, FileCompare):
        return element

    elif isinstance(element, Logger):
        return element

    elif isinstance(element, str):
        return expandItem(element, local_parents)
    else:
        #print("Is item: {element}".format(element=element))
        return element

   
