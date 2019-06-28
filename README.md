# podcast_spider
使用泛用型播客客户端订阅其他音乐平台的节目

##支持平台
持喜马拉雅
网易云音乐

## 使用
填写config.json  
```json
[
    {
        "platform": "ximalaya",
        "albumid": "244444"
    },
    {
        "platform": "music163",
        "albumid": "968099"
    }
]
```
albumid为专辑页面的网页地址的最后一串数字  
例：https://www.ximalaya.com/erciyuan/7382293/  
albumid = *7382293*


运行
```
$ python run_sprider.py
```

