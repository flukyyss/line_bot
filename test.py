from tempfile import NamedTemporaryFile

f = NamedTemporaryFile(prefix='test-',mode='r', dir=r'C:\Users\fluky\Desktop',delete=False)
print(f.name)
