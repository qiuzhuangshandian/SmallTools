import os
import sys
# sys.path.append("J:\software\inkscape")
def convertSVGtoEMF(figname):
    figname = figname.split('.')[0]
    cmd = 'inkscape -z %s.svg -M %s.emf' % (figname, figname)
    print(cmd)
    os.system(cmd)
def main():
    filelist = os.listdir('.\\')
    for name in filelist:
        if name.split('.')[-1] == 'svg':
            convertSVGtoEMF(name)
    print('change ok!')
if __name__=='__main__':
    main()