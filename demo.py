import importlib
import yaml
from jinja2 import Template

if __name__ == '__main__':
    config = None
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

    print config['output']['class']
    print config['output']['parameters']
    
    template = None
    with open('template.json', 'r') as template_file:
        template = Template(template_file.read())
    
    context = {}
    for mod_name in config['imports']:
        module = importlib.import_module(mod_name)
        context[mod_name] = module

    for datum in config['data']:
        for k, v in datum.items():
            context[k] = v
    print context
    print template.render(context)
