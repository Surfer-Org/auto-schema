import json

def schema_to_mdx(json_data, indent=0):
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
            elif value.get('type') == 'csv':
                mdx += "  " * indent + f'<Accordion title="{key}">\n'
                columns = value.get('columns', {})
                mdx += "  " * (indent + 1) + "| Column | Data Type | Example Value | Nullable |\n"
                mdx += "  " * (indent + 1) + "|---------------|-----------|---------------|----------|\n"
                for col_name, col_info in columns.items():
                    data_type = col_info.get('data_type', '')
                    example = col_info.get('example_value', '')
                    nullable = col_info.get('nullable', '')
                    mdx += "  " * (indent + 1) + f"| {col_name} | {data_type} | {example} | {nullable} |\n"
                mdx += "  " * indent + "</Accordion>\n"
            elif not value:
                mdx += "  " * indent + f'<Card title="{key}"></Card>\n'
            else:
                mdx += "  " * indent + f'<Accordion title="{key}">\n'
                mdx += "  " * (indent + 1) + "<AccordionGroup>\n"
                mdx += schema_to_mdx(value, indent + 2)
                mdx += "  " * (indent + 1) + "</AccordionGroup>\n"
                mdx += "  " * indent + "</Accordion>\n"
        else:
            mdx += "  " * indent + f'<Card title="{key}"></Card>\n'
    return mdx

def generate_mdx(json_data, output_file):
    mdx_content = f"""# Data Export Format

<Info>
This is an optional info card that you can use.
</Info>


Export type: [insert export type]

<AccordionGroup>
{schema_to_mdx(json_data)}
</AccordionGroup>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mdx_content)