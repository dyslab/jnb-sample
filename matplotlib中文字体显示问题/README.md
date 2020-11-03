# 解决notebook中 matplotlib 图表中文显示乱码的问题


1. **添加单元格，输入并运行如下代码，得到 matplotlib 配置文件路径和字体存放的目录。**

    ```Python
    import matplotlib

    print('matplotlib配置文件路径：%s' % matplotlib.matplotlib_fname())

    # 例如，本机输出结果如下：
    #
    # matplotlib配置文件路径：/home/vincento/pws/jnb-sample/venv/lib/python3.5/site-packages/matplotlib/mpl-data/matplotlibrc
    #
    ```


2. **取得 matplotlib 字体文件存放目录，其路径为：[matplotlib配置文件所在目录]/fonts/ttf/**

    本例中，matplotlib 字体文件存放于 `/home/vincento/pws/jnb-sample/venv/lib/python3.5/site-packages/matplotlib/mpl-data/fonts/ttf/`


3. **把本目录中的字体文件 CESI_xx_GB2312.ttf 拷贝到 matplotlib 字体文件存放路径中。**

    字体文件描述：（ 字体代码：*字体* ）

    - CESI_SS_GB2312：*对应 CESI宋体-GB2312*
    - CESI_FS_GB2312：*对应 CESI仿宋-GB2312*
    - CESI_KT_GB2312：*对应 CESI楷体-GB2312*
    - CESI_HT_GB2312：*对应 CESI黑体-GB2312*


4. **添加一个新的单元格，输入并运行如下代码：**

    ```Python
    plt.rcParams['font.family'] = ['CESI_FS_GB2312']        # Set font family to Chinese
    plt.rcParams['font.sans-serif'] = ['CESI_FS_GB2312']    # Set default font type to Chinese
    plt.rcParams['font.size'] = 14.0                        # default value changes to 14
    plt.rcParams['axes.unicode_minus'] = False              # Fix Minus Sign unrecognized issue
    ```


5. **完成以上步骤后，即可在后续单元格中使用 matplotlib 图表正常输出显示中文。**

    注：需要更换默认字体的话，可把 **第4点** 中 `plt.rcParams['font.sans-serif']` 的值赋为其他字体代码即可。
