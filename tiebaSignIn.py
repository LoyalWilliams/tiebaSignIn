#coding=utf-8
import time
from selenium import webdriver
from lxml import etree


class tiebaSpider():
    def __init__(self,url):
        '''
        初始化
        :param url:
        '''
        self.url=url
        driver = webdriver.Chrome()
        self.driver=driver
        driver.delete_all_cookies()
        driver.get(url)
        html = driver.page_source
        self.html=html
        time.sleep(1)
        selector = etree.HTML(html)
        self.selector=selector

    def logIn(self,useName,passWord):
        '''
        登录模块，需要用户名和密码
        :param useName:
        :param passWord:
        :return:
        '''
        driver=self.driver
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="com_userbar"]/ul/li[4]/div/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys(useName)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys(passWord)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()
        time.sleep(2)

    def signIn(self):
        '''
        循环贴吧地址，签到
        :return:
        '''
        driver=self.driver
        tiebaList = self.getBaList()
        time.sleep(2)
        for tiebaUrl in tiebaList:
            driver.get(tiebaUrl)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="signstar_wrapper"]/a').click()
            time.sleep(2)

    def getBaList(self):
        '''
        这里是获取贴吧地址的方法，返回的是一个列表
        这里发现我写的这个方法，又调用了另一个方法，这其实是一种灵活的写法，
        因为可以把这个方法看做是一个接口，具体实现是调用别的方法，修改代码的时候可以很容易的修改，
        比如：我这里有2个获取贴吧列表的方法，我只需把self.getList1()改成return self.getList2()
        :return:
        '''
        # return self.getList1()
        return self.getList2()

    def getList1(self):
        '''
        获取关注的贴吧的地址列表
        :return:
        '''
        button = self.driver.find_element_by_xpath('//*[@id="forum_group_wrap"]/span/span[1]')
        time.sleep(3)
        button.click()
        time.sleep(3)
        html = self.driver.page_source
        selector = etree.HTML(html)
        tiebaList = selector.xpath("//div[@id='forum_group_wrap']/a/@href") + selector.xpath(
            '//*[@id="forumscontainer"]//a/@href')
        print len(tiebaList)
        return ['http://tieba.baidu.com'+ url for url in set(tiebaList) if url != '#']

    def getList2(self):
        l=[]
        with open('tiebaList.txt','r') as f:
            for line in f:
                l.append(line.strip())
        return l

    def saveBaList(self):
        '''
        把关注的贴吧地址列表保存到本地，这样就用每次都爬取地址了
        :return:
        '''
        with open('tiebaList.txt','w') as f:
            for list in self.getList1():
                f.write( list+'\n')

    def close(self):
        '''
        关掉浏览器
        :return:
        '''
        self.driver.quit()


def main():
    spider = tiebaSpider('http://tieba.baidu.com/home/main?id=7b9be5b08fe69fb3e9a39ee58f8ce9b1bc6f40&fr=userbar&red_tag=n3342692588')
    spider.logIn('账号','密码')
    spider.signIn()
    spider.close()


if __name__ == '__main__':
    main()