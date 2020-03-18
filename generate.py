# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import sys
import json

try:
    import jinja2
except ImportError:
    raise ImportError('Could not import jinja2, make sure it is installed')

log = logging.getLogger(__name__)


def list_files(folder_path):
    """Traverse directory given by folder_path.
    Return a generator made up of *.rst files.
    """
    if (os.path.exists(folder_path) == False):
        raise FileNotFoundError('Could not find source directory')

    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)
        

def read_file(file_path):
    """Read file and return metadata and content."""
    try:
        with open(file_path, 'r') as f:
            raw_metadata = ""
            for line in f:
                if line.strip() == '---':
                    break
                raw_metadata += line
            content = ""
            for line in f:
                content += line
            f.close()
    except OSError:
        raise OSError('Could not open/read files')

    return json.loads(raw_metadata), content

def write_output(output_folder, filename, html_data):
    """Write htmp_data in output_folder/filename."""
    # try to create the output folder
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    with open(os.path.join(output_folder, filename + '.html'), 'w+') as f:
        f.write(html_data)
        f.close()

def generate_site(folder_path, output_folder):
    """Takes all .rst files in folder_path.
    Creates equivalent .html files in output_folder.
    """
    log.info("Generating site from %r", folder_path)

    # init jinja2 env with template folder "templatePath"
    templatePath = os.path.join(folder_path, "layout")
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templatePath),
        trim_blocks=True, lstrip_blocks=True)

    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)

        # get coresponding template (or 'layout' in our case)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)

        html_data = template.render(**data)
        file = os.path.basename(file_path)
        filename = os.path.splitext(file)[0]
        write_output(output_folder, filename, html_data)
        log.info("Writing %r with template %r", filename, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
