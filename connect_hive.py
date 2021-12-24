def connect_hive():  # 此处函数名，任意命名都行。
    from impala.dbapi import connect  # 导入impala的依赖包
    import pandas as pd  # 导入pandas 的依赖包
    # ali yun
    # conn = connect(host='39.105.27.82', port=10000, auth_mechanism='PLAIN', user='root', password='root')
    # tx yun
    conn = connect(host='119.45.131.150', port=10000, auth_mechanism='PLAIN', user='root', password='root')
    # impala = connect('116.168.1.20', port=11050, user='hdxdf')  # 连接方式
    print("connect to hive success")
    return conn  # 返回变量impala
