"""
Filter 过滤式
"""

from sklearn.feature_selection import VarianceThreshold
from pandas.core.frame import DataFrame
from scipy.stats import pearsonr
from sklearn.decomposition import PCA
import pandas as pd


def vt_test():
    """
    方差选择: 选择方差较大的特征
    """
    data = [
        [-0.46736075, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [1.29441185, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [1.00078309, 0.36773003, 0., 4.35889894, 0., 4.35889894],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 1., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.51629888, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.41838998, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [3.643442, 3.63644142, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.46736075, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [0.75609245, 2.00208572, 0., -0.22941573, 0., -0.22941573],
        [-0.46736075, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573]
    ]
    df = DataFrame(data, columns=["pm_count", "ord_count", "name_count", "addr_count", "chan_count", "item_count"])
    # iloc[a:b, c:d] , 逗号前是行选择, 逗号后是列选择, 仅写:代表全选, 下标从0开始, 区间右边闭合
    # 因为下标第2列都是0, 所以用iloc筛一下, 只选下标第0-1列 + 第3列 + 第5列, 这里保留第4列, 并且第4列有一个1的值, 让filter处理
    # df.iloc[:, 0:2], df.iloc[:, 3:4], df.iloc[:, -1:] + df.iloc[:, -2:-1]
    # append是纵向拼接, 跟在后面, 也就是行数会累加
    # concat时需要设置axis, axis=0就是append, axis=1是merge(left_index=True,right_index=True,how='outer')
    df_new = pd.concat([df.iloc[:, 0:2], df.iloc[:, 3:4], df.iloc[:, -1:], df.iloc[:, -2:-1]], axis=1)
    print(df_new)
    # threshold 默认是 0.0, 是方差
    vt = VarianceThreshold(threshold=0.5)
    data_new = vt.fit_transform(df_new)
    print(data_new)
    return None


def correlation_coefficient_test():
    """
    相关系数: 特征之间的相关程度
    皮尔森相关系数: 两个变量之间的皮尔森相关系数定义为两个变量之间的协方差和标准差的商
    例如广告费投入和销售额的相关性:
    广告费   销售额
    12.5    21.2
    15.3    23.9
    23.2    32.9
    ...
    ...
    r = (n * sigma(x * y) - sigma(x) * sigma(y)) / (sqrt(n * sigma(x^2) - sigma(x)^2) * sqrt(n * sigma(y^2) - sigma(y)^2))
    也就是:
            x       y       x^2     y^2     x*y
            12.5    21.2    156.25  449.44  265
            15.3    23.9    234.09  571.21  365.67
            23.2    32.9    538.24  1082.41 763.28
    sigma   51      78      928.58  2103.06 1393.95
    最终结果:
    r = (3 * 1393.95 - 51 * 78) / (sqrt(3 * 928.58 - 51^2) * sqrt(3 * 2103.06 - 78^2))
      = (4181.85 - 3978) / (sqrt(2785.74 - 2601) * sqrt(6309.18 - 6084)
      = 203.85 / sqrt(184.74) * sqrt(225.18)
      = 203.85 / 13.5919 * 15.0060
      = 203.85 / 203.9602
      = 0.9995
    r的结果会在-1到1之间, r > 0 表示正相关, r < 0 表示负相关, |r|越大, 相关性越强.
    一般而言, |r| < 0.4 是低度相关, 0.4 <= |r| < 0.7是显著相关, |r| >= 0.7是高度线性相关
    """
    data = [
        [-0.46736075, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [1.29441185, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [1.00078309, 0.36773003, 0., 4.35889894, 0., 4.35889894],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 1., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.51629888, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.41838998, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [3.643442, 3.63644142, 0., -0.22941573, 0., -0.22941573],
        [-0.17373199, -0.44944782, 0., -0.22941573, 0., -0.22941574],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.46736075, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [0.75609245, 2.00208572, 0., -0.22941573, 0., -0.22941573],
        [-0.46736075, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.04085889, 0., -0.22941573, 0., -0.22941573],
        [-0.66311327, -0.44944782, 0., -0.22941573, 0., -0.22941573]
    ]
    df = DataFrame(data, columns=["pm_count", "ord_count", "name_count", "addr_count", "chan_count", "item_count"])
    r = pearsonr(df["pm_count"], df["ord_count"])
    # r的第一个值就是相关系数, 这里可以看出pm_count和ord_count具有较强的相关性, 结果是0.8777
    print(r)
    return None


def pca_test():
    """
    主成分分析: 高维数据转换为低维数据, 过程中可能舍弃原有数据, 创造新的特征. 尽可能降低维数, 损失少量信息.
    """
    data = [
        [2, 8, 4, 5],
        [6, 3, 0, 8],
        [5, 4, 9, 1]
    ]
    # n_component为小数, 表示保留多少百分比的信息, 为整数, 表示减少到多少个特征
    pca1 = PCA(n_components=0.95)
    r1 = pca1.fit_transform(data)
    print(r1)
    pca2 = PCA(n_components=3)
    r2 = pca2.fit_transform(data)
    print(r2)
    return None


if __name__ == '__main__':
    """
    如果能用方差选择剔除方差较小的特征, 则过滤掉这部分
    如果不能, 那么就找出相关系数接近的特征, 要么选取其中之一, 要么加权求和, 要么使用主成分分析
    """
    # vt_test()
    # correlation_coefficient_test()
    pca_test()
