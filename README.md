# Vika

[Vika](https://vika.cn) Python SDK 是对维格表 Fusion API 的官方封装，提供类似 Django ORM 风格的 API。

![demo](https://s1.vika.cn/space/2020/10/19/f75caf2a161b465facfd170598ea0934)

## 快速开始

### 环境要求

python3.6 + 

### 安装

```shell
pip install --upgrade vika
```

### 获取 API TOKEN

访问维格表的工作台，点击左下角的个人头像，进入「用户中心 > 开发者配置」。点击生成Token(首次使用需要绑定邮箱)。

### 使用

基础用法

```python
from vika import Vika
vika = Vika("your api_token")

dst = vika.datasheet("dstt3KGCKtp11fgK0t")
# 传入表格URL 会自动解析表格 id，忽略视图 id。
# dst = vika.datasheet("https://vika.cn/space/spcxcvEBLXf7X/workbench/dstt3KGCKtp11fgK0t/viwmKtRiYcPfk")

# 创建记录
record = dst.records.create({"title":"new record from Python SDK"})
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

# 附件字段更新
my_file = dst.upload_file(<本地或网络文件路径>)
record.files = [my_file]


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

### 字段映射

对于中文用户，表格的字段名通常是中文，虽然 Python 支持中文变量名，但是依然会出现中文字段名不符合变量规范的情况。因此你不得不回退到使用 fieldId 作为 key 的情况，致使代码可读性变差。

为了改善这种情况，Python SDK 提供了字段映射的功能。

| Bug 标题\!     | Bug状态 |
|----------------|---------|
| 登陆后页面崩溃 | 待修复  |
|                |         |


```python 
dst = vika.datasheet("dstt3KGCKtp11fgK0t",field_key_map={
  "title": "Bug 标题!",
  "state": "Bug状态",
})

record = dst.records.get()
print(record.title)
# "登陆后页面崩溃"
print(record.state)
# "待修复"
record.update(state="已修复")
```

保留使用 field id 作 key 的用法
```python
bug = vika.datasheet("dstn2lEFltyGHe2j86", field_key="id")
row = bug.records.get(flddpSLHEzDPQ="登陆后页面崩溃")
row.flddpSLHEzDPQ = "登陆后页面崩溃"
row.update({
  "flddpSLHEzDPQ": "登陆后页面崩溃",
  "fldwvNDf9teD2": "已修复"
})

```

指定 `field_key="id"` 时，再指定 `field_key_map` 对应的键值应该是 `fieldId`

```python
bug = vika.datasheet("dstn2lEFltyGHe2j86", field_key="id", field_key_map={
  "title":"flddpSLHEzDPQ",
  "state":"fldwvNDf9teD2",
})
```

## API 

### records 方法

| 方法        | 参数   | 返回类型 | 说明                            | 例子                                                                         |
|-------------|--------|----------|---------------------------------|------------------------------------------------------------------------------|
| create      | dict   | Record   | 创建单条记录                    | `dst.records.create({"title":"new title"})`                                  |
| bulk_create | dict[] | Record[] | 批量创建多条记录                | `dst.records.bulk_create([{"title":"new record1"},{"title":"new record2"}])` |
| all         | **dict | QuerySet | 返回记录集合,可传参定制返回内容 | `dst.records.all()`                                                          |
| count       | /      | int      | 记录总数                        | `dst.records.count()`                                                        |
| get         | **dict | Record   | 单条记录                        | `dst.records.get(title="new title")`                                         |
| filter      | **dict | QuerySet | 过滤一批记录                    | `dst.records.filter(title="new title")`                                      |

### QuerySet

返回 QuerySet 的方法可以进行链式调用

| 方法   | 参数   | 返回类型 | 说明                   | 例子                                                              |
|--------|--------|----------|------------------------|-------------------------------------------------------------------|
| filter | **dict | QuerySet | 过滤出一批记录         | `dst.records.filter(title="new title")`                           |
| all    | /      | QuerySet | 返回当前记录集合的拷贝 | `dst.records.filter(title="new title").all()`                     |
| get    | **dict | Record   | 单条记录               | `dst.records.get(title="new title")`                              |
| count  | /      | int      | 记录总数               | `dst.records.filter(title="new title").count()`                   |
| last   | /      | Record   | 最后一条记录           | `dst.records.filter(title="new title").last()`                    |
| first  | /      | Record   | 第一条记录             | `dst.records.filter(title="new title").first()`                   |
| update | **dict | int      | 更新成功的记录数       | `dst.records.filter(title="new title").update(title="new title")` |
| delete | /      | bool     | 是否删除成功           | `dst.records.filter(title="new title").delete()`                  |

### all 参数

当首次调用 all 不传入任何参数时，默认加载第一个视图的记录，后续的 filter、get 均在本地缓存数据中进行，all 方法仅在首次调用时，从服务端获取数据。

当调用 all 时，显式地传入参数，则利用服务端计算返回部分数据集。

| 参数            | 类型           | 说明                                                                          | 例子                           |
|-----------------|----------------|-------------------------------------------------------------------------------|--------------------------------|
| viewId          | str            | 视图ID。默认为维格表中第一个视图。请求会返回视图中经过视图中筛选/排序后的结果 |                                |
| pageNum         | int            | 默认 1                                                                        |                                |
| pageSize        | int            | 默认 100 ， 最大 1000                                                         |                                |
| sort            | dict[]         | 指定排序的字段，会覆盖视图排序条件                                            | `[{ '列名称或者 ID': 'asc' }]` |
| recordIds       | str[]          | 返回指定 recordId 的记录集                                                    | `['recordId1', 'recordId2']`   |
| fields          | str[]          | 只有指定字段会返回                                                            |                                |
| filterByFormula | str            | 使用公式作为筛选条件，返回匹配的记录                                          |                                |
| maxRecords      | int            | 限制返回记录数，默认 5000                                                     |                                |
| fieldKey        | 'name' or 'id' | 指定 field 查询和返回的 key。默认使用列名 'name'。                            |                                |


参见：[公式使用方式](https://vika.cn/help/tutorial-getting-started-with-formulas/)

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

### 可以自动创建单多选选项吗？
```
record.tags = ["目前 tags 字段中不存在的选项"]
```
目前不可以，你只能赋值已经存在的选项。后续会支持 :D

### 单个表格最大支持多少条记录？

目前单表最大支持 5w 条记录

## TODO

+ [ ] 优化数据集较大时的网络请求
+ [ ] 网络请求封装 & 错误处理
+ [ ] filter 操作符
