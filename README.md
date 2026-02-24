# life-simulation
A minimal Python simulation of tribal life evolution with environmental adaptation
数字部落进化仿真 这个项目模拟了带有部落属性的细胞群体在周期性变化环境中的生存、竞争与演化过程。细胞通过遗传、变异形成独特的生存策略，同部落成员间还会进行互助行为。 核心功能 1. 基于遗传算法的策略演化，包含吸收效率、节能倾向、合作意愿三个维度 2. 周期性波动的环境资源模型 3. 部落间的资源竞争与部落内的个体互助机制 4. 种群数量动态平衡控制  运行方法 直接执行 Python 文件即可： bash   运行      python digital_tribe.py
    运行过程中会每 20 步输出一次当前种群状态，包括存活数量、各部落规模等信息。 参数调整 可以修改代码开头的全局配置来调整仿真规则： • MAX_POPULATION: 最大种群容量 • run_simulation()函数的参数可以调整仿真步数和环境周期长度
