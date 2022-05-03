from jinja2 import Environment, FileSystemLoader, StrictUndefined
from app import configuration as C
import time
import os


def render_myfile(template, parameter):

    if not os.path.isfile(C.TEMPLATE_DIR + template):
        return('T68')
    else:
        env = Environment(
            loader=FileSystemLoader(C.TEMPLATE_DIR),
            undefined=StrictUndefined,
            trim_blocks=True
        )

        template = env.get_template(template)
        return template.render(parameter)


def render_file(template, **kwargs):

    env = Environment(
        loader=FileSystemLoader(C.TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True
    )

    template = env.get_template(template)
    return template.render(**kwargs)


def generate_tname():

    timeint = int(str(time.time()).replace(".",""))
    timehex = hex(timeint)
    tnamenum = timehex[2:12].upper()
    return("ZTP"+tnamenum)

