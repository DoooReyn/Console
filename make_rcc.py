import os
import subprocess

QRC = 'resources.qrc'
DIRS = (('img', 'statics/img'),)


def write_rcc():
    f = open(QRC, 'w+')
    f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource>\n')

    for d in DIRS:
        for item in os.listdir(d[1]):
            f.write('<file alias="{0}/{1}">statics/{0}/{1}</file>\n'.format(d[0], item))

    f.write(u'</qresource>\n</RCC>')
    f.close()


if __name__ == '__main__':
    write_rcc()

    pipe = subprocess.Popen(r'pyrcc5 -o ./cclog/resources.py resources.qrc', stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE, creationflags=0x08)
