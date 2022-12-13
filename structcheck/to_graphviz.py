"""
Nodes attributes: https://graphviz.org/docs/nodes/
Edges attributes: https://graphviz.org/docs/edges/
"""
import copy
import os
import re
import graphviz

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"


def data_create(dico, config, nodes=None, links=None):
    if nodes is None:
        nodes = {}
    if links is None:
        links = []
    source = list(nodes)[-1]
    for y, elem in enumerate(dico):
        if isinstance(dico[elem], list):
            for el in dico[elem]:
                attributes_edge = {}
                attributes_node = {}
                if elem == "Files_optionnal":
                    if config["names"].get(el, {"type": "unknow"})["type"] == "folder":
                        attributes_node = config.get("nodes", {}).get("Folders_optionnal", {})
                        attributes_edge = config.get("edges", {}).get("Folders_optionnal", {})
                    elif config["names"].get(el, {"type": "unknow"})["type"] == "file":
                        attributes_node = config.get("nodes", {}).get("Files_optionnal", {})
                        attributes_edge = config.get("edges", {}).get("Files_optionnal", {})
                elif elem == "Files":
                    if config["names"].get(el, {"type": "unknow"})["type"] == "folder":
                        attributes_node = config.get("nodes", {}).get("Folders", {})
                        attributes_edge = config.get("edges", {}).get("Folders", {})
                    elif config["names"].get(el, {"type": "unknow"})["type"] == "file":
                        attributes_node = config.get("nodes", {}).get("Files", {})
                        attributes_edge = config.get("edges", {}).get("Files", {})

                node = el
                i = 1
                el += "_" + str(i)
                while el in nodes:
                    el = el[:-len(str(i))]
                    i += 1
                    el += str(i)
                    if i == 2:
                        print()
                nodes[el] = attributes_node | copy.deepcopy(config["names"].get(node, {})) | copy.deepcopy(nodes.get(node, {}))

                nodes[el]["label"] = nodes[el]["regex"]
                if nodes[el]["label"].startswith("^"):
                    nodes[el]["label"] = nodes[el]["label"][1:]
                if nodes[el]["label"].endswith("$"):
                    nodes[el]["label"] = nodes[el]["label"][:-1]
                if nodes[el]["label"] != node:
                    nodes[el]["xlabel"] = node
                nodes[el]["tooltip"] = f"{el}: { nodes[el].get('description', 'No description')}\n"
                matches = re.findall("{.*?}", nodes[el]["regex"])
                if matches:
                    nodes[el]["tooltip"] += "\n\n"
                    regex_example = nodes[el].get("regex", el)
                    for match in matches:
                        key = match.replace("{", "").replace("}", "")
                        if key not in config.get("variables", {}):
                            continue
                        regex_key = config.get("variables", {}).get(key)
                        nodes[el]["tooltip"] += match + f" : ({regex_key.get('regex', '')}) = " + regex_key.get("description", "")
                        if "example" in regex_key:
                            nodes[el]["tooltip"] += f" -> {regex_key['example']}"
                            regex_example = regex_example.replace(match, regex_key["example"])
                        nodes[el]["tooltip"] += '\n'
                    if len(matches):
                        nodes[el]["tooltip"] += f"\nExample: {regex_example}"

                links.append([
                    source,
                    el,
                    attributes_edge
                ])

        elif isinstance(dico[elem], dict):
            attributes_node = config.get("nodes", {}).get("tree", {})
            attributes_edge = config.get("edges", {}).get("tree", {})
            links.append([
                source,
                elem,
                attributes_edge
            ])

            nodes[elem] = attributes_node | config["names"].get(elem, {})
            nodes[elem]["label"] = nodes[elem]["regex"]
            if nodes[elem]["label"].startswith("^"):
                nodes[elem]["label"] = nodes[elem]["label"][1:]
            if nodes[elem]["label"].endswith("$"):
                nodes[elem]["label"] = nodes[elem]["label"][:-1]
            if nodes[elem]["label"] != elem:
                nodes[elem]["xlabel"] = elem
            nodes, links = data_create(dico[elem], config, nodes=nodes, links=links)
        
        else:
            raise Exception(f"Wrong type for '{elem}' = {dico[elem]} : {type(dico[elem])}")
    
    return nodes, links


def main(config):
    print(f"Generation graph at {config['paths']['graph_svg']}")
    nodes, links = data_create(
        config["structure"],
        config,
        nodes={"root": config["nodes"]["root"] | {"label": repr(config['paths']['root'])}}
    )

    f = graphviz.Digraph('Graph', filename=config['paths']['graph'], format="svg")
    f.attr(**config.get("graph", {}))
    f.attr('node', **config.get("nodes", {}).get("default", {}))
    f.attr('edge', **config.get("edges", {}).get("default", {}))
    for node in nodes:
        # nodes[node]["tooltip"] = f"{node}"
        # if nodes[node].get('description', ""):
        #     nodes[node]["tooltip"] += f" : {nodes[node]['description']}"
        # matches = re.findall("{.*?}", nodes[node].get("regex", node))
        # if matches:
        #     nodes[node]["tooltip"] += "\n\n"
        # regex_example = nodes[node].get("regex", node)
        # for match in matches:
        #     key = match.replace("{", "").replace("}", "")
        #     if key not in config.get("variables", {}):
        #         continue
        #     regex_key = config.get("variables", {}).get(key)
        #     nodes[node]["tooltip"] += match + f" : ({regex_key.get('regex', '')}) = " + regex_key.get("description", "")
        #     if "example" in regex_key:
        #         nodes[node]["tooltip"] += f" -> {regex_key['example']}"
        #         regex_example = regex_example.replace(match, regex_key["example"])
        #     nodes[node]["tooltip"] += '\n'
        # if len(matches):
        #     nodes[node]["tooltip"] += f"\nExample: {regex_example}"
        # if "label" not in nodes[node]:
        #     nodes[node]["label"] = nodes[node]["regex"]
        # if nodes[node]["label"].startswith("^"):
        #     nodes[node]["label"] = nodes[node]["label"][1:]
        # if nodes[node]["label"].endswith("$"):
        #     nodes[node]["label"] = nodes[node]["label"][:-1]
        f.node(node, **nodes[node])
    for link in links:
        f.edge(link[0], link[1], **link[2])
    f.render(outfile=config['paths']['graph_svg'], format="svg")
