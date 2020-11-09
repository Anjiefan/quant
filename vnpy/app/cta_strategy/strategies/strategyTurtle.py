

if __name__ == '__main__':
    # _*_ encoding:utf-8 _*_
    import requests
    import datetime
    import json
    import re

    time1 = "2020-10-20"
    time2 = "2020-11-06"
    time1 = datetime.datetime.strptime(time1, '%Y-%m-%d').strftime('%Y-%m-%d')
    time2 = datetime.datetime.strptime(time2, '%Y-%m-%d').strftime('%Y-%m-%d')


    def luowen():
        url = "https://openapi.mysteel.com/zs/newprice/getChartMultiCity.ms?callback=callback&catalog=%25E8%259E%25BA%25E7%25BA%25B9%25E9%2592%25A2_%3A_%25E8%259E%25BA%25E7%25BA%25B9%25E9%2592%25A2&city=%25E6%2588%2590%25E9%2583%25BD&spec=HRB400%252020MM_%3A_HRB400_20MM&startTime=" + time1 + "&endTime=" + time2 + "&_=1604845106805"
        a = requests.get(url)
        print(a.text)


    def rezhaban(time1, time2):
        url = "https://openapi.mysteel.com/zs/newprice/getChartMultiCity.ms?callback=callback&catalog=%25E7%2583%25AD%25E8%25BD%25A7%25E6%259D%25BF%25E5%258D%25B7_%3A_%25E7%2583%25AD%25E8%25BD%25A7%25E6%259D%25BF%25E5%258D%25B7&city=%25E6%2588%2590%25E9%2583%25BD&spec=4.75_%3A__4.75%25E7%2583%25AD%25E8%25BD%25A7%25E6%259D%25BF%25E5%258D%25B7&startTime=" + time1 + "&endTime=" + time2 + "&_=1604847139035"
        a = requests.get(url)
        return a

    text=re.findall('\((.*)\)', rezhaban(time1, time2).text)

    print(json.loads(text[0]))