import pygame as pg
import numpy as np
from xml.dom.minidom import Document

PIECE_NAME=['board',"rk", "ra", "rb", "rn", "rr", "rc", "rp", "bk", "ba", "bb", "bn", "br", "bc", "bp",]
def init():
    pg.init()
    return pg.display.set_mode([600,600])
    

def gen(win):
    win.fill(np.random.randint(0,255,[3]))
    labels=[]
    
    xys=[np.random.randint(20,200,[2])]
    for i in range(10):
        for j in range(11):
            if(np.random.choice([True,False])):
                xy=np.array([i*60,j*60])+np.random.randint(0,15,[2])
                xys.append(xy)
    
    
    for i in range(len(xys)):
        if i==0:
            bd=pg.image.load('images/'+PIECE_NAME[i]+'.gif')
        else:
            bd=pg.image.load('images/'+PIECE_NAME[i%(len(PIECE_NAME)-1)+1]+'.gif')
        
        wh=np.array(bd.get_size())*(np.random.ranf()*0.3+0.7)
        wh=wh.astype('int32')
        bd=pg.transform.scale(bd,wh)
        xy=xys[i]        
        win.blit(bd,xy)    
        labels.append([xy[0],xy[1],xy[0]+wh[0],xy[1]+wh[1],PIECE_NAME[i if i==0 else i%(len(PIECE_NAME)-1)+1]])
    pg.display.flip()
#     print(labels)
    return labels


def docxml(labels=[[26, 91, 447, 566, 'board'], [7, 125, 52, 170, 'ra']],name='chess_'+str(0)):
    ##default is only for test----
    doc = Document()
    order = doc.createElement("annotation")
    doc.appendChild(order)
    
    filenam=doc.createElement('filename')
    filenam.appendChild(doc.createTextNode(name+'.jpg'))
    folder=doc.createElement('folder')
    folder.appendChild(doc.createTextNode('RSDS2016'))
    order.appendChild(filenam)
    order.appendChild(folder)
    
    obj1=['object','bndbox','xmin','xmax','ymin','ymax','difficult','pose','name','truncated']
    def obj(lb):
        obj=[doc.createElement(x) for x in obj1]
        obj[0].appendChild(obj[1])
        for i in range(2,6):
            obj[1].appendChild(obj[i])
        for i in range(6,10):
            obj[0].appendChild(obj[i])
        for i in range(4):
            obj[2+i].appendChild(doc.createTextNode(str(lb[i]))) 
        obj[-2].appendChild(doc.createTextNode(lb[-1]))
        obj[-1].appendChild(doc.createTextNode('1'))
        obj[-3].appendChild(doc.createTextNode('Left'))
        obj[-4].appendChild(doc.createTextNode('0'))
        
        order.appendChild(obj[0])
        
    for i in range(len(labels)):
        obj(labels[i])
        
    
    
    '''
    <object>
        <bndbox>
            <xmin>910</xmin>
            <ymin>306</ymin>
            <ymax>403</ymax>
            <xmax>1008</xmax>
        </bndbox>
        <difficult>0</difficult>
        <pose>Left</pose>
        <name>aircraft</name>
        <truncated>1</truncated>
    </object>
    <filename>aircraft_100.jpg</filename>
    '''    
    f = open('file/xml/'+name+'.xml', 'w')
    doc.writexml(f, indent='', newl='\n', addindent='\t', encoding='utf-8')
    f.close()

import os
if __name__ == '__main__':
    win=init()
    if True:
        os.makedirs('file/JPEGImages')
        os.makedirs('file/xml')
    for i in range(400,500):
        docxml(gen(win),'chess_'+str(i))
        pg.image.save(win,'file/JPEGImages/chess_'+str(i)+'.jpg')
    pg.display.quit()


