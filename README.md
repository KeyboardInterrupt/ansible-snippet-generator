# ansible-snippet-generator

This tool generates ansible code snippets based on the ansible documentation and jinja2 Templates

## Requirements

ansible-snippet-generator works with python2 or python3, the following python packages and Versions are needed.
- ansible `2.3.0.0`
- jinja2 

## Usage

To generate sublime-text snippets you would need to run this command:

`./ansible-snippet-generator.py -t templates/sublime-snippet-template.jinja2 -o ./sublime-snippets/ -e sublime-snippet`

To display all available commandline options/arguments run `./ansible-snippet-generator.py -h` which will display this:

```
usage: ansible-snippet-generator.py [-h] [-t TEMPLATE] [-o OUTPUT_DIRECTORY]
                                    [-e EXTENSION]
                                    [modules [modules ...]]

Generate snippets based on the Ansible module documentation.

positional arguments:
  modules               Modules to generate snippets for, if no modules are
                        given, snippets for all modules will be generated.

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Jinja2 template file used for Snippet generation.
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory, if none is specified, the snippets
                        will be printed out to STDOUT.
  -e EXTENSION, --extension EXTENSION
                        Filename extension used for the snippets. Default is
                        ".snippet"

```

## Availabla Jinja2 variables

You can use the following Information for snippet generation:
 
- the module name
- all available options
- option name
- available choices (i.e 'present' or 'absent')
- if a option is required
- a short description of an option

i.e. for the `group` module the available Information are:

```python
module = u'group'
options = [[u'state',
  {u'choices': [u'present', u'absent'],
   u'default': u'present',
   u'description': [u'Whether the group should be present or not on the remote host.'],
   u'required': False}],
 [u'gid',
  {u'description': [u'Optional I(GID) to set for the group.'],
   u'required': False}],
 [u'name',
  {u'description': [u'Name of the group to manage.'], u'required': True}],
 [u'system',
  {u'choices': [u'yes', u'no'],
   u'default': u'no',
   u'description': [u'If I(yes), indicates that the group created is a system group.'],
   u'required': False}]]
```

## Example Jinja2 Template

Template:

```jinja2
<snippet>
<content><![CDATA[
${1:{% for option in options %}# {{ option[0] }} = {{ option[1]['description'][0].split(' ')[:20]|join(' ')}}
{% endfor %}}- name: ${2:Name for {{ module }} module.}
  {{ module }}:
{% for option in options %}    ${% raw %}{{% endraw %}{{ loop.index +3 }}:{{ option[0] }}: {% raw %}}{% endraw %}
{% endfor %}  when: variable is defined
  with_items: array
  tags: array]]></content>
	<tabTrigger>{{ module }}</tabTrigger>
	<scope>source.yaml,source.ansible</scope>
</snippet>
```

Output of `./ansible-snippet-generator.py group -t templates/sublime-snippet-template.jinja2`:

```
<snippet>
<content><![CDATA[
${1:# state = Whether the group should be present or not on the remote host.
# gid = Optional I(GID) to set for the group.
# name = Name of the group to manage.
# system = If I(yes), indicates that the group created is a system group.
}- name: ${2:Name for group module.}
  group:
    ${4:state: }
    ${5:gid: }
    ${6:name: }
    ${7:system: }
  when: variable is defined
  with_items: array
  tags: array]]></content>
        <tabTrigger>group</tabTrigger>
        <scope>source.yaml,source.ansible</scope>
</snippet>
```
