#!/usr/bin/env python3
"""
Create Tool Script

This script automates the creation of new tools by:
1. Creating a new tool implementation file based on the template
2. Adding the tool definition to the tool_registry.py file
3. Adding the tool import and handler to tools/__init__.py
"""
import os
import re
import sys
import shutil
from pathlib import Path


def camel_to_snake(name):
    """Convert CamelCase to snake_case."""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def validate_tool_name(name):
    """Validate that the tool name is in CamelCase format."""
    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
        print("Error: Tool name must be in CamelCase format (e.g., SearchFlights).")
        sys.exit(1)


def create_tool_file(tool_name):
    """Create a new tool implementation file based on the template."""
    snake_name = camel_to_snake(tool_name)
    template_path = Path('tools/tool_template.py')
    new_tool_path = Path(f'tools/{snake_name}.py')
    
    if not template_path.exists():
        print("Error: Tool template not found. Please ensure tools/tool_template.py exists.")
        sys.exit(1)
    
    if new_tool_path.exists():
        print(f"Error: Tool file {new_tool_path} already exists.")
        sys.exit(1)
    
    # Copy and modify the template
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Replace placeholders
    modified_content = template_content.replace('def tool_name', f'def {snake_name}')
    
    with open(new_tool_path, 'w') as f:
        f.write(modified_content)
    
    print(f"✅ Created new tool file: {new_tool_path}")
    return snake_name


def add_tool_to_registry(tool_name, args):
    """Add the tool definition to the tool_registry.py file."""
    registry_path = Path('tools/tool_registry.py')
    
    if not registry_path.exists():
        print("Error: Tool registry file not found.")
        sys.exit(1)
    
    with open(registry_path, 'r') as f:
        registry_content = f.read()
    
    # Create tool definition
    args_content = []
    for arg in args:
        arg_name, arg_type, arg_desc = arg
        args_content.append(f"""
        ToolArgument(
            name="{arg_name}",
            type="{arg_type}",
            description="{arg_desc}",
        ),""")
    
    tool_def = f"""
{tool_name.lower()}_tool = ToolDefinition(
    name="{tool_name}",
    description="TODO: Add description for {tool_name} tool",
    arguments=[{''.join(args_content)}
    ],
)
"""
    
    # Find the position to insert the tool definition (before the first function)
    match = re.search(r'from models\.tool_definitions', registry_content)
    if match:
        insert_pos = registry_content.find('\n\n', match.end()) + 2
        new_content = registry_content[:insert_pos] + tool_def + registry_content[insert_pos:]
        
        with open(registry_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Added tool definition to {registry_path}")
    else:
        print("Warning: Could not find the right position to insert tool definition.")
        print(f"Please manually add the following definition to {registry_path}:")
        print(tool_def)


def update_init_file(tool_name, snake_name):
    """Add the tool import and handler to tools/__init__.py."""
    init_path = Path('tools/__init__.py')
    
    if not init_path.exists():
        print(f"Error: {init_path} not found.")
        sys.exit(1)
    
    with open(init_path, 'r') as f:
        init_content = f.read()
    
    # Add import
    import_line = f"from .{snake_name} import {snake_name}\n"
    if not import_line in init_content:
        # Find the last import
        match = re.search(r'^from \.\w+ import \w+', init_content, re.MULTILINE)
        if match:
            last_import_end = match.end()
            line_end = init_content.find('\n', last_import_end) + 1
            new_content = init_content[:line_end] + import_line + init_content[line_end:]
        else:
            new_content = import_line + init_content
    else:
        new_content = init_content
    
    # Add handler case
    handler_block = f"""    if tool_name == "{tool_name}":
        return {snake_name}"""
    
    if not handler_block in new_content:
        # Find the get_handler function
        match = re.search(r'def get_handler\(tool_name: str\):', new_content)
        if match:
            # Find the first return statement
            return_match = re.search(r'    if tool_name ==', new_content, re.MULTILINE)
            if return_match:
                insert_pos = return_match.start()
                new_content = new_content[:insert_pos] + handler_block + "\n" + new_content[insert_pos:]
            else:
                # If we can't find a return statement, add after function definition
                func_end = new_content.find('\n', match.end()) + 1
                new_content = new_content[:func_end] + handler_block + "\n" + new_content[func_end:]
        else:
            print("Warning: Could not find get_handler function.")
            print(f"Please manually add the following to {init_path}:")
            print(handler_block)
    
    with open(init_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated {init_path} with new tool import and handler")


def main():
    """Main function to create a new tool."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_tool.py ToolName [arg1:type:description] [arg2:type:description] ...")
        print("\nExample: python scripts/create_tool.py SearchHotels location:string:\"Hotel location\" checkin:ISO8601:\"Check-in date\"")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    validate_tool_name(tool_name)
    
    args = []
    for arg_str in sys.argv[2:]:
        parts = arg_str.split(':')
        if len(parts) < 3:
            print(f"Error: Argument '{arg_str}' is not in the correct format (name:type:description).")
            sys.exit(1)
        arg_name = parts[0]
        arg_type = parts[1]
        arg_desc = ':'.join(parts[2:])  # Rejoin any extra colons in the description
        args.append((arg_name, arg_type, arg_desc))
    
    snake_name = create_tool_file(tool_name)
    add_tool_to_registry(tool_name, args)
    update_init_file(tool_name, snake_name)
    
    print("\n🎉 Tool creation complete!")
    print(f"\nNext steps:")
    print(f"1. Update the description for {tool_name} in tools/tool_registry.py")
    print(f"2. Implement your tool logic in tools/{snake_name}.py")
    print(f"3. Test your tool with the agent workflow")


if __name__ == "__main__":
    main() 