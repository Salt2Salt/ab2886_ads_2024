def logString(header, block):
  """Indents block and adds an unindented header"""
  if block[0] != '\n': block = '\n' + block
  return header + block.replace('\n', '\n|  ')