import os
import re
import sys
import time
import xml.etree.ElementTree as etree
from OpenTextClass import HandleOpenTextXML

class read_xml:

   #handler to import
   xml_handler = HandleOpenTextXML()

   #location of the XML we want to extract from
   xml_loc = ""
      
   def __init__(self):
      self.__csv_structure__()
      header_row = ''
      for title in self.header:
         header_row = header_row + '"' + title + '",'
      sys.stdout.write(header_row.rstrip(',') + "\n")

   def __csv_structure__(self):
      self.header = self.xml_handler.csv_columns
      self.row_dict = self.xml_handler.csv_rows

   def output_csv(self, rows):
      str = ''
      for row in rows:
         for cell in self.header:
            value = row[cell]
            if value is None:
               value = ''
            str = str + '"' + value + '"' + ','
         str = str.strip(',') + "\n" 
      sys.stdout.write(str)
            
   def scan_xml(self):           
      self.rows = []
      for dp, dn, filenames in os.walk(self.xml_loc):
         for f in filenames:
            if os.path.splitext(f)[1] == '.xml':
               
               #create full path and read XML
               #note: consider if we need to protect create-write-access dates
               fullpath = os.path.abspath(os.path.join(dp, f))

               if re.match("(^\d*\.xml$)", f) is not None:
                  xmlfile = open(fullpath, 'rb')
                  tree = etree.parse(xmlfile)
                  xmlfile.close()   #close file once in memory
                  
                  root = tree.getroot()
                  xml_iter = iter(root)
               
                  document_count = self.xml_handler.xml_to_csv(root, self.row_dict, self.rows)
                  root.clear()
                  
                  #time.sleep(0.03) #throttle if necessary

      self.output_csv(self.rows)
      return document_count
      
#time script execution time roughly...
t0 = time.clock()

xml = read_xml()
document_count = xml.scan_xml()

log = open('output.log', 'wb')
log.write(str(document_count) + " files output" + "\n")
log.write(str(time.clock() - t0) + " script execution time" + "\n")