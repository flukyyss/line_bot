from tempfile import NamedTemporaryFile

f = open(file=r'C:\Users\fluky\Desktop\New folder (2)\New folder\static\tmp\info.txt', mode="r")
print(f.read())
f.close()