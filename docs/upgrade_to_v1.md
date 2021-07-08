从 v0.1.2 升级到 v1.x 指南

## 新增

### 维格表

+ 新增获取 fields 接口
  ```python
  for field in dst.fields.all():
    print(field.name)
  # 获取指定视图的字段，隐藏的字段不会返回
  for field in dst.fields.all(viewId="viewId"):
    print(field.name)
  ```
+ 新增获取 views 接口
  ```python
  for view in dst.views.all():
    print(view.name)
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

### 空间站

+ 新增获取空间站列表接口
  ```python
  # 获取当前用户的空间站列表
  for space in vika.spaces.all():
    print(space.name)
  ```

### 文件

+ 新增获取指定空间站根文件目录接口
  ```python
  for node in vika.space('spaceId').nodes.all():
    print(node.name)
  ```

+ 新增获取指定文件信息接口
  ```python
  dst_info = vika.nodes.get('dst_id')
  # 打印数表名称
  print(dst_info.name)
  folder_info = vika.nodes.get('folder_id')
  # 文件夹节点存在 children 可以获取子文件信息
  print(dst_info.children)
  ```

## 不兼容改动

整体改动：

### 不再支持批量操作 10 条以上的记录

API 目前只支持一次写入 10 条记录，在批量新增、更新、删除操作时候，如果传入的数据大于 10 条，会报错。 批量操作虽然很方便，但是掩盖了部分请求失败的错误，显示地处理错误更能保证数据的正确性。

QuerySet 现在提供了 chunks 方法，自动将记录分批处理。我们认为这是值得的，特别是当你的业务数据很重要时，便捷应该被放在第二位。
 

```python
more_then_10_records = dst.records.all()

# 现在这样做会报错❌
more_then_10_records.delete()
# raise Exception

# 正确的做法 ✅
for each_batch_records in more_then_10_records.chunks():
    try:
        each_batch_records.delete()
    except Exception as e:
        print(e)
        # 在这里处理你的错误
```

### 获取记录

+ dst.records.filter
+ dst.records.all
    + 这是一个消耗巨大的请求，可能会非常慢。在此之前需要串行请求完所有分页的数据再返回，阻塞等待很久。 从返回全部的记录，变成迭代返回每页记录
