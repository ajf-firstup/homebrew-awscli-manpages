#!/opt/homebrew/Cellar/awscli/2.9.1/libexec/bin/python3.11
#
# More info / inspiration:
#
#   https://tanguy.ortolo.eu/blog/article153/awscli-manpages
#

import subprocess
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
    visitor = manpage_writer.translator_class(manpage_writer.document)
    visitor._docinfo['manual_group']   = 'awscli'
    visitor._docinfo['manual_section'] = '1aws'
    visitor._docinfo['version']        = '2.9.1'
    manpage_writer.document.walkabout(visitor)
    manpage_writer.output = visitor.astext()

manpage.Writer.translate = manpage_translate_with_docinfo

# --------------------------------------------------------------------------------------------------

driver = awscli.clidriver.CLIDriver()

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

write_manpage(['aws'])
for command, subcommands in driver._get_command_table().items():
    write_manpage(['aws', command])
    if command != 'help':
        for subcommand in subcommands._get_command_table():
            write_manpage(['aws', command, subcommand])
