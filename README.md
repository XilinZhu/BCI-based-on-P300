# BCI-based-on-P300
 A Brain computer interface algorithm based on p300. This is a project developed from 17th China Post-Graduate Mathematical Contest in Modeling(GMCM2020).

## 文件说明

- 通过`generate_train_set.mlx` `generate_test_set.mlx` 读取数据并生成训练集和测试集。
- 通过 `Model` 进行模型训练与预测。
  - `Model` 只展示了比较实验后最终选用的 LDA 分类器。

## 概要

根据脑电信号噪声多，随机性强的特点设计了去趋势、10Hz低通滤波的预处理基本步骤。进一步地，针对 P300 的检测进行了 EMD 滤波以及数据分割和相干叠加平均。实验发现，受试者在靶刺激下的脑电信号与非靶刺激者相比，前者在0.4-0.5s 之间的幅度明显高于后者。为了获得最佳的分类方法，设计了 0-800ms, 0-500ms, 100-500ms, 200-500ms 四种数据分割方案，并尝试了LDA、随机森林、逻辑回归与 sVM四种常见分类器。经过实验对比发现，200-500ms的分割方法配合LDA可以获得最佳的P300 检测性能——平均F1得分为0.38，准确度为0.62。

## 模型框图

![](https://i.loli.net/2020/10/22/wEBTSiPlXV4pAte.jpg)

## 预处理

预处理（`generate_train_set.mlx` `generate_test_set.mlx`）主要包含了以下步骤：

1. 基于线性拟合去趋势
2. 10Hz 低通滤波
3. 基于 EMD 的低频噪声去除
4. 降采样与归一化
5. 数据分割与相干叠加平均

下面两张图展示了步骤1-4以及步骤5的结果

<table> 
    <tr>
        <td><center><img src = "https://i.loli.net/2020/10/22/Z1Ms9S8YzUeXILv.png"height="300"></center><br>
            <center>图1 预处理</center>
        </td>
        <td><center><img src = "https://i.loli.net/2020/10/22/wOHXrPKvyFtMJaR.jpg" height="300"></center><br>
        	<center>图2 分割与相干叠加平均</center>
        </td>
    </tr>
</table>

## 分类器

经过实验对比发现，选区刺激发生后 200-500ms 的内的脑电信号，配合 LDA 分类器可以获得最佳的 P300 检测性能——平均 F1 得分为 0.38，准确度为 0.62。

<table> 
    <tr>
        <td><center><img src = "https://i.loli.net/2020/10/22/gt6w7cHEoQBkWpZ.png"height="300"></center><br>
            <center>图3 F1得分</center>
        </td>
        <td><center><img src = "https://i.loli.net/2020/10/22/xy8Be1VTv5KkqWU.png" height="300"></center><br>
        	<center>图4 准确度</center>
        </td>
    </tr>
</table>