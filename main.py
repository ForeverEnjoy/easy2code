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
    schema_file = ''
    schema_file_type = ''

    def __init__(self):
        pass


def underscore(s):
    return s.replace(" ", "_").replace("-", "_")


def get_opt_arg():
    print '参数列表:', str(sys.argv)
    optarg = OptArg()
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ht:c:s:o:",
            ["template_file=", "code_file=", "schema_file=", "schema_file_type="]
        )
    except getopt.GetoptError:
        print '-t <template_file> -c <code_file> -s <schema_file> -o <schema_file_type>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: main.py -t <template_file> -c <code_file> -s <schema_file> -o <schema_file_type>'
            sys.exit()
        elif opt in ("-t", "--template_file"):
            optarg.template_file = arg
        elif opt in ("-c", "--code_file"):  # output code file
            optarg.code_file = arg
        elif opt in ("-s", "--schema_file"):  # dir/* dir/*.txt dir/file.txt
            optarg.schema_file = arg
        elif opt in ("-o", "--schema_file_type"):  # js or json5
            optarg.schema_file_type = arg
    return optarg


def read_config(schema_file, schema_type):
    content = open(schema_file, 'r').read()
    if 'js' == schema_type:
        ctx = execjs.compile(content)
        return ctx.eval('__config__')
    return json5.loads(content)


def write_to(file_path, content):
    print os.path.dirname(file_path)
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
    for e in glob.glob(opt_arg.schema_file):
        # print c
        # config = json5.load(open(c, 'r'))
        config = read_config(e, opt_arg.schema_file_type)
        print config
        out = template.render(config)

        out_path = env.from_string(opt_arg.code_file).render(config)
        if '' == out_path:
            raise ValueError('output path is empty')

        write_to(out_path, out)



