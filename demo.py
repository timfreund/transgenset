import transgenset
import importlib
import sys
import time
import yaml
from jinja2 import Template

def configure_producer(config):
    context = {}
    for mod_name in config['imports']:
        module = importlib.import_module(mod_name)
        context[mod_name] = module

    for datum in config['data']:
        for k, v in datum.items():
            context[k] = v

    template = None
    with open('template.json', 'r') as template_file:
        template = Template(template_file.read())

    producer = transgenset.Producer(context, template)
    return producer

def configure_output_multiplexer(config, producer):
    print config['output']['class']
    print config['output']['parameters']
    mean_wait = float(config['output']['mean_wait'])

    transmitters = []

    for x in range(0, config['output']['transmitters']):
        full_class_name = config['output']['class']
        mod_name, class_name = full_class_name.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        cls = getattr(mod, class_name)
        kwparams = config['output']['parameters']
        if kwparams:
            transmitter = cls(**kwparams)
        else:
            transmitter = cls()
        transmitters.append(transmitter)

    multiplexer = transgenset.output.Multiplexer(producer, transmitters, mean_wait)
    return multiplexer

if __name__ == '__main__':
    config = None
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

    producer = configure_producer(config)
    multiplexer = configure_output_multiplexer(config, producer)
    multiplexer.start_transmissions()
    
    while True:
        try:
            time.sleep(1)
        except:
            multiplexer.stop_transmissions()
            sys.exit(1)

