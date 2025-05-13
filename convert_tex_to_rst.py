import os
import subprocess

# Function to recursively convert all `.tex` files in a directory to `.rst` using Pandoc
def convert_tex_to_rst(root_dir='technical-spec'):
    # Walk through all subdirectories and files starting from root_dir
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Only process files ending in .tex
            if filename.endswith('.tex'):
                # Full path to the .tex file
                tex_path = os.path.join(dirpath, filename)
                # Replace .tex extension with .rst for output file
                rst_path = os.path.splitext(tex_path)[0] + '.rst'

                try:
                    # Run the Pandoc command to convert LaTeX to reStructuredText
                    subprocess.run(
                        ['pandoc', tex_path, '-f', 'latex', '-t', 'rst', '-o', rst_path],
                        check=True
                    )
                    print(f"Converted: {tex_path} → {rst_path}")
                except subprocess.CalledProcessError:
                    # Handles Pandoc execution errors
                    print(f"Failed to convert: {tex_path}")
                except FileNotFoundError:
                    # Handles missing Pandoc installation
                    print("Pandoc not found. Please install it with: sudo apt install pandoc")

# Run the converter when the script is executed directly
if __name__ == '__main__':
    convert_tex_to_rst()
