class XMLHandlerFunctions:

   def __gettext__(self, node):
      nodeval = ''
      if node is not None:
         nodeval = node.text
      return nodeval