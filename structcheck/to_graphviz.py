"""
Nodes attributes: https://graphviz.org/docs/nodes/
Edges attributes: https://graphviz.org/docs/edges/
"""

import os
import re
import json
import graphviz

os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

def data_create(dico, nodes={}, links=[]):
    source = list(nodes)[-1]
    for elem in dico:
        if isinstance(dico[elem], list):
            for el in dico[elem]:
                attributes_edge = {}
                attributes_node = {}
                if elem == "Files_optionnal":
                    if config["regex_names"].get(el, {"type": "unknow"})["type"] == "folder":
                        attributes_node = config.get("default_styles_nodes", {}).get("Folders_optionnal", {})
                        attributes_edge = config.get("default_styles_edges", {}).get("Folders_optionnal", {})
                    elif config["regex_names"].get(el, {"type": "unknow"})["type"] == "file":
                        attributes_node = config.get("default_styles_nodes", {}).get("Files_optionnal", {})
                        attributes_edge = config.get("default_styles_edges", {}).get("Files_optionnal", {})
                elif elem == "Files":
                    if config["regex_names"].get(el, {"type": "unknow"})["type"] == "folder":
                        attributes_node = config.get("default_styles_nodes", {}).get("Folders", {})
                        attributes_edge = config.get("default_styles_edges", {}).get("Folders", {})
                    elif config["regex_names"].get(el, {"type": "unknow"})["type"] == "file":
                        attributes_node = config.get("default_styles_nodes", {}).get("Files", {})
                        attributes_edge = config.get("default_styles_edges", {}).get("Files", {})
                # else:
                    # raise Exception(f"Not allowed key '{elem}' in '{source}'")
                
                link_1 = config["regex_names"].get(source, {"regex": source})["regex"]
                if link_1.startswith("^"):
                    link_1 = link_1[1:]
                if link_1.endswith("$"):
                    link_1 = link_1[:-1]
                link_2 = config["regex_names"].get(el, {"regex": el})["regex"]
                if link_2.startswith("^"):
                    link_2 = link_2[1:]
                if link_2.endswith("$"):
                    link_2 = link_2[:-1]
                links.append([
                    link_1, 
                    link_2, 
                    attributes_edge
                ])
                # if el not in config["regex_names"]:
                    # raise Exception(f"Missing variable '{el}' in '{config['regex_names']}'")
                nodes[el] = attributes_node | config["regex_names"].get(el, {})
                
        elif isinstance(dico[elem], dict):
            attributes_node = config.get("default_styles_nodes", {}).get("Tree", {})
            links.append([
                config["regex_names"].get(source, {"regex": source})["regex"][1:-1],
                config["regex_names"].get(elem, {"regex": elem})["regex"][1:-1], {}
            ])
            nodes[elem] = attributes_node | config["regex_names"].get(elem, {}) 
            nodes, links = data_create(dico[elem], nodes=nodes, links=links)
        
        else:
            raise Exception(f"Wrong type for '{elem}' = {dico[elem]} : {type(dico[elem])}")
    
    return nodes, links


def main(path_config, path_graphiz):
    global config
    config = json.load(open(path_config, "r"))
    
    config["regex_names"] = {"root": {"regex": "^root$", "type": "folder", "description": "Root of data classification"}} | config.get("regex_names", {})
    
    nodes, links = data_create(config["Structure"], nodes={"root": config.get("default_styles_nodes", {}).get("Root", {}) | config.get("regex_names", {})["root"]})
    
    f = graphviz.Digraph('Graph', filename=path_graphiz, format="svg")
    f.attr(**config.get("graph_attributes", {}))
    f.attr('node', **config.get("default_styles_nodes", {}).get("All", {}))
    f.attr('edge', **config.get("default_styles_edges", {}).get("All", {}))
    for node in nodes:
        nodes[node]["tooltip"] = f"{node}"
        if nodes[node].get('description', ""):
            nodes[node]["tooltip"] += f" : {nodes[node]['description']}"
        matches = re.findall("{.*?}", nodes[node].get("regex", node))
        if matches:
            nodes[node]["tooltip"] += "\n\n"
        regex_example = nodes[node].get("regex", node)
        for match in matches:
            if "regex_variables" not in config:
                break
            regex_key = config["regex_variables"][match.replace("{", "").replace("}", "")]
            nodes[node]["tooltip"] += match + " = " + regex_key["description"] + "\n"
            if "example" in regex_key:
                regex_example = regex_example.replace(match, regex_key["example"])
        if len(matches):
            nodes[node]["tooltip"] += f"\nExample: {regex_example[1:-1]}"
        if node.replace("^", "").replace("$", "") != nodes[node].get("regex", node).replace("^", "").replace("$", ""):
            nodes[node]["xlabel"] = node
        node_txt = nodes[node].get("regex", node)
        if node_txt.startswith("^"):
            node_txt = node_txt[1:]
        if node_txt.endswith("$"):
            node_txt = node_txt[:-1]
        f.node(node_txt, **nodes[node])
    for link in links:
        f.edge(link[0], link[1], **link[2])
    f.render(outfile=path_graphiz+".svg", format="svg")


if __name__ == "__main__":
    dir_current = os.path.dirname(__file__)
    path_config = os.path.join(dir_current, "config.json")
    path_graphiz = os.path.join(dir_current, "graph")
    main(path_config, path_graphiz)
