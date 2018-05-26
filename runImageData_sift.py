import psycopg2
import os
import logging
import datetime
from siftImage import cmpSiftImage


def LogInit():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'Image_%s.log'%datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)

    # 文件
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    # 标准输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger


def runImageSift(dir):

    conn = psycopg2.connect(database="ircloud_micprogram", user="ir_user", password="CsiabyAnmqY#Up9w", host="113.200.91.99", port="15432")
    cur = conn.cursor()
    cur2 = conn.cursor()

    logger = LogInit()

    cur.execute("SELECT path FROM public.wx_miniapp_info")
    rows = cur.fetchall()

    for root,dirs,files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root,file)
            print("sourceFilePath:%s,suffix:%s"%(file_path,file_path[-2:]))
            if file_path[-2:]=='rd':
                continue
            filekey=file.split(".")[0]
            # all rows in table
            for i in rows:
                red = i[0]
                #print("mappingFilePath:",red)
                if not red:
                    continue
                red = "/Users/zhenjietang/Downloads/Image_compare/xiao_chenxu2.png"
                result = cmpSiftImage(file_path,red)
                if result >= 1.00:
                    newsql="UPDATE public.temp_wx_download SET sift_mapping_path='%s',sift_ratio='%s' WHERE id='%s';" % (red,result,filekey)
                    print("similar='%.2f',newsql='%s'" % (result,newsql))
                    cur2.execute(newsql)
                    conn.commit()
                    logger.info("filekey:" + filekey + ",dbfile:" + red + ",result:" + str(result) + ", update DB success!")
                    break
            logger.info("filekey:" + filekey +",rawfilepath process:"+file_path)

    cur.close()
    cur2.close()
    conn.close()


if __name__ == '__main__':
    runImageSift('/Users/zhenjietang/Downloads/Image_compare/onefile')
