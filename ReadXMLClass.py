import os
import re
import sys
import xml.etree.ElementTree as etree

class read_xml:

   #handler for the XML
   xml_handler = ''
   
   #where the xml resides...
   xml_loc = ''
   
   def __init__(self, xml_loc, xml_handler):
   
      #initialize variables...
      self.xml_loc = xml_loc
   
      if self.__initiate_handler__(xml_handler) == True:
         self.xml_handler = xml_handler
      else:
         sys.exit("ERROR: Handler not configured correctly.")

      #initial output...
      self.__csv_structure__()
      header_row = ''
      if os.path.isdir(self.xml_loc):
         for title in self.header:
            header_row = header_row + '"' + title + '",'
         sys.stdout.write(header_row.rstrip(',') + "\n")
      else:
         sys.stderr.write("WARNING: Input directory " + self.xml_loc + " is not a directory.")

   def __initiate_handler__(self, xml_handler):
      configured = False
      #
      # xml_handler needs to implement:
      #      self.header = self.xml_handler.csv_columns(...)   [LIST]
      #      self.row_dict = self.xml_handler.csv_rows(...)    [DICT]
      #      self.xml_handler.xml_to_csv(...)                  [FUNCTION]
      #
      if "xml_to_csv" in dir(xml_handler):
         if "csv_columns" in dir(xml_handler) and "csv_rows" in dir(xml_handler):
            if type(xml_handler.csv_columns) is list and type(xml_handler.csv_rows) is dict:
               configured = True
      return configured

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
      for dir_paths, dir_names, filenames in os.walk(self.xml_loc):
         for f in filenames:
            if os.path.splitext(f)[1] == '.xml':
               
               #create full path and read XML
               #note: consider if we need to protect create-write-access dates
               fullpath = os.path.abspath(os.path.join(dir_paths, f))

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