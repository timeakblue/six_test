class RepositoryError(Exception):
  '''base class for all repository errors '''
  pass

class NotFoundError(RepositoryError):
  '''requested entity not found '''
  pass

class InvalidOperationError(RepositoryError):
  '''business rule violated '''
  pass
