# TrackAttacker V1.0 #

**TrackAttacker** 是一个HW时通过IP追踪攻击者指纹工具

TrackAttacker目前版本为1.0，已满足功能如下

* 1：IP查域名
* 2：IP查地址
* 3：IP查端口
* 4：IP查主机名
* 5：域名查备案
* 6：域名查Whois

------

### Install ###

python3 -m pip install -r requirements.txt

### 开始使用

* ##### **常规追踪**

```
python3 TrackAttack.py
```

* ##### 使用1个或多个规则，扫描文件中的所有目标

```
python BBScan.py --no-scripts --rule git_and_svn --no-check404 --no-crawl -f iqiyi.txt
```

使用 `git_and_svn` 文件中的规则，扫描 `iqiyi.txt` 文件中的所有目标，每一行一个目标

`--no-check404`  指定不检查404状态码

`--no-crawl` 指定不抓取子目录

通过指定上述两个参数，可显著减少HTTP请求的数量。

### 参数说明 ###

**如何设定扫描目标** 

	  --host [HOST [HOST ...]]
	                        该参数可指定1个或多个域名/IP
	  -f TargetFile         从文件中导入所有目标，目标以换行符分隔
	  -d TargetDirectory    从文件夹导入所有.txt文件，文件中是换行符分隔的目标
	  --network MASK        设置一个子网掩码(8 ~ 31)，配合上面3个参数中任意一个。将扫描
	  						Target/MASK 网络下面的所有IP

**HTTP扫描**

	  --rule [RuleFileName [RuleFileName ...]]
	                        扫描指定的1个或多个规则
	  -n, --no-crawl        禁用页面抓取，不处理页面中的其他链接
	  -nn, --no-check404    禁用404状态码检查
	  --full                处理所有子目录。 /x/y/z/这样的链接，/x/ /x/y/也将被扫描

**插件扫描**

	  --scripts-only        只启用插件扫描，禁用HTTP规则扫描
	  --script [ScriptName [ScriptName ...]]
	                        扫描指定1个或多个插件
	  --no-scripts          禁用插件扫描

**并发**

```
  -p PROCESS            扫描进程数，默认30。建议设置 10 ~ 50之间
  -t THREADS            单个目标的扫描线程数, 默认3。建议设置 3 ~ 10之间
```

**其他参数**

	  --timeout TIMEOUT     单个目标最大扫描时间（单位:分钟），默认10分钟
	  -md                   输出markdown格式报告
	  --save-ports PortsDataFile
	                        将端口开放信息保存到文件 PortsDataFile，可以导入再次使用
	  --debug               打印调试信息
	  -nnn, --no-browser    不使用默认浏览器打开扫描报告
	  -v                    show program's version number and exit

### 使用技巧

* **如何把BBScan当做一个快速的端口扫描工具使用？**

找到scripts/tools/port_scan.py，填入需要扫描的端口号列表。把文件移动到scripts下。执行

```
python BBScan.py --scripts-only --script port_scan --host www.baidu.com --network 16 --save-ports ports_80.txt
