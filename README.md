> ⚠️ 请参考[迁移指南](https://github.com/vikadata/vika.py/blob/master/docs/upgrade_to_v1.md) 从 0.1.x 升级至 1.x 版本，旧版本我们将不再维护!

![vika.py](https://socialify.git.ci/vikadata/vika.py/image?description=1&descriptionEditable=Vika%20is%20a%20API-based%20SaaS%20database%20platform%20for%20users%20and%20developers%20here%27s%20Python%20SDK%20for%20integration.&font=Inter&forks=1&issues=1&language=1&logo=https%3A%2F%2Fs1.vika.cn%2Fspace%2F2020%2F09%2F04%2F9fcd0d98c2c74274840fcde3341d5164&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light)

[Vika](https://vika.cn) Python SDK 是对维格表 Fusion API 的官方封装，提供类似 Django ORM 风格的 API。

用户交流 QQ 群：683795224

## 快速开始

### 环境要求

python3.6 +

### 安装

```shell
pip install --upgrade vika
```

### 获取 API TOKEN

访问维格表的工作台，点击左下角的个人头像，进入「用户中心 > 开发者配置」。点击生成 Token(首次使用需要绑定邮箱)。

### 使用

基础用法

```python
from vika import Vika

vika = Vika("your api_token")

dst = vika.datasheet("dstt3KGCKtp11fgK0t")
# 传入表格URL 会自动解析表格 id，忽略视图 id。
# dst = vika.datasheet("https://vika.cn/space/spcxcvEBLXf7X/workbench/dstt3KGCKtp11fgK0t/viwmKtRiYcPfk")

# 创建记录
record = dst.records.create({"title": "new record from Python SDK"})
print(record.title)
# print(record.标题)

# 批量创建记录
records = dst.records.bulk_create([
    {"title": "new record from Python SDK"},
    {"title": "new record from Python SDK2"}
])

# 更新单个字段值
record.title = "new title"
print(record.title)
# "new title"

# 更新多个字段值
record.update({
    "title": "new title",
    "other_field": "new value",
})

# 批量更新多条记录
records = dst.records.bulk_update([
    {"recordId": "recxxxxx1", "fields":{"title": "new record.title from Python SDK"}},
    {"recordId": "recxxxxx2", "fields":{"title": "new record.title from Python SDK2"}},
])

# 附件字段更新
my_file = dst.upload_file( < 本地或网络文件路径 >)
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

# 将 record 对象转化为 json
record.json()

# 删除符合过滤条件的一批记录
dst.records.filter(title=None).delete()

# 获取字段
for field in vika.datasheet("dstId").fields.all():
  print(field.name)

# 获取指定视图的字段，隐藏的字段不会返回
for field in vika.datasheet("dstId").fields.all(viewId="viewId"):
  print(field.name)

# 获取视图
for view in vika.datasheet("dstId").views.all():
  print(view.name)

```

### 字段映射

对于中文用户，表格的字段名通常是中文，虽然 Python 支持中文变量名，但是依然会出现中文字段名不符合变量规范的情况。因此你不得不回退到使用 fieldId 作为 key 的情况，致使代码可读性变差。

为了改善这种情况，Python SDK 提供了字段映射的功能。

| Bug 标题\!     | Bug 状态 |
| -------------- | -------- |
| 登陆后页面崩溃 | 待修复   |

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
record.state="已修复"
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
    "title": "flddpSLHEzDPQ",
    "state": "fldwvNDf9teD2",
})
```

## API

### 维格表

#### records 方法

`dst.records` 管理表格中的记录。

| 方法             | 参数                  | 返回类型    | 说明                                                                                                   | 例子                                                                                                           |
| ---------------- | --------------------- | ----------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| create           | dict                  | Record      | 创建单条记录                                                                                           | `dst.records.create({"title":"new title"})`                                                                    |
| bulk_create      | dict[]                | Record[]    | 批量创建多条记录                                                                                       | `dst.records.bulk_create([{"title":"new record1"},{"title":"new record2"}])`                                   |
| bulk_update      | dict[]                | Record[]    | 批量更新多条记录                                                                                       | `dst.records.bulk_update([{"recordId": "recxxxxx1", "fields":{"title": "new record.title from Python SDK"}}])` |
| all              | \*\*kwargs            | QuerySet    | 返回记录集合,可传参定制返回内容                                                                        | `dst.records.all()`                                                                                            |
| get              | \*\*kwargs            | Record      | 单条记录                                                                                               | `dst.records.get(title="new title")`                                                                           |
| get_or_create    | (defaults,\*\*kwargs) | Record,bool | 通过 kwargs 查询对应的记录，如果不存在则结合 defaults 创建一条新记录，返回的 bool 表示是否是新建的记录 | `dst.records.get_or_create(title="new title",defaults={"status":"pending"})`                                   |
| update_or_create | (defaults,\*\*kwargs) | Record,bool | 通过 kwargs 查询对应的记录，并以 defaults 更新记录。不存在则创建（与 get_or_create 一致）              | `dst.records.update_or_create(title="new title",defaults={"status":"done"})`                                   |
| filter           | \*\*kwargs            | QuerySet    | 过滤一批记录                                                                                           | `dst.records.filter(title="new title")`                                                                        |

#### QuerySet

返回 QuerySet 的方法可以进行链式调用

| 方法   | 参数     | 返回类型 | 说明                   | 例子                                                              |
| ------ | -------- | -------- | ---------------------- | ----------------------------------------------------------------- |
| filter | \*\*dict | QuerySet | 过滤出一批记录         | `dst.records.filter(title="new title")`                           |
| all    | /        | QuerySet | 返回当前记录集合的拷贝 | `dst.records.filter(title="new title").all()`                     |
| get    | \*\*dict | Record   | 单条记录               | `dst.records.get(title="new title")`                              |
| count  | /        | int      | 记录总数               | `dst.records.filter(title="new title").count()`                   |
| last   | /        | Record   | 最后一条记录           | `dst.records.filter(title="new title").last()`                    |
| first  | /        | Record   | 第一条记录             | `dst.records.filter(title="new title").first()`                   |
| update | \*\*dict | Record   | 更新成功的记录数       | `dst.records.filter(title="new title").update(title="new title")` |
| delete | /        | bool     | 是否删除成功           | `dst.records.filter(title="new title").delete()`                  |

#### Record

查询出来的 QuerySet 是一个 Record 的集合。单个 Record 可以通过 `record.字段名` 的方式获取指定字段的值。

**请尽量避免字段名和 Record 保留的方法属性同名，表格中的同名字段会被遮蔽。如果确实存在，请使用字段映射配置**

| 方法/属性 | 参数 | 返回类型 | 说明                                     | 例子            |
| --------- | ---- | -------- | ---------------------------------------- | --------------- |
| json      | /    | dict     | 返回当前记录的所有字段值                 | `record.json()` |
| \_id      | /    | str      | \_id 是保留属性，返回当前记录的 recordId | `record._id`    |

#### 字段值

维格列字段值与 Python 数据结构的映射关系。 维格表中单元格为空的数据始终是 null，API 返回的记录中，不会包含值为 null 的字段。

| 维格列类型 | 数据类型            |
| ---------- | ------------------- |
| 单行文本   | str                 |
| 多行文本   | str                 |
| 单选       | str                 |
| 多选       | str[]               |
| 网址       | str                 |
| 电话       | str                 |
| 邮箱       | str                 |
| 数字       | number              |
| 货币       | number              |
| 百分比     | number              |
| 自增数字   | number              |
| 日期       | number              |
| 创建时间   | number              |
| 修改时间   | number              |
| 附件       | attachment object[] |
| 成员       | unit object[]       |
| 勾选       | bool                |
| 评分       | int                 |
| 创建人     | unit object         |
| 修改人     | unit object         |
| 神奇关联   | str[]               |
| 神奇引用   | any[]               |
| 智能公式   | str / bool          |

#### all 参数

all 方法会自动处理分页加载全部资源

_传入分页相关参数（pageNum、pageSize）时，SDK 不会再自动加载全部记录，只返回指定页数据_。

> 尽量避免在不加参数的情况下使用 dst.records.all 方法，获取全部数据。
> API 每次请求最多获取 1000 条数据，如果你的数据量过大，接近 50000 的限制。在不加任何参数的情况下，调用 all 会串行请求 50 次 API。 不仅非常慢，而且消耗 API 请求额度。

_返回指定分页的记录_

```python
dst.records.all(pageNum=3)
```

_搭配视图使用_

指定视图 id 返回和视图中相同的数据。

```python
dst.records.all(viewId="viwxxxxxx")
```

_使用公式筛选数据_

```python
dst.records.all(filterByFormula='{title}="hello"')
```

| 参数            | 类型               | 说明                                                                  | 例子                                  |
| --------------- | ------------------ | --------------------------------------------------------------------- | ------------------------------------- |
| viewId          | str                | 视图 ID。请求会返回视图中经过视图中筛选/排序后的结果                  |                                       |
| pageNum         | int                | 默认 1                                                                |                                       |
| pageSize        | int                | 默认 100 ， 最大 1000                                                 |                                       |
| sort            | dict[]             | 指定排序的字段，会覆盖视图排序条件                                    | `[{ field: 'field1', order: 'asc' }]` |
| recordIds       | str[]              | 返回指定 recordId 的记录集                                            | `['recordId1', 'recordId2']`          |
| fields          | str[]              | 只有指定字段会返回                                                    |                                       |
| filterByFormula | str                | 使用公式作为筛选条件，返回匹配的记录                                  |                                       |
| maxRecords      | int                | 限制返回记录数，默认 5000                                             |                                       |
| cellFormat      | 'json' or 'string' | 默认为 'json'，指定为 'string' 时所有值都将被自动转换为 string 格式。 |                                       |
| fieldKey        | 'name' or 'id'     | 指定 field 查询和返回的 key。默认使用列名 'name'。                    |                                       |

参见：[公式使用方式](https://vika.cn/help/tutorial-getting-started-with-formulas/)

### 空间站

### 文件目录

## 开发测试

复制测试模板到自己的空间站，每次测试时，保证表中只有一条 title = "无人生还" 的记录

- [正式环境测试模板](https://vika.cn/share/shrTZC8odwrWl95Gil2Dm)
- [内部环境测试模板](https://integration.vika.ltd/share/shr2BYKJ5QysFK9YoAws1)

```shell
cp .env.example .env
```

配置测试所需的环境变量

```shell
# 安装依赖
pipenv install --pre
pipenv shell
python -m unittest test
```

## 更新日志

参见: [releases](https://github.com/vikadata/vika.py/releases)

## 相关项目

- [JavaScript SDK](https://github.com/vikadata/vika.js)
- [Golang SDK](https://github.com/vikadata/vika.go)
- [Java SDK](https://github.com/vikadata/vika.java)

## FAQ

### 可以拿到表格的字段类型（meta）信息吗？

~~目前不可以，后续 REST API 升级会暴露表格 meta 信息~~

可以通过 fields/views 接口获取

### 可以自动创建单多选选项吗？

```
record.tags = ["目前 tags 字段中不存在的选项"]
```

~~目前不可以，你只能赋值已经存在的选项。后续会支持 :D~~

现在已经支持，如果写入不存在的单多选字段，自动创建该选项

### 单个表格最大支持多少条记录？

目前单表最大支持 5w 条记录

### 每次请求可以处理更多的记录吗？

目前是 10 条。后续我们会根据实际情况，调整该限制的大小。

### 每次请求可以获取更多的记录吗?

目前最大值是 1000 条。后续我们会根据实际情况，调整该限制的大小。
