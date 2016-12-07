#!/bin/sh
# 获得时间戳
date=`date +%Y-%m-%d`
# 日志文件命名
logFile="yoho_""$date"".log"
# 爬取
cd ~/Projects2016/paper/spider
~/anaconda/bin/scrapy crawl yoho --logfile=$logFile