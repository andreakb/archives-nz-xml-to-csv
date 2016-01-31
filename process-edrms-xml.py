import os
import re
import argparse
import sys
import time
import xml.etree.ElementTree as etree
from OpenTextClass import HandleOpenTextXML

class read_xml:

   #handler to import
   xml_handler = HandleOpenTextXML()
   
   #where the xml resides...
   xml_loc = ''
   
   def __init__(self, xml_loc):
      self.xml_loc = xml_loc
      self.__csv_structure__()
      header_row = ''
      if os.path.isdir(self.xml_loc):
         for title in self.header:
            header_row = header_row + '"' + title + '",'
         sys.stdout.write(header_row.rstrip(',') + "\n")
      else:
         sys.stderr.write("WARNING: Input directory " + self.xml_loc + " is not a directory.")

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
      document_count = 0
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
      
def main():

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Extract and Flatten XML to CSV - ideal for EDRMs export.')
   parser.add_argument('--loc', help='Mandatory: Source folder of the XML.', default=False)

   start_time = time.time()

   if len(sys.argv) == 1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.loc:

      #location of the XML we want to extract from, #e.g.
      #xml_loc = "e:\transfer-folder\open-text\disp_20151111101907_1000\xml"
   
      #time script execution time roughly...
      t0 = time.clock()

      xml = read_xml(args.loc)
      document_count = xml.scan_xml()

      log = open('output.log', 'wb')
      log.write(str(document_count) + " files output" + "\n")
      log.write(str(time.clock() - t0) + " script execution time" + "\n")
   
   else:
      parser.print_help()
      sys.exit(1)

if __name__ == "__main__":      
   main()
