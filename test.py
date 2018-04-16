from tempfile import NamedTemporaryFile

f = NamedTemporaryFile(prefix='test-',mode='w+', dir=r'C:\Users\fluky\Desktop',delete=False)
f.write('hello')
print(f.name)
print('hey')
print(f.read())
f.close()