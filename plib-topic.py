#!/d/ProgramData/Anaconda2/python
# -*- coding: utf-8 -*-
"""
    Pdf Library command line utilities
    
    To expand the utility of the orevious library.py, need toi factor out
    functions betwee the Topic database and the Paper dattabase
 
                                               rgr19sep17                                         
"""
# =============================================================================    
#  Version Information
#  1.x.x    Initial ideas
#  1.1.x    Added the add subcommant
#  
# 
#   Dependencies
#   local   
#   library 
#           
#   Other   
# =============================================================================

# define the user interface, leaving all the functionality to
# imported code from plibCommands
PROG_DESCRIPTION = "PDF Library topic database utility"
CMD_NAME = 'plib-topic'
VERSION_NO = '1.0.1'         # increment last digit with minor changes
DATE = 5*'\t'+'rgr21oct17'   # see tinyUrl_Revisions.txt for notes

import argparse, sys
from os import path

# override the standard parser to add a usage line in case of an exception
class ArgumentParserRGR(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(message + '\n')
        self.print_usage()
        # for the command line version a system exit here
        # prevents the traceback message - not so useful when debugging
        self.exit(2,'done')
        # sys.exit(2)
        # raise 
    
parser = ArgumentParserRGR(
        description=PROG_DESCRIPTION,
        version='%(prog)s ' + VERSION_NO,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=path.basename(__file__) + DATE)

# build the parser structure by hand
subparsers = parser.add_subparsers(
        help='available sub-commands are add, find and edit')
parser.add_argument('-t', '--test', 
        help="show actions but don't change the database", 
        action='store_true')
parser.add_argument('-V', '--Verbose', 
        help='a way to get more help', action='store_true')

# use sub-parsers for each of the sub commands  
from plibCommands import doAdd                # the add command
# 2 required positional parameters
parser_add = subparsers.add_parser('add', 
        help='add a category to the database')
parser_add.set_defaults(func=doAdd)
parser_add.add_argument('cat', type=str, help='the category to be added')
parser_add.add_argument('key', type=str, help='key words for the category')
parser_add.add_argument('desc', type=str,
        help='text for the decription of this category in the database')
parser_add.add_argument('more', type=str, nargs='*',
        help='all added to the desc')
parser_add.add_argument('-F', '--force', action='store_true',
        help='Force a new category, overwtirring the old one')

parser_add.add_argument('-s', '--see-also', action='append', default=[],
        help='Include other categories in a list')
# add --see-also as an optiona item
from plibCommands import doFind
parser_find = subparsers.add_parser('find', 
        help='find a target string in the database - default=description')
parser_find.set_defaults(func=doFind)
# 1 required positional parameter
parser_find.add_argument('target', type=str, help='the item to search for')
# optional switches to control the search
parser_find.add_argument('-i', '--ignore', action='store_true',
        help='make search case sensitive')
parser_find.add_argument('-w', '--words', action='store_true',
        help='search for whole words only')

parser_find.add_argument('-c', '--cat', action='store_true',
        help='include the category field in the search')
parser_find.add_argument('-C', '--Category', action='store_true',
        help='search the category field only')
parser_find.add_argument('-d', '--desc', action='store_true',
        help='include the description field in the search')
parser_find.add_argument('-D', '--Description', action='store_true',
        help='search the description field only')
parser_find.add_argument('-k', '--key', action='store_true',
        help='include the key words field in the search')
parser_find.add_argument('-K', '--Key-word', action='store_true',
        help='search the key words field only')

from plibCommands import doEdit
parser_edit = subparsers.add_parser('edit',
        help='edit an exisitng item in the database')
parser_edit.add_argument('turl', type=str, 
        help='the T-URL to edit, use del to delete the last entry added')
parser_edit.add_argument('cmd', type=str, nargs='*',
        help='edit commands "new text to replace all exisitng"\r\n\
        "int text" to replace the existing[int] item')
parser_edit.add_argument('-u', '--url', action='store_true', 
        help='replace the existing url with the remaining cmd ... string')
parser_edit.set_defaults(func=doEdit)

def test(cmds):
    args = parser.parse_args(cmds.split())
    if args.Verbose:
        print 'args:', args
    args.func(args)
    return args

if __name__=='__main__':
    import logging
    from sys import stdout
    from time import strftime
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=stdout)
    logger.level = logging.INFO
    logger.debug('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    args = parser.parse_args()  # this will show help for -h
    if args.Verbose:
        print 'args:', args
    # run the utility
    args.func(args)
