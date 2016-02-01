# archives-nz-xml-to-csv
Code to convert EDRMS XML to CSV

Current version outputs to two streams (file data on stdout, and folder data on stderr) and a file, output.log.

To run:

    python process-edrms-xml.py --loc "z:\path-to-xml\xml' > file-object-data.csv 2> business-classification-data.csv

Where 'xml' is a directoy.

### New XML handlers

There is only a certain amount I can do to counter the issue of rubbish-in-rubbish-out. The following function helps: https://github.com/exponential-decay/archives-nz-xml-to-csv/blob/master/ReadXMLClass.py#L34

To create a new handler, simply implement the following things in your handler class:

    csv_columns - a list for your columns so that they are ordered on output
    csv_rows - a dict duplicating your column headers and with blank values - you'll populate this with xml data
    xml_to_csv() - a function reading the elements and attributes of the XML - you will need to implement its traversal properly

The calling class will do the following:

    self.header = self.xml_handler.csv_columns(...)   [LIST]
    self.row_dict = self.xml_handler.csv_rows(...)    [DICT]
    self.xml_handler.xml_to_csv(...)                  [FUNCTION]

In the primary script (entry point) add your class to the imports (example below) and then change the handler value to your class name, e.g. this for OpenText:

    from OpenTextClass import HandleOpenTextXML

    global XML_HANDLER
    XML_HANDLER = HandleOpenTextXML()

The script tries to protect as best as possible but you will still need to rely on implementing things sensibly. 

Happy coding! 
      
### License

Copyright (c) 2016 

This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.

Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.

This notice may not be removed or altered from any source distribution.
