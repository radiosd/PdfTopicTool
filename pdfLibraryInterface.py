# -*- coding: utf-8 -*-
"""
    Interface class for the Pdf Library Topic database

                                                     rgr19sep17
"""
import logging
logger = logging.getLogger(__name__)
logger.level = logging.INFO             # change for import level

import re
from rgrCsvData.findAdex import FindAdex, Category

class PdfLibraryInterface():
    def __init__(self, args, f_name=None):
        """Create the interface and load the Topic data base"""
        self.args = args
        if f_name is None:
            self.db = None
            self.length = 0
        else: 
            self.db = FindAdex(f_name, Category)
            self.length = len(self.db.data)
        
    def saveData(self):
        """Save the database as llong as not in test mode"""
        if self.args.test or self.db is None:
            logger.info('no changes saved')
        else:
            self.tdb.save()
        
#============================================================================
#   The FindAdex database is a list of CsvItem objects with 
#   REQUIRED_FIELDS and an OPTIONAL_FIELD that is a list 
#   
#============================================================================
    def hasCategory(self, key):
        return self.tdb.data.hasCategory(key)

    def search(self, fields):
        """use regex to search the fields prescribed by the various args"""
        # set up the regex pattern, to include -i and -w options
        if self.length==0:
            return []
        # turn on to allow field abbreviations
        # fields = [self.db.data[0].findKey(k) for k in fields]
        # create the search pattern
        case = re.IGNORECASE if self.args.ignore else 0
        match = r'\b' + self.args.target + r'\b' \
                if self.args.words else self.args.target 
        pattern = re.compile(match, flags=case)
        # look through whole db for this pattern in the fields provided
        # use exisitng functions - messy but ok for now
        logger.debug('search for:'+self.args.target+
                     ' in '+str(fields)+' fields')
        ans = []
        for item in self.db.data:
            # each one is a CsvItem, field abbreviations are not allowed
            if filter(pattern.search, [item[k] for k in fields]):
                ans.append(item)
        return ans
    
    def display(self, item):
        """print a single CsvItem using internal methods"""
        # quick and dirty for now
        if len(item['See Also'])==0:
            print '{:4s} {:s}'.format(item['Category'], item['Key Words'])
        else:
            print '{:4s} {:s} {:s}'.format(item['Category'],
                                           item['Key Words'], 
                                           str(item['See Also']))
        print '     {:s}'.format(item['Description'])
                                          
    
if __name__=='__main__':  
    from os import path, sys
    from time import strftime
    logging.basicConfig(stream=sys.stdout)
    logger.level = logging.DEBUG       # change for interactive level
    logger.info('\tstarting: '+path.basename(__file__)+'\t==='
                 + strftime('%a-%d %H:%M') + ' ===')
    # this is a local copy for test purposes
    # creat mock arguments
    import argparse
    args = argparse.Namespace()
    args.target = 'filter'
    args.test = True
    args.ignore = True
    args.words = False
    pli = PdfLibraryInterface(args, 'CategoriesTest.csv')