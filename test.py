from tempfile import NamedTemporaryFile

f = NamedTemporaryFile(prefix='test-',mode='w', dir=r'C:\Users\fluky\Desktop')
f.write('hello')
print(f.name)
f.close()