
with open('gene.csv') as f:
    g = open('genes.sql', 'w')
    for line in f:
        attrs = line.split('~')
        print(attrs[0])
        g.write('INSERT INTO gene VALUES ("{0}","{1}","{2}","{3}","{4}","{5}",0);\n'.format(attrs[0],attrs[1],attrs[2],attrs[3],attrs[4],attrs[5]))