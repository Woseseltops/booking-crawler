import booking_crawler as b

lines = open('output_nl.txt','r').readlines();
newlines = [];

for i in lines:
    i = i[:-1];
    exec('i = \''+i+'\'');

    for r in [('&#47;','/'),('&#39;','\'')]:
        i = i.replace(r[0],r[1]);

    newlines.append(b.iso_to_utf(i));

open('cl_output_nl.txt','w').write(''.join(newlines));
