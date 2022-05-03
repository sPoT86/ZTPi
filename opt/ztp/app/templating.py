from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound, UndefinedError, TemplateSyntaxError
from app import configuration as C
import time
import os


def render_myfile(template, parameter):

    if not os.path.isdir(C.TEMPLATE_DIR):
        return('T74')
    else:
        env = Environment(
            loader=FileSystemLoader(C.TEMPLATE_DIR),
            undefined=StrictUndefined,
            trim_blocks=True
        )

        try:
            template = env.get_template(template)
            try:
                config = template.render(parameter)
            except UndefinedError:
                return('T81')
            except TemplateSyntaxError:
                return('T82')
            else:
                return config
        except TemplateNotFound:
            return('T68')


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

