#!/usr/bin/python
# -*- coding: UTF-8 -*-

import jinja2
import json5
import sys
import getopt
import glob
import os
import errno
import execjs
import stringconvertor


class OptArg:
    template_file = ''
    code_file = ''
    instance_file = ''
    instance_file_type = ''

    def __init__(self):
        pass


def underscore(s):
    return s.replace(" ", "_").replace("-", "_")


def get_opt_arg():
    optarg = OptArg()
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ht:c:i:",
            ["template_file=", "code_file=", "instance_file="]
        )
    except getopt.GetoptError:
        print('-t <template_file> -i <instance_file> -c <code_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: easy2code -t <template_file> -i <instance_file> -c <code_file>')
            sys.exit()
        elif opt in ("-t", "--template_file"):
            optarg.template_file = arg
        elif opt in ("-c", "--code_file"):  # output code file
            optarg.code_file = arg
        elif opt in ("-i", "--instance_file"):  # dir/* dir/*.txt dir/file.txt
            optarg.instance_file = arg
        elif opt in ("-o", "--instance_file_type"):  # TODO js or json5 
            optarg.instance_file_type = arg
    return optarg


def read_config(instance_file, schema_type):
    content = open(instance_file, 'r').read()
    if 'js' == schema_type:
        ctx = execjs.compile(content)
        return ctx.eval('__config__')
    return json5.loads(content)


def write_to(file_path, content):
    print(os.path.dirname(file_path))
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        try:
            os.makedirs(file_dir)
        except OSError as err:  # Guard against race condition
            if err.errno != errno.EEXIST:
                raise

    f = open(file_path, "w")
    try:
        f.write(content)
    finally:
        f.close()


if __name__ == '__main__':
    opt_arg = get_opt_arg()

    # init environment
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    env.filters['underscore'] = underscore
    env.filters['pascalcase'] = stringconvertor.pascalcase
    env.filters['camelcase'] = stringconvertor.camelcase

    # get template
    template = env.get_template(opt_arg.template_file)

    # list all file match config path
    for e in glob.glob(opt_arg.instance_file):
        config = read_config(e, opt_arg.instance_file_type)
        print (config)
        out = template.render(config)

        out_path = env.from_string(opt_arg.code_file).render(config)
        if '' == out_path:
            raise ValueError('output path is empty')
        print out_path

        write_to(out_path, out)



