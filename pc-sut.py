#coding:utf-8

import sys
import urllib
import cookielib
import urllib2
import re
import json
#import image
#import cStringIO
#from PIL import Image

reload(sys)
sys.setdefaultencoding("utf8")

loginurl='http://jwc.sut.edu.cn/ACTIONLOGON.APPPROCESS?mode=4'

class Sutjwcxx(object):

    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.yzmurl='http://jwc.sut.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS'
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def login (self):
        #img = cStringIO.StringIO(urllib2.urlopen(self.yzmurl).read())
        picture = self.opener.open(self.yzmurl).read()
        local = open('f:/test/image.jpg', 'wb')
        local.write(picture)
        local.close()
        #image = Image.open(img)
        #image.show()
        yzm = raw_input('输入验证码： ')
        loginmessage=urllib.urlencode({
            'WebUserNO':self.name,
            'Password':self.password,
            'Agnomen':yzm,
            'submit.x': '30',
            'submit.y': '20'
        })
        headers={
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            'Accept - Language':'zh - CN, zh;q = 0.8',
            'Connection':'keep - alive',
            'Content-Type':'text/html;charset=GBK',
            'User - Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        }
        req = urllib2.Request(loginurl, loginmessage)
        response = self.opener.open(req)
        page = response.read().decode("GBK")
        print page
        if page.find(u"错误的用户名或者密码<br>") > 0:
            print "Error username or password."
            return
        if page.find(u"请输入正确的附加码<br>") > 0:
            print "Error Agnomen."
            return
        print 'Login Sucess!'
    def getxx(self):
        url='http://jwc.sut.edu.cn/ACTIONQUERYSTUDENT.APPPROCESS'
        response = self.opener.open(url)
        page1 = response.read().decode("GBK")
        reg_no=u'<td width="17%" height="30" align="left" valign="middle" nowrap class="color-row">([0-9]{9}|[0-9]{9}L{0,})</td>'
        com_no = re.compile(reg_no)
        print re.findall(com_no, page1)
        reg_year = u'<td width="17%" height="30" align="left" valign="middle" nowrap class="color-row">([0-9]{4})</td>'
        com_year=re.compile(reg_year)
        print re.findall(com_year, page1)
        reg_sex = u'<td width="17%" height="30" align="left" valign="middle" nowrap class="color-row">(男|女)</td>'
        com_sex = re.compile(reg_sex)
        a=json.dumps(re.findall(com_sex, page1), encoding='UTF-8', ensure_ascii=False)
        print a
        reg_name_nation = u'<td width="17%" height="30" align="left" valign="middle" nowrap class="color-row">([\u4e00-\u9fa5]{2,})</td>'
        com_name_nation = re.compile(reg_name_nation)
        b=json.dumps(re.findall(com_name_nation, page1), encoding='UTF-8', ensure_ascii=False)
        print b
        reg_major = u'<td width="28%" height="30" align="left" valign="middle" nowrap class="color-row">([\u4e00-\u9fa5()]{2,})</td>'
        com_major = re.compile(reg_major)
        c=json.dumps(re.findall(com_major, page1), encoding='UTF-8', ensure_ascii=False)
        print c
        reg_class = u'<td height="31" height="30" align="left" valign="middle" nowrap class="color-row">([\u4e00-\u9fa5()]{2,}[0-9]{2,}班)</td>'
        com_class = re.compile(reg_class)
        d=json.dumps(re.findall(com_class, page1), encoding='UTF-8', ensure_ascii=False)
        print d
        reg_city = u'<td height="36" colspan="2" align="left" valign="middle" nowrap class="color-row">([\u4e00-\u9fa5]{2,})</td>'
        com_city = re.compile(reg_city)
        e=json.dumps(re.findall(com_city, page1), encoding='UTF-8', ensure_ascii=False)
        print e
        reg_sid = u'<td height="33" colspan="2" align="left" valign="middle" nowrap class="color-row">([0-9xX]{18})</td>'
        com_sid = re.compile(reg_sid)
        print re.findall(com_sid, page1)




if __name__ == '__main__':
    username = 'xxxxxxxxx'
    password = 'xxxxxx'
    userlogin = Sutjwcxx(username, password)
    userlogin.login()
    userlogin.getxx()