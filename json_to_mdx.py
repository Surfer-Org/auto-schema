import json

def json_to_mdx(json_data, indent=0):
    mdx = ""
    for key, value in json_data.items():
        if isinstance(value, dict):
            if value.get('type') == 'json':
                mdx += "  " * indent + f'<Accordion title="{key}">\n'
                mdx += "  " * (indent + 1) + "```json\n"
                json_content = json.dumps(value.get('columns', {}), indent=2)
                mdx += "\n".join("  " * (indent + 1) + line for line in json_content.split("\n"))
                mdx += "\n"
                mdx += "  " * (indent + 1) + "```\n"
                mdx += "  " * indent + "</Accordion>\n"
            elif not value:
                mdx += "  " * indent + f'<Card title="{key}"></Card>\n'
            else:
                mdx += "  " * indent + f'<Accordion title="{key}">\n'
                mdx += "  " * (indent + 1) + "<AccordionGroup>\n"
                mdx += json_to_mdx(value, indent + 2)
                mdx += "  " * (indent + 1) + "</AccordionGroup>\n"
                mdx += "  " * indent + "</Accordion>\n"
        else:
            mdx += "  " * indent + f'<Card title="{key}"></Card>\n'
    return mdx

def generate_mdx(json_data, output_file):
    mdx_content = f"""---

## Data Export Format

Export type: [insert export type]

<AccordionGroup>
{json_to_mdx(json_data)}
</AccordionGroup>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mdx_content)
