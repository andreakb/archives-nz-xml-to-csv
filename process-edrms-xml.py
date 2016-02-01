import os
import argparse
import sys
import time
from ReadXMLClass import read_xml
from OpenTextClass import HandleOpenTextXML


# xml_handler needs to implement:
#      self.header = self.xml_handler.csv_columns(...)   [LIST]
#      self.row_dict = self.xml_handler.csv_rows(...)    [DICT]
#      self.xml_handler.xml_to_csv(...)                  [FUNCTION]
#
global XML_HANDLER
XML_HANDLER = HandleOpenTextXML()
      
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

      xml = read_xml(args.loc, XML_HANDLER)
      document_count = xml.scan_xml()

      log = open('output.log', 'wb')
      log.write(str(document_count) + " files output" + "\n")
      log.write(str(time.clock() - t0) + " script execution time" + "\n")
   
   else:
      parser.print_help()
      sys.exit(1)

if __name__ == "__main__":      
   main()
