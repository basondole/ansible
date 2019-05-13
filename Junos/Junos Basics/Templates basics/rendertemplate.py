from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('./templates/'))

def gen(filename):

    print('-------------------')
    print('')
    with open('vars/' + filename + '.yml') as _:
        varfile = yaml.load(_)
        template = ENV.get_template(filename + ".j2")
        print(template.render(config=varfile))

gen('interfaces')

gen('protocolbgp')

gen('protocolospf')

gen('protocolrip')

gen('protocolstatic')

# Forked from Matt Oswalt's nwkauto git
