from get_images import *
page_random = range(1, 10)
main_url = 'https://www.zcool.com.cn/'
for page_n in page_random:
    demo = SpiderImages()
    page_url = demo.next_page(main_url, page_n)
    demo.get_images(page_url, page_n)
    print('第%s页图片下载完毕' % page_n)
print('图片下载完毕')
