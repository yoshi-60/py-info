#
# readline() 
with open('input.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.rstrip()
        print(line)
        line = f.readline()

# after 3.8
with open('input.txt', 'r') as f:
    while line := f.readline():
        line = line.rstrip()
        print(line)

# write
with open('output.txt', 'wt') as f:
    f.write('text output.\n')

#
f = open('output.txt', 'w')
f.write('text output.\n')
f.close()
