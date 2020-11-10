def chunks(_list, chunk_size):
    for i in range(0, len(_list), chunk_size):
        yield _list[i: i + chunk_size]
