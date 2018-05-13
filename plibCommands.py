# -*- coding: utf-8 -*-
"""
    Commands for the plib-topic utility

                                           rgr19sep17
"""
import logging
logger = logging.getLogger(__name__)
logger.level = logging.INFO             # change for import level

# csv data basea are on the NAS drive, access is different on each platform
TOPIC_DB = 'Categories.csv'
PAPER_DB = 'MasterCatalogue.csv'
import platform
if platform.system()=='Darwin':
    PATH_DB = '/Volumes/richard/NAS/PdfLibrary'
elif platform.system()=='Linux':
    PATH_DB = '/home/pi/NASmount/PdfLibary'
else:   # assume it is Windows
    PATH_DB = r'r:\NAS\PdfLibrary'

import pdfLibraryInterface as pfi
from os import path

def loadTopics(args):
    """Load and return the database from the given file name"""
    return pfi.PdfLibraryInterface(args, path.join(PATH_DB, TOPIC_DB))

def doAdd(agrs):
    logger.debug('\tperform Add sub-command')

def doFind(args):
    logger.debug('\tperform Find sub-command, target:'+args.target)
    if args.Verbose:
        msg = ['search for']
        if args.words: msg.insert(0, 'whole words')
        if args.ignore: msg.insert(0, 'case insensitive')
        if args.words and args.ignore: msg.insert(1, 'and')
        msg.append('"'+args.target+'"')
        print(' '.join(msg))
    # create a list of the fields to search, better to get them from
    # the database somehow?
    if args.Category:
        fields = ['Category']
    elif args.Key_word:
        fields = ['Key Words']
    elif args.Description:
        fields = ['Description']
    else:
        fields = ['Description']
        if args.key:
            fields.insert(0, 'Key Words')
        if args.cat:
            fields.insert(0, 'Category')
    logger.debug('search in: ' + str(fields))
    # create a data base interface
    p_lib = loadTopics(args)
    results = p_lib.search(fields)
    # display results
    if len(results)==0:
        if args.Verbose:
            print('none')
        return
#    elif args.select:
#      # the item selected or first by default  
#      n = args.selection 
#      if n<len(ans):
#          tiny_ci.display(ans[n], True)
#      else:
#          if args.Verbose:
#              print(Display.LINE2.format(str(n),'out of range'))
    else:
        for a in results:
            p_lib.display(a)
    if args.Verbose:
        print('{:<3n}{:s}'.format(len(results),'found'))
    # return results
    
def doEdit(args):
    logger.debug('\tperform Edit sub-command')

def doShowPaths():
    """print the full path and filename of the databases used"""
    print('Topics: {:s}'.format(path.join(PATH_DB, TOPIC_DB)))
    print('Papers: {:s}'.format(path.join(PATH_DB, PAPER_DB)))
          

if __name__=='__main__':  
    from os import sys
    from time import strftime
    logging.basicConfig(stream=sys.stdout)
    logger.level = logging.DEBUG       # change for interactive level
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')

    tdb = loadTopics(None)
