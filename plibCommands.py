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
PAPER_DC = 'MasterCatalogue.csv'
import platform
if platform.system()=='Darwin':
    PATH_DB = '/Volumes/richard/NAS/PdfLibrary'
elif platform.system()=='Linux':
    PATH_DB = '/home/pi/NASmount/PdfLibary'
else:   # assume it is Windows
    PATH_DB = r'r:\NAS\PdfLibrary'

import pdfLibraryInterface as pfi
from rgrCsvData.findAdex import FindAdexError
from os import path

# local copies for testing - remove before commit and merge
# PATH_DB = ''
# TOPIC_DB = 'CategoriesTest.csv'
def loadTopics(args, f_name=None):
    """Load and return the database from the given file name"""
    if f_name is None:
        return pfi.PdfLibraryInterface(args, path.join(PATH_DB, TOPIC_DB))
    else:
        return pfi.PdfLibraryInterface(args, f_name)

def doAdd(args, db_file=None):
    """Add a new item to the topic database"""
    logger.debug('\tperform Add sub-command')
    # create a data base interface
    p_lib = loadTopics(args, db_file)
    # check that the topic is indeed new
    if args.force and p_lib.hasCategroy(args.cat):
        logger.info('Category {:s} already exists - use --force to change it'
                   .format(args.cat.upper()))
        return
    for _sa in args.see_also:
        # See Also information is optional
        # but it must refer to existing categories
        logger.debug('checking for see_also category:' + _sa)
        if not p_lib.hasCategory(_sa):
            logger.error('error: category ' + _sa + ' does not exist')
            return
    # if the new category is Xn00 then find the next free Xn value
    _flag = ' '
    if args.cat[2:]=='00':
        args.cat = p_lib.db.nextCategory(args.cat)
        _flag = ' new '
    logger.debug('adding' + _flag +'category:' + args.cat)
    # merge the desc and more arguments
    args.more.insert(0,args.desc)
    # a fudge for now the addEntry should handle an empty list
#    if len(args.see_also)==0:
#        p_lib.db.addEntry(args.cat, args.key, ' '.join(args.more))
#    else:
#        p_lib.db.addEntry(args.cat, args.key, ' '.join(args.more), 
#                          *args.see_also)
    try:
        p_lib.db.addEntry(args.cat, args.key, ' '.join(args.more), 
                          *args.see_also)
        p_lib.db.save()
    except FindAdexError, err:
        #logger.warning(err)
        logger.error('Error: ' + err)
    # for testing
    if db_file is not None:
        return p_lib

def doFind(args):
    logger.debug('\tperform Find sub-command, target:'+args.target)
    if args.Verbose:
        msg = ['search for']
        if args.words: msg.insert(0, 'whole words')
        if args.ignore: msg.insert(0, 'case insensitive')
        if args.words and args.ignore: msg.insert(1, 'and')
        msg.append('"'+args.target+'"')
        logger.debug(' '.join(msg))
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
            logger.debug('none')
        return
    else:
        for a in results:
            p_lib.display(a)
    if args.Verbose:
        logger.debug('{:<3n}{:s}'.format(len(results),'found'))
    
def doEdit(args):
    logger.debug('\tperform Edit sub-command')
   

if __name__=='__main__':  
    from os import sys
    from time import strftime
    logging.basicConfig(stream=sys.stdout)
    logger.level = logging.DEBUG       # change for interactive level
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    # testing here is not right:
    # the doXXX code still works on the full database 
    # when I want a way to test on the experimental one?
    
    # create dummy arguments
    import argparse
    args = argparse.Namespace()
    args.cat = 'A400'
    args.key = 'ZX89'
    args.desc = 'blah'
    args.more = ['blah', 'and', 'blah']
    args.force = False
    args.see_also = ['X200']
    new_db = doAdd(args, 'CategoriesTest.csv')
