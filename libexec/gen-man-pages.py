# -*- python -*-
#
# More info / inspiration:
#
#   https://tanguy.ortolo.eu/blog/article153/awscli-manpages
#

import collections

import subprocess
import awscli
import awscli.clidriver
import awscli.help
import gzip

# --------------------------------------------------------------------------------------------------
# The libraries don't expose customization points for these, so we make our own!

from docutils.core import publish_string
from docutils.writers import manpage

class TroffHelpRenderer(object):
    def render(self, contents):
        writer = manpage.Writer()
        global output_file
        output_file.write(publish_string(contents, writer=writer))

awscli.help.get_renderer = lambda: TroffHelpRenderer()

def manpage_translate_with_docinfo(manpage_writer):
    global aws_cli_version
    visitor = manpage_writer.translator_class(manpage_writer.document)
    visitor._docinfo['manual_group']   = 'awscli'
    visitor._docinfo['manual_section'] = '1aws'
    visitor._docinfo['version']        = awscli.__version__
    manpage_writer.document.walkabout(visitor)
    manpage_writer.output = visitor.astext()

manpage.Writer.translate = manpage_translate_with_docinfo

# --------------------------------------------------------------------------------------------------

# driver = awscli.clidriver.CLIDriver()
driver = awscli.clidriver.create_clidriver()

def write_manpage(command):
    filename = '%s.1aws' % '-'.join(command)
    command = command[1:]  # Strip off leading `aws`.
    command.append('help')
    print(filename)
    global output_file
    # output_file = open(filename, 'wb')
    output_file = gzip.open(f"{filename}.gz", mode='wb', compresslevel=9)
    global driver
    driver.main(command)
    output_file.close()

# --------------------------------------------------------------------------------------------------

pending = collections.deque()
pending.append( ( ['aws'], driver ) )

while len( pending ) > 0:
    command_so_far, command_obj = pending.popleft()
    write_manpage(command_so_far)
    for subcommand, subcommand_table in command_obj.subcommand_table.items():
        if subcommand == "help":
            continue
        new_command = command_so_far[:]
        new_command.append( subcommand )
        pending.append( ( new_command, subcommand_table ) )
