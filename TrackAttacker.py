#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
Program：TrackAttacker
Function：help people track the attacker
 
Version：Python3
Time：2021/3/24
Author：bywalks
Blog：http://www.bywalks.com
Github：https://github.com/bywalks
'''

import requests
import time
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from requests.packages import urllib3
import re
import json
import nmap
import sys

urllib3.disable_warnings()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie' : 'Hm_lvt_d5e9e87de330d4ceb8f78059e5df3182=1616638111; Hm_lpvt_d5e9e87de330d4ceb8f78059e5df3182=1616638111; eid=2c2dcde34fc9ec2b0b411655235dbe05'
}


banner = '''
  _______             _             _   _             _             
 |__   __|           | |       /\  | | | |           | |            
    | |_ __ __ _  ___| | __   /  \ | |_| |_ __ _  ___| | _____ _ __ 
    | | '__/ _` |/ __| |/ /  / /\ \| __| __/ _` |/ __| |/ / _ \ '__|
    | | | | (_| | (__|   <  / ____ \ |_| || (_| | (__|   <  __/ |   
    |_|_|  \__,_|\___|_|\_\/_/    \_\__|\__\__,_|\___|_|\_\___|_|   
                                   By Bywalks | V 1.0            
'''

#通过IP获取网站域名
def get_site_by_ip(ip):
    try:
        url = "https://site.ip138.com/"+str(ip)+"/"
        req = requests.get(url,timeout=3,headers=headers,verify=False)
        req.encoding = "utf-8"
        site=re.findall('<li><span\sclass="date">[\d\-\s]+</span><a\shref=".*?"\starget="_blank">(.*?)</a></li>',req.text) 
        if site != "":
            print("[+]Site:"+site[0])
            return site[0]
    except:
        pass

#通过IP获取地址        
def get_address_by_ip(ip):
    try:
        url = "https://www.ip138.com/iplookup.asp?ip="+str(ip)+"&action=2"
        req = requests.get(url,timeout=3,headers=headers,verify=False)
        req.encoding = "gbk"
        address=re.findall('"ASN归属地":"(.*?)",\s"iP段":',req.text) 
        if address != "":
            print("[+]Address:"+address[0])
    except:
        pass

#通过网站获取备案信息        
def get_beian_by_site(site):
    try:
        url = "https://www.beian88.com/home/Search"
        post_site = {'d': site}
        req = requests.post(url,data=post_site,timeout=3,headers=headers,verify=False)
        req.encoding = "utf-8"
        key=re.findall('"key":"(.*?)"}',req.text) 
        url1 = "https://www.beian88.com/d/" + key[0]
        requ = requests.get(url1,timeout=3,headers=headers,verify=False)
        requ.encoding = "utf-8"
        name=re.findall('<span class="field-value" id="ba_Name">(.*?)</span>',requ.text)
        if name[0] != "":
            #print("备案信息")
            webname=re.findall('<span class="field-value" id="ba_WebName">(.*?)</span>',requ.text) 
            print("[+]网站名称:"+webname[0]) 
            print("[+]主办单位名称:"+name[0])
            type=re.findall('<span class="field-value" id="ba_Type">(.*?)</span>',requ.text) 
            print("[+]主办单位性质:"+type[0])
            license=re.findall('<span class="field-value" id="ba_License">(.*?)</span>',requ.text) 
            print("[+]网站备案/许可证号:"+license[0])        
        
    except:
        pass

#通过网站获取whois信息
def get_whois_by_site(site):
    try:
        url = "http://whois.4.cn/api/main"
        post_site = {'domain': site}
        req = requests.post(url,data=post_site,headers=headers,verify=False)
        json_data = json.loads(req.text)
        if json_data['data']['owner_name'] !="":
            #print("Whois信息")
            print("[+]域名所有者:"+json_data['data']['owner_name'])
            print("[+]域名所有者邮箱:"+json_data['data']['owner_email'])
            print("[+]域名所有者注册:"+json_data['data']['registrars'])
    except:
        pass

#通过ip查端口
def nmap_port(ip):
    n = nmap.PortScanner() 
    ip = "\""+ip+"\""
    n.scan(hosts=ip,arguments="-sV -p 22,80,90,443,1433,1521,3306,3389,6379,7001,7002,8000,8080,9090,9043,9080,9300")
    for x in n.all_hosts():
        if n[x].hostname() != "":
            print("[+]HostName: " + n[x].hostname())
        for y in n[x].all_protocols():
            print("[+]Protocols: " + y)
            for z in n[x][y].keys():
                if n[x][y][z]["state"] == "open":
                    print("[+]port: " + str(z) + " | name: " + n[x][y][z]["name"] + " | state: " + n[x][y][z]["state"])
                
def deal_url(url):
    print(url)
    get_address_by_ip(url)
    site = get_site_by_ip(url)
    if site != None:
        get_beian_by_site(site)
        get_whois_by_site(site)
    nmap_port(url)
    print("=========================================")    

def main():
    print(banner)
    print("[+]帮助小伙伴追踪Attacker的小工具")
    print("[+]使用方法1：python3 TrackAttacker.py")
    print("[+]使用方法2：python3 TrackAttacker.py all")
    print("[+]如果你第一次使用该工具，请看README.md")
    print("=========================================")
    url = "urls.txt"

    with open(url) as f:
        for url in f:
            url = url.replace('\n','')
            print(url)
            get_address_by_ip(url)
            site = get_site_by_ip(url)
            if site != None:
                get_beian_by_site(site)
                get_whois_by_site(site)
            if len(sys.argv)>1:
                if sys.argv[1]=="all":
                    nmap_port(url)
            print("=========================================")
           
if __name__=="__main__":
    #判断程序运行时间
    start = time.time()      
    main()
    end = time.time()
    print("The program spend time is %.3f seconds" %(end-start))            