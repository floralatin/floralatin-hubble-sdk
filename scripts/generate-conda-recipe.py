import yaml
import json

class RecipeDumper(yaml.SafeDumper):
    """Adds a line break between top level objects and ignore aliases"""

    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def ignore_aliases(self, data):
        return True

    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

def delete_lines(file: str, line: int):
    with open(file, 'r') as fr:
        read_lines = fr.readlines()

    with open(file, 'w') as fw:
        write_lines = ''.join(read_lines[line:])
        fw.write(write_lines)


def get_lines(file: str, start: int, end: int):
    with open(file, 'r') as fr:
        read_lines = fr.readlines()
    return read_lines[ start:end ]


def insert_lines(file: str, insert_lines: list, start: int = 0):
    with open(file, 'r+') as fd:
        contents = fd.readlines()
        for index,line in enumerate(insert_lines):
            contents.insert(start + index, line)
            fd.seek(0)
        fd.writelines(contents)


def generate_meta_yaml(path: str, target_path: str):
    path = "conda/floralatin-hubble-sdk/meta.yaml"

    save_lines = get_lines(path, 0, 2)
    delete_lines(path, 2)

    with open(path) as f:
        meta_dict = yaml.safe_load(f)

        meta_dict['package'] = {'name': '<{ name|lower }>', 'version': '<{ version }>'}

        requirements = meta_dict['requirements']
        if(meta_dict['requirements'] and meta_dict['requirements']['host']):
            meta_dict['requirements']['host'] = ['docker-py' if item == 'docker' else item for item in meta_dict['requirements']['run']]
        if(meta_dict['requirements'] and meta_dict['requirements']['run']):
            meta_dict['requirements']['run'] = ['docker-py' if item == 'docker' else item for item in meta_dict['requirements']['run']]

    with open(target_path, 'w+') as fp:
        recipe = yaml.dump(
            meta_dict,
            Dumper=RecipeDumper,
            width=1000,
            sort_keys=False,
            default_style=None,
        )
        recipe = recipe.replace('<{', '{{').replace('}>', '}}')
        fp.write(recipe)
    
    insert_lines(target_path, save_lines)

generate_meta_yaml("conda/floralatin-hubble-sdk/meta.yaml", 'conda/meta.yaml')