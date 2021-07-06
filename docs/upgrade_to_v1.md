从 v0.1.2 升级到 v1.x 

## 新增

```python
from Vika import vika
vika = Vika(token="your API Token")
dst = vika.datasheet('dstId')
```
+ 新增获取 fields 接口
  ```python
  for field in dst.fields.all():
    print(field.name)
  ```
+ 新增获取 views 接口
  ```python
  for view in dst.views.all():
    print(view.name)
  ```
+ 新增获取 spaces 接口
  ```python
  for space in vika.spaces.all():
    print(space.)
  ```
+ 新增获取 nodes 接口
  ```python
  for space in vika.spaces.nodes(spaceId="spaceId"):
    print(space.name)
  ```
+ 更新一批记录记时，支持传入自定义函数
  ```python
  def update_name(record):
    if record.score >= 80:
      record.level = 'A'
    elif record.score >= 60:
      record.level = 'B'
    else:
      record.level = 'C'

  dst.records.all().update(update_name)
  ```
+ 更新所
## 不兼容改动

整体改动：
+ 批量操作大于 10 条记录时会报错。在批量新增、更新、删除操作时候，如果传入的数据大于 10 条。
  + 批量操作虽然很方便，但是掩盖了部分请求失败的错误，显示地处理错误更能保证数据的正确性

### 获取记录

+ dst.records.filter
+ dst.records.all
  + 这是一个消耗巨大的请求，可能会非常慢。在此之前需要串行请求完所有分页的数据再返回，阻塞等待很久。 从返回全部的记录，变成迭代返回每页记录
  