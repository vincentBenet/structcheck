import re
import copy


def get_variables_in_regex(name_expression: str) -> list:
    """
    Return the list of regex variables inside a name expression
    """
    return re.findall(r"\{(.*?)\}", name_expression)


def name_to_regex(name_expression: str, variables: dict) -> str:
    """
    Return the regex expression of a name
    """
    name_regex = name_expression
    variables_regex = get_variables_in_regex(name_expression)
    for variable_name in variables_regex:
        if variable_name not in variables:
            raise Exception(f"Missing variable {variable_name} inside regex variables")
        name_regex = name_regex.replace('{'+variable_name+'}', variables[variable_name]["regex"], 1)
    return name_regex


def build_names_regex(names: dict, variables: dict) -> dict:
    """
    Build names in full regex
    """
    names_regex = copy.deepcopy(names)
    for name in names:
        names_regex[name]["regex"] = name_to_regex(
            names_regex[name]["regex"],
            variables
        )
    return names_regex


def get_dico_keylist(dico: dict, listo: list) -> dict:
    """
    Find a dict value by navigate throught key using list of keys
    """
    dico_duppli = copy.deepcopy(dico)
    for key in listo:
        dico_duppli = dico_duppli[key]
    return dico_duppli


def walker_regex(current_dict: dict, names: dict, variables: dict, structure: dict, path: list) -> dict:
    """
    Recursive function to scan a non-fixed size dictionnary and replace names with regex
    """
    for key in get_dico_keylist(structure, path):
        value = get_dico_keylist(structure, path + [key])
        if isinstance(value, list):
            for i, expression in enumerate(value):
                if expression not in names:
                    raise Exception(f"Missing '{expression}' into config of names")
                else:
                    current_dict[key][i] = name_to_regex(names[expression]["regex"], variables)
        if isinstance(value, dict):
            current_dict.pop(key)
            current_dict[name_to_regex(names[key]["regex"], variables)] = walker_regex(
                value,
                names,
                variables,
                structure,
                path + [key]
            )
    return current_dict
   

def walker_names(current_dict: dict, names: dict, structure: dict, path: list) -> dict:
    """
    Recursive function to scan a non-fixed size dictionnary and replace names with variables
    """
    for key in get_dico_keylist(structure, path):
        value = get_dico_keylist(structure, path + [key])
        if isinstance(value, list):
            for i, expression in enumerate(value):
                current_dict[key][i] = names[expression]["regex"]
        if isinstance(value, dict):
            current_dict.pop(key)
            current_dict[names[key]["regex"]] = walker_names(
                value,
                names,
                structure,
                path + [key]
            )
    return current_dict


def buid_structure_regex(structure: dict, names: dict, variables: dict) -> dict:
    """
    Build structure in full regex
    """
    return walker_regex(copy.deepcopy(structure), names, variables, structure, [])


def buid_structure_names(structure: dict, names: dict) -> dict:
    """
    Build structure with variables
    """
    return walker_names(copy.deepcopy(structure), names, structure, [])
