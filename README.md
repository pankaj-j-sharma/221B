# 221B
Python module for parsing excel file and also implementing custom utility
few changes done to ttl\Lib\site-packages\xlrd\xlsx.py to remove deprecated warnings 

D:\Python\ttl\lib\site-packages\xlrd\xlsx.py:39: DeprecationWarning: defusedxml.cElementTree is deprecated, import from defusedxml.ElementTree instead.
  try: import defusedxml.cElementTree as ET
D:\Python\ttl\lib\site-packages\xlrd\xlsx.py:266: DeprecationWarning: This method will be removed in future versions.  Use 'tree.iter()' or 'list(tree.iter())' instead.
  for elem in self.tree.iter() if Element_has_iter else self.tree.getiterator():
D:\Python\ttl\lib\site-packages\xlrd\xlsx.py:312: DeprecationWarning: This method will be removed in future versions.  Use 'tree.iter()' or 'list(tree.iter())' instead.
  for elem in self.tree.iter() if Element_has_iter else self.tree.getiterator():
  
