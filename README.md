# Vika

[Vika](https://vika.cn) Python SDK [WIP]

## 快速开始

### 环境要求

python3.6 + 

### 安装

```shell
pip install vika
# or
pipenv install vika
```

### 获取 API TOKEN

访问维格表的工作台，点击左下角的个人头像，进入「用户中心 > 开发者配置」。点击生成Token(首次使用需要绑定邮箱)。

### 使用

下面是一些常见的用法。详细的使用文档请参考 API 面板（进入任意一张数表, cmd + shift + p 打开 API 面板）

```python
from vika import Vika
vika = Vika("your api_token")


dst = vika.datasheet("dstt3KGCKtp11fgK0t")
# 下面这种写法也可以哦，会自动解析表格 id，忽略视图 id。
# dst = vika.datasheet("https://vika.cn/space/spcxcvEBLXf7X/workbench/dstt3KGCKtp11fgK0t/viwmKtRiYcPfk")

# 创建记录
record = dst.records.create({"title":"new record from Python SDK"}):
print(record.title)
#print(record.标题)

# 批量创建记录
records = dst.records.bulk_create([
  {"title":"new record from Python SDK"},
  {"title":"new record from Python SDK2"}
])

# 更新单个字段值
record.title = "new title"
print(record.title)
# "new title"

# 更新多个字段值
record.update({
  "title":"new title",
  "other_field": "new value",
})

# 过滤记录
songs = dst_songs.records.filter(artist="faye wong")
for song in songs:
    print(song.title)

# 批量更新一批记录
dst_tasks.records.filter(title=None).update(status="Pending")

# 获取单条记录
book = dst_book.records.get(ISBN="9787506341271")
print(book.title)

# 删除符合过滤条件的一批记录
dst.records.filter(title=None).delete()
```

## 开发测试

复制测试模板到自己的空间站，每次测试时，保证表中只有一条 title = "无人生还" 的记录

+ [正式环境测试模板](https://vika.cn/share/shrTZC8odwrWl95Gil2Dm)
+ [内部环境测试模板](https://integration.vika.ltd/share/shr2BYKJ5QysFK9YoAws1)

``` shell
cp .env.example .env
```

配置测试所需的环境变量

``` shell
# 安装依赖
pipenv install --pre
python -m unittest test
```

## 更新日志

参见: [releases](https://github.com/vikadata/vika.py/releases)

## 相关项目

+ [JavaScript SDK](https://github.com/vikadata/vika.js)
+ [Golang SDK](https://github.com/vikadata/vika.go)
+ [PHP SDK](https://github.com/vikadata/vika.php)

## FAQ

### 可以拿到表格的字段类型（meta）信息吗？

目前不可以，后续 REST API 升级会暴露表格 meta 信息

### 可以自动单多选选项吗？
```
record.tags = ["目前 tags 字段中不存在的选项"]
```
目前不可以，你只能赋值已经存在的选项。后续会支持 :D