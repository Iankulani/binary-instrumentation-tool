# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  1 12:45:47 2025

@author: IAN CARTER KULANI
"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("BINARY INSTRUMENTATION TOOL ")
print(Fore.GREEN+font)


import os
import subprocess

def assemble_code(assembly_file):
    """
    Assemble the given assembly code file into machine code using nasm.
    """
    try:
        # Check if the assembly file exists
        if not os.path.exists(assembly_file):
            print(f"Assembly file {assembly_file} not found.")
            return None

        # Define the output object file
        obj_filename = "temp.obj"

        # Run the nasm assembler using subprocess
        command = ["nasm", "-f", "bin", "-o", obj_filename, assembly_file]
        subprocess.run(command, check=True)

        # Read the generated binary file (machine code)
        with open(obj_filename, 'rb') as obj_file:
            machine_code = obj_file.read()

        # Clean up temporary object file
        os.remove(obj_filename)

        return machine_code

    except Exception as e:
        print(f"Error assembling code: {e}")
        return None


def modify_binary_file(binary_file_path, injected_code, offset=0):
    """
    Modify the binary file by injecting the assembly (machine) code at the specified offset.
    """
    try:
        # Open the original binary file
        with open(binary_file_path, 'rb') as file:
            binary_data = file.read()

        # Inject the assembly machine code into the binary data at the specified offset
        modified_data = bytearray(binary_data)

        # Ensure the injected code fits within the modified binary data
        modified_data[offset:offset+len(injected_code)] = injected_code

        # Write the modified data back to the binary file
        with open(binary_file_path, 'wb') as file:
            file.write(modified_data)

        print(f"Binary file {binary_file_path} has been modified successfully.")

    except Exception as e:
        print(f"Error modifying binary file: {e}")


def main():
    # Ask for the binary file to modify
    binary_file_path = input("Enter the path of the binary file you want to modify (e.g., file.bin):").strip()

    # Check if the binary file exists
    if not os.path.exists(binary_file_path):
        print(f"Binary file {binary_file_path} not found.")
        return

    # Ask for the assembly file
    assembly_file = input("Enter the path of the assembly file (e.g., code.asm):").strip()

    # Assemble the code from the assembly file
    injected_code = assemble_code(assembly_file)

    if injected_code is None:
        print("Failed to assemble the assembly code.")
        return

    # Ask the user for the injection offset (where the machine code will be inserted)
    try:
        offset = int(input("Enter the offset (in bytes) where the code will be injected (default 0): ").strip() or "0")
    except ValueError:
        print("Invalid input for offset. Using default value 0.")
        offset = 0

    # Modify the binary file with the injected machine code
    modify_binary_file(binary_file_path, injected_code, offset)


if __name__ == "__main__":
    main()
