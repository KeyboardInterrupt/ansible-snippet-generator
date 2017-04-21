#!/usr/bin/env python
from ansible import constants as C
from ansible.plugins import module_loader
from ansible.utils import module_docs
from ansible.compat.six import iteritems
from jinja2 import Template
import os
import codecs
import argparse


def main():
    parser = argparse.ArgumentParser(description='Generate snippets based on the Ansible module documentation.')
    parser.add_argument('modules', nargs='*', type=str, help='Modules to generate snippets for, if no modules are given, snippets for all modules will be generated.')
    parser.add_argument('-t', '--template', type=str, default=None,
                        help='Jinja2 template file used for Snippet generation.')
    parser.add_argument('-o', '--output-directory', type=str, default=None,
                        help='Output directory, if none is specified, the snippets will be printed out to STDOUT.')
    parser.add_argument('-e', '--extension', default='.snippet', type=str,
                        help='Filename extension used for the snippets. Default is ".snippet"')
    args = parser.parse_args()

    template = Template(
        '''
- name: Name for {{ module }} module.
  {{ module }}:
{% for option in options %}   {{ option[0] }}: {{option[1]['default']}}
{% endfor %}
  when: variable is defined
  with_items: array
  tags: array
'''
    )
    if args.template != None:
        with open(args.template, 'r') as template_file:
            template = Template(template_file.read())
    modules = args.modules
    if args.modules == []:
        for path in module_loader._get_paths():
            for module in find_modules(path):
                modules.append(module)
    for module in modules:
        doc, plainexamples, returndocs, metadata = module_docs.get_docstring(
            module_loader.find_plugin(module, mod_type='.py', ignore_deprecated=True))
        options = []
        if doc is not None:
            for (k, v) in iteritems(doc['options']):
                options.append([k, v])
            if args.output_directory == None:
                print(template.render(module=module, options=options))
            else:
                with codecs.open("%s/%s.%s" % (args.output_directory, module, args.extension), 'w',
                                 'utf-8') as snippet_file:
                    snippet_file.write(template.render(module=module, options=options))


def find_modules(path):
    module_list = []
    for module in os.listdir(path):
        full_path = '/'.join([path, module])

        if module.startswith('.'):
            continue
        elif os.path.isdir(full_path):
            continue
        elif any(module.endswith(x) for x in C.BLACKLIST_EXTS):
            continue
        elif module.startswith('__'):
            continue
        elif module in C.IGNORE_FILES:
            continue
        elif module.startswith('_'):
            if os.path.islink(full_path):  # avoids aliases
                continue

        module = os.path.splitext(module)[0]  # removes the extension
        module = module.lstrip('_')  # remove underscore from deprecated modules
        module_list.append(module)
    return module_list


if __name__ == '__main__':
    main()
