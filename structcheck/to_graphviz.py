"""
Nodes attributes: https://graphviz.org/docs/nodes/
Edges attributes: https://graphviz.org/docs/edges/
"""

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

                label = config["names"].get(el)["regex"][1:-1]
                if el in nodes:
                    i = 1
                    el += "_" + str(i)
                    while el in nodes:
                        el = el[:-len(str(i))]
                        i += 1
                        el += str(i)

                links.append([
                    config["names"].get(source, {"regex": source})["regex"],
                    config["names"].get(el, {"regex": el})["regex"],
                    attributes_edge
                ])
                nodes[el] = attributes_node | config["names"].get(el, {}) | {"label": label}
                
        elif isinstance(dico[elem], dict):
            attributes_node = config.get("nodes", {}).get("tree", {})
            attributes_edge = config.get("edges", {}).get("tree", {})
            links.append([
                config["names"].get(source, {"regex": source})["regex"],
                config["names"].get(elem, {"regex": elem})["regex"], {},
                attributes_edge
            ])
            nodes[elem] = attributes_node | config["names"].get(elem, {})
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
        nodes[node]["tooltip"] = f"{node}"
        if nodes[node].get('description', ""):
            nodes[node]["tooltip"] += f" : {nodes[node]['description']}"
        matches = re.findall("{.*?}", nodes[node].get("regex", node))
        if matches:
            nodes[node]["tooltip"] += "\n\n"
        regex_example = nodes[node].get("regex", node)
        for match in matches:
            key = match.replace("{", "").replace("}", "")
            if key not in config.get("variables", {}):
                continue
            regex_key = config.get("variables", {}).get(key)
            nodes[node]["tooltip"] += match + f" : ({regex_key.get('regex', '')}) = " + regex_key.get("description", "")
            if "example" in regex_key:
                nodes[node]["tooltip"] += f" -> {regex_key['example']}"
                regex_example = regex_example.replace(match, regex_key["example"])
            nodes[node]["tooltip"] += '\n'
        if len(matches):
            nodes[node]["tooltip"] += f"\nExample: {regex_example}"
        if node.replace("^", "").replace("$", "") != nodes[node].get("regex", node).replace("^", "").replace("$", ""):
            nodes[node]["xlabel"] = node
        node_txt = nodes[node].get("regex", node)
        if "label" not in nodes[node]:
            nodes[node]["label"] = node
        nodes[node]["label"] = nodes[node]["label"]
        f.node(node_txt, **nodes[node])
    for link in links:
        f.edge(link[0], link[1], **link[2])
    f.render(outfile=config['paths']['graph_svg'], format="svg")
