import sys 
from XMLHandler import XMLHandlerFunctions
import xml.etree.ElementTree as etree

class HandleOpenTextXML:

   def __init__(self):
      self.writeItemLevelXML = False

   xmlhelper = XMLHandlerFunctions()

   #have we written the columns for the error stream?
   error_csv_written = False

   #report on unique paths only... 
   dir_seen = []

   #how many objects do we output data for
   doc_count = 0

   #top row of csv
   #LIST: Ordered so we can control column ordering
   csv_columns = ['FileID', 'FileVersion', 'FileName', 'Path', 'Doc.CreateDate','Doc.DataID','Doc.Link','Doc.MimeType',
                  'Doc.ModifyDate','Doc.Name','Doc.Subtype','multi.description',
                     'multi.language','multi.name','rmmeta.comment','rmmeta.ClassName',
                        'rmmeta.FileNumber','rmmeta.RSI','rmmeta.RecordDate','rmmeta.Status',
                           'rmmeta.StatusDate','rmmeta.Official','rmmeta.Essential','rmmeta.Storage',
                              'rmmeta.Subject','rmmeta.Addressees','rmmeta.OrigOrg','rmeta.AuthOrig','rmmeta.OtherAddressees',
                                 'rmmeta.CyclePeriod','rmmeta.NextReviewDate','rmmeta.ReceivedDate','CatAtt.Context.LegacyID','CatAtt.Context.Role',
                                    'CatAtt.Context.Branch','CatAtt.Context.WorkUnit','CatAtt.Context.Organisation','CatAtt.Context.Language']
   
   #DICT: unordered so we control column ordering using self.header
   csv_rows = {'FileID':'', 'FileVersion':'', 'FileName':'', 'Path':'', 'Doc.CreateDate':'','Doc.DataID':'','Doc.Link':'','Doc.MimeType':'',
               'Doc.ModifyDate':'','Doc.Name':'','Doc.Subtype':'','multi.description':'',
                  'multi.language':'','multi.name':'','rmmeta.comment':'','rmmeta.ClassName':'',
                     'rmmeta.FileNumber':'','rmmeta.RSI':'','rmmeta.RecordDate':'','rmmeta.Status':'',
                        'rmmeta.StatusDate':'','rmmeta.Official':'','rmmeta.Essential':'','rmmeta.Storage':'',
                           'rmmeta.Subject':'','rmmeta.Addressees':'','rmmeta.OrigOrg':'','rmeta.AuthOrig':'','rmmeta.OtherAddressees':'',
                              'rmmeta.CyclePeriod':'','rmmeta.NextReviewDate':'','rmmeta.ReceivedDate':'','CatAtt.Context.LegacyID':'','CatAtt.Context.Role':'',
                                 'CatAtt.Context.Branch':'','CatAtt.Context.WorkUnit':'','CatAtt.Context.Organisation':'','CatAtt.Context.Language':''} 
                                 
   def __opentextPathSection__(self, path_section, candidate_file_path):
   
      #write errors as a CSV... 
      if self.error_csv_written is False:
         sys.stderr.write('"dirname","subtype","description","aggregate_path"' + "\n")
         self.error_csv_written = True

      for level in path_section:
         level_data = ''
         
         dirname = level.attrib['Name'].replace('/', '-')
         subtype = level.attrib['Subtype'].replace('/', '-')
         
         candidate_file_path = candidate_file_path + "\\" + dirname
         
         if dirname not in self.dir_seen:
            self.dir_seen.append(dirname)
            
            level_data = '"' + dirname + '","' + subtype + '"'
            
            for comments in level: 
               if comments.tag.lower() == 'multilingual':
                  description = str(comments.attrib['description'])
                  level_data = level_data + ',"' + description + '"'
            
            level_data = level_data + ',"' + candidate_file_path.lstrip('\\') + '",'
            sys.stderr.write(str(level_data.strip(',')) + "\n")
            
      return candidate_file_path

   def __writeItemLevelXML__(self, element, objectname):
      fname = ('xml_output\\' + str(''.join(objectname.split('.')[:-1])) + '.xml')
      et = etree.ElementTree(element)
      et.write(fname, encoding="utf-8", xml_declaration=True)
   
   def __opentextDocumentSection__(self, element, candidate_file_path, row_dict):
      
      #create a new CSV row per Doc discovered
      row = dict(row_dict)
   
      self.doc_count+=1
      
      doc_element = element

      docID = element.attrib['Link'].split('\\', 1)[1].rsplit('.', 2)[0]
      docName = element.attrib['Link'].split('\\', 1)[1]
      version = docName.rsplit('.', 2)[1]
      
      if self.writeItemLevelXML == True:
         self.__writeItemLevelXML__(element, docName)
      
      '''sys.stderr.write("Found document metadata." + "\n")
      sys.stderr.write("ID: " + str(docID) + "\n")
      sys.stderr.write("Name: " + str(docName) + "\n")
      sys.stderr.write("Version: " + str(version) + "\n")
      sys.stderr.write("Path: " + candidate_file_path + "\n")'''
      
      row['FileID'] = docID
      row['FileName'] = docName
            
      #only output a version if we've an integer
      #if isinstance( version, int ):
      try: 
         version = int(version)
         row['FileVersion'] = str(version)
      except ValueError as e:
         row['FileVersion'] = ''
      
      row['Path'] = candidate_file_path.lstrip('\\') + "\\"
      
      row['Doc.CreateDate'] = element.attrib['CreateDate']
      
      row['Doc.DataID'] = element.attrib['DataID']
      row['Doc.Link'] = element.attrib['Link']
      row['Doc.MimeType'] = element.attrib['MimeType']
      row['Doc.ModifyDate'] = element.attrib['ModifyDate']
      row['Doc.Name'] = element.attrib['Name']
      row['Doc.Subtype'] = element.attrib['Subtype']
   
      for subelement in doc_element:
         name = subelement.tag
         
         if name.lower() == 'multilingual':
            row['multi.description'] = subelement.attrib['description']
            row['multi.language'] = subelement.attrib['language']
            row['multi.name'] = subelement.attrib['name']
         
         if name.lower() == 'rmmeta':
            row['rmmeta.comment'] = self.xmlhelper.__gettext__(subelement.find('Comment'))
            row['rmmeta.ClassName'] = self.xmlhelper.__gettext__(subelement.find('ClassName'))
            row['rmmeta.FileNumber'] = self.xmlhelper.__gettext__(subelement.find('FileNumber'))
            row['rmmeta.RSI'] = self.xmlhelper.__gettext__(subelement.find('RSI'))
            row['rmmeta.RecordDate'] = self.xmlhelper.__gettext__(subelement.find('RecordDate'))
            row['rmmeta.Status'] = self.xmlhelper.__gettext__(subelement.find('Status'))
            row['rmmeta.StatusDate'] = self.xmlhelper.__gettext__(subelement.find('StatusDate'))
            row['rmmeta.Official'] = self.xmlhelper.__gettext__(subelement.find('Official'))
            row['rmmeta.Essential'] = self.xmlhelper.__gettext__(subelement.find('Essential'))
            row['rmmeta.Storage'] = self.xmlhelper.__gettext__(subelement.find('Storage'))
            row['rmmeta.Subject'] = self.xmlhelper.__gettext__(subelement.find('Subject'))
            row['rmmeta.Addressees'] = self.xmlhelper.__gettext__(subelement.find('Addressees'))
            row['rmmeta.OrigOrg'] = self.xmlhelper.__gettext__(subelement.find('OrigOrg'))
            row['rmmeta.AuthOrig'] = self.xmlhelper.__gettext__(subelement.find('AuthOrig'))
            row['rmmeta.OtherAddressees'] = self.xmlhelper.__gettext__(subelement.find('OtherAddressees'))
            row['rmmeta.CyclePeriod']= self.xmlhelper.__gettext__(subelement.find('CyclePeriod'))
            row['rmmeta.NextReviewDate'] = self.xmlhelper.__gettext__(subelement.find('NextReviewDate'))
            row['rmmeta.ReceivedDate'] = self.xmlhelper.__gettext__(subelement.find('ReceivedDate'))
         
         if name.lower() == 'catsattsmeta':
            cats = subelement
            for cat in cats:
               if cat.attrib['AttName'] == 'Legacy ID':
                  row['CatAtt.Context.LegacyID'] = self.xmlhelper.__gettext__(cat)
               if cat.attrib['AttName'] == 'Role':
                  row['CatAtt.Context.Role'] = self.xmlhelper.__gettext__(cat)
               if cat.attrib['AttName'] == 'Branch':
                  row['CatAtt.Context.Branch'] = self.xmlhelper.__gettext__(cat)
               if cat.attrib['AttName'] == 'Work Unit':
                  row['CatAtt.Context.WorkUnit'] = self.xmlhelper.__gettext__(cat)
               if cat.attrib['AttName'] == 'Organisation':
                  row['CatAtt.Context.Organisation'] = self.xmlhelper.__gettext__(cat)
               if cat.attrib['AttName'] == 'Language':
                  row['CatAtt.Context.Language'] = self.xmlhelper.__gettext__(cat)
      return row

   def xml_to_csv(self, xml_iter, row_dict, rows):
      #one path per XML we're interested in... 
      #clear and recreate here...
      candidate_file_path = ""
   
      for element in xml_iter:
         name = element.tag

         #extract path data (not object data)
         if name.lower() == 'path':
            candidate_file_path = self.__opentextPathSection__(element, candidate_file_path)
         
         #extract object information (noth path information)
         if name.lower() == 'doc':
            row = self.__opentextDocumentSection__(element, candidate_file_path, row_dict)
            rows.append(row)
      
      return self.doc_count