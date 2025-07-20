import yaml

def parse_markdown_with_frontmatter(path):
    """Devuelve un diccionario con frontmatter y el contenido Markdown."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"El archivo {path} no contiene frontmatter YAML.")

    start, end = None, None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if start is None:
                start = i
            elif end is None:
                end = i
                break

    if start is None or end is None or end <= start:
        raise ValueError(f"Frontmatter mal formado en {path}.")

    yaml_block = yaml.safe_load("".join(lines[start+1:end]))
    markdown_body = "".join(lines[end+1:])
    return yaml_block, markdown_body


def update_frontmatter_field(path, field, new_value):
    """Actualiza un campo del frontmatter YAML y guarda el archivo."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    start, end = None, None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if start is None:
                start = i
            elif end is None:
                end = i
                break

    if start is None or end is None:
        raise ValueError(f"Frontmatter mal formado en {path}.")

    yaml_block = yaml.safe_load("".join(lines[start+1:end]))
    yaml_block[field] = new_value
    new_yaml = yaml.dump(yaml_block, allow_unicode=True, sort_keys=False)

    new_content = (
        lines[:start+1]
        + [line + "\n" for line in new_yaml.strip().splitlines()]
        + lines[end:]
    )

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_content)
