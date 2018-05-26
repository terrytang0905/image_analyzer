import psycopg2
import os
from cvHash import cmpCVImage


conn = psycopg2.connect(database="ircloud_micprogram", user="ir_user", password="CsiabyAnmqY#Up9w", host="113.200.91.99", port="15432")
cur = conn.cursor()
cur2 = conn.cursor()

dir = '/data1/miniapp_image/wechat_image'
#dir = '/Users/zhenjietang/Documents/workspace/newroad/Learn-to-identify-similar-images/image_src'
#mapping_dir = '/Users/zhenjietang/Documents/workspace/newroad/Learn-to-identify-similar-images/image_mapping'

cur.execute("SELECT path FROM public.wx_miniapp_info")
rows = cur.fetchall()

for root,dirs,files in os.walk(dir):
    for file in files:
        file_path = os.path.join(root,file)
        print("sourceFilePath:",file_path)
        filekey=file.split(".")[0]
        # all rows in table
        for i in rows:
            red = i[0]
            #print("mappingFilePath:",red)
            if not red:
                continue
            result = cmpCVImage(file_path,red)
            #print("accuracy:", result)
            if result <= 10 and result>=0:
                newsql="UPDATE public.temp_wx_download SET new_mapping_path='%s',sim_acc='%s' WHERE id='%s';" % (red,result,filekey)
                print("similar='%d',newsql='%s'" % (result,newsql))
                cur2.execute(newsql)
                break
        conn.commit()

cur.close()
conn.close()