import os
import subprocess

def convert_tex_to_rst(root_dir='technical-spec'):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.tex'):
                tex_path = os.path.join(dirpath, filename)
                rst_path = os.path.splitext(tex_path)[0] + '.rst'

                try:
                    subprocess.run(
                        ['pandoc', tex_path, '-f', 'latex', '-t', 'rst', '-o', rst_path],
                        check=True
                    )
                    print(f"Converted: {tex_path} → {rst_path}")
                except subprocess.CalledProcessError:
                    print(f"Failed to convert: {tex_path}")
                except FileNotFoundError:
                    print("Pandoc not found. Please install it with: sudo apt install pandoc")

if __name__ == '__main__':
    convert_tex_to_rst()
    