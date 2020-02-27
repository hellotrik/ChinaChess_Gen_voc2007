import os
import re
import uuid
import requests

def download_image(key_word, download_max):
    download_sum = 0
    str_gsm = '00'
    save_path = '/home/aistudio/data/face_image' + '/' + key_word
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    while download_sum < download_max:
        if download_sum >= download_max:
            break
        str_pn = str(download_sum)
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
              'word=' + key_word + '&pn=' + str_pn + '&gsm=' + str_gsm + '&ct=&ic=0&lm=-1&width=0&height=0'
        
        try:
            result = requests.get(url, timeout=30).text
            img_urls = re.findall('"objURL":"(.*?)",', result, re.S)
            if len(img_urls) < 1:
                break
            for img_url in img_urls:
                img = requests.get(img_url, timeout=30)
                img_name = save_path + '/' + str(uuid.uuid1()) + '.jpg'
                print('\r正在下载 %s 的第 %d 张图片...' % (key_word, download_sum),end='')
                
                with open(img_name, 'wb') as f:
                    f.write(img.content)
                with open('image_url_list.txt', 'a+', encoding='utf-8') as f:
                    f.write(img_name + '\t' + img_url + '\n')
                download_sum += 1
                if download_sum >= download_max:
                    break
        except Exception as e:
            print('【错误】当前图片无法下载，%s' % e)
            download_sum += 1
            continue
    print('下载完成')
    
def down(max_sum=40,file='list.txt'):
    f=open(file,'r')
    list=f.read().split('\n')
    f.close()
    print(list)
    for i in list:
        download_image(i,max_sum)
    print('全部下载完成')
    
if __name__ == '__main__':
    max_sum = 40
    # 获取明星的名字
    if False:
        key_word = str(input('name for search q 2 quit: '))
        while key_word !='q':
            # 使用明星的名字开始下载图片
            download_image(key_word, max_sum)
            print('全部图片以下载完成')
            key_word = str(input('name for search q 2 quit: '))
    else:
        down(max_sum)
        
        
    
    
