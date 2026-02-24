import random
import math

# 全局配置
MAX_POPULATION = 200
cells = []
tribe_id_counter = 1

class TribalCell:
    def __init__(self, cell_id, tribe_id, parent_strategy=None):
        self.id = cell_id
        self.tribe = tribe_id
        self.energy = 50.0
        self.alive = True
        
        # 初始化策略基因：[吸收效率, 节能倾向, 合作意愿]
        if parent_strategy is None:
            self.strategy = [random.random() for _ in range(3)]
        else:
            # 遗传+微小变异
            self.strategy = [max(0, min(1, s + random.gauss(0, 0.03))) for s in parent_strategy]
        
        # 归一化策略值
        total = sum(self.strategy)
        self.strategy = [s / total for s in self.strategy]

    def act(self, resource):
        """执行生存行为，返回能量变化值"""
        # 吸收资源：基础资源*吸收效率*增益系数
        gain = resource * self.strategy[0] * 15
        # 能量消耗：基础消耗*(1-节能倾向)
        cost = 1.5 * (1 - self.strategy[1])
        return gain - cost

    def cooperate(self):
        """执行部落合作行为"""
        # 仅向同部落低能量成员捐赠
        tribe_members = [c for c in cells if c.alive and c.tribe == self.tribe and c.energy < 20]
        if tribe_members and self.energy > 60:
            donate_amount = min(8.0, self.energy - 50)
            target = random.choice(tribe_members)
            self.energy -= donate_amount
            target.energy += donate_amount

    def life_step(self, resource):
        """完成一个生命周期，返回新生细胞或None"""
        if not self.alive or self.energy <= 0:
            self.alive = False
            return None

        # 1. 执行生存行为
        self.energy += self.act(resource)
        self.energy = min(self.energy, 120.0)  # 能量上限

        # 2. 执行合作行为
        if random.random() < self.strategy[2]:
            self.cooperate()

        # 3. 尝试繁殖
        new_cell = None
        if self.energy >= 65 and len(cells) < MAX_POPULATION:
            self.energy -= 30  # 繁殖能量消耗
            new_cell = TribalCell(random.randint(1000, 9999), self.tribe, self.strategy)

        # 4. 自然死亡判定
        if random.random() < 0.0005:
            self.alive = False

        return new_cell

def run_simulation(steps=500, cycle=40):
    """运行完整仿真流程"""
    global cells, tribe_id_counter
    print("=== 数字部落进化仿真开始 ===")
    print(f"最大种群: {MAX_POPULATION} | 环境周期: {cycle} 步")
    
    # 初始化第一个细胞
    cells = [TribalCell(0, tribe_id_counter)]
    tribe_id_counter += 1

    for step in range(steps):
        # 1. 计算当前环境资源（周期性波动）
        phase = 2 * math.pi * (step % cycle) / cycle
        base_resource = 0.3 + 0.5 * math.sin(phase)

        # 2. 计算各部落资源分配（按种群占比分配）
        tribe_sizes = {}
        for cell in cells:
            if cell.alive:
                tribe_sizes[cell.tribe] = tribe_sizes.get(cell.tribe, 0) + 1
        
        total_alive = sum(tribe_sizes.values())
        tribe_resource = {}
        for tid, size in tribe_sizes.items():
            tribe_resource[tid] = base_resource * (size / total_alive) if total_alive > 0 else 0.1

        # 3. 执行所有细胞生命周期
        new_cells = []
        surviving_cells = []
        
        for cell in cells:
            if cell.alive:
                res = tribe_resource.get(cell.tribe, 0.1)
                baby = cell.life_step(res)
                surviving_cells.append(cell)
                if baby:
                    new_cells.append(baby)

        # 4. 更新细胞列表
        cells = surviving_cells + new_cells

        # 5. 每20步输出一次状态
        if step % 20 == 0:
            alive_count = len([c for c in cells if c.alive])
            tribe_info = " | ".join([f"部落{t}:{s}" for t, s in tribe_sizes.items()])
            print(f"第{step:3d}步 | 存活:{alive_count:3d} | {tribe_info}")

    print("\n=== 仿真结束 ===")
    print(f"最终存活数量: {len([c for c in cells if c.alive])}")
    print(f"当前部落数: {len(set(c.tribe for c in cells if c.alive))}")

if __name__ == "__main__":
    run_simulation(steps=500)