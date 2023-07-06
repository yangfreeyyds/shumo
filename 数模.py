import random
import turtle

population = []
infection_rate = 2
hospital_capacity = [0, 0]
num=[0,0]
recovery_period = 3
max_survival_days = 50
death_rate = 5
personnumber=int(input("请输入人口基数^2:"))
bednumber=int(input("请输入病床数:"))
size=float(input("请输入最大传播距离:"))
cure=float(input("请输入治愈率:"))
cricul=int(input("模拟天数:"))

# 创建初始状态的人口
for i in range(-personnumber, personnumber):
    for j in range(-personnumber, personnumber):
        individual = [[i, j], 100, 0, turtle.Turtle()]  # [坐标, 状态（0：未感染，1：感染，2：已隔离，3：已死亡），天数，turtle对象]
        population.append(individual)  # 将人口添加到列表population中
        turtle.delay(0)  # 设置绘图延迟
        individual[3].shape('circle')  # 设置人口的形状
        individual[3].resizemode('user')  # 设置人口的缩放模式
        individual[3].shapesize(0.3)  # 设置人口的大小
        individual[3].fillcolor('green')  # 设置人口的颜色
        individual[3].penup()  # 抬起画笔，避免绘制轨迹
        individual[3].goto((individual[0][0] * 8) - 100, (individual[0][1] * 8) - 100)  # 将画笔移动到人口的初始位置

movement_directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [0, 0]]  # 定义人口移动的方向

# 定义人口移动的函数
def move_individual(individual):
    individual[0][0] += movement_directions[random.randint(0, 4)][0]  # 随机选择一个方向并移动
    individual[0][1] += movement_directions[random.randint(0, 4)][1]

    individual[3].goto((individual[0][0] * 8) - 100, (individual[0][1] * 8) - 100)  # 将画笔移动到人口的新位置
    return individual

# 定义传染病传播的函数
def spread_infection(individual):
    infection_list = []
    for person in population:
        if (person[0][0] - individual[0][0]) ** 2 + (person[0][1] - individual[0][1]) ** 2 < size and person[2] == 0:  # 判断距离是否小于2，并且未感染
            infection_list.append(person)  # 将可传染的人口添加到列表中
        else:
            continue
    for _ in range(infection_rate):
        if len(infection_list) == 0:  # 如果没有可传染的人口，则结束传染
            break
        else:
            random_index = random.randint(0, (len(infection_list) - 1))  # 随机选择一个可传染的人口进行传染
            infection_list[random_index][2] = 1  # 将该人口状态设置为感染
            infection_list[random_index][3].fillcolor('yellow')  # 将该人口的颜色设置为黄色
            infection_list.remove(infection_list[random_index])  # 将该人口从可传染列表中移除

def treat_individual(individual):
    individual[2] = 2  # 将病人状态设置为已治愈
    if individual[1] >= 90:  # 如果病人已经痊愈
        population.remove(individual)  # 将病人从总人口列表中移除
        individual[3].reset()  # 将病人的turtle对象清除
        hospital_capacity[1] += 1  # 将医院收治的人数加1
        hospital_capacity[0] -= 1  # 将医院剩余床位数减1
    else:  # 如果病人还没痊愈
        individual[1] += death_rate  # 将病人的生存天数增加death_rate
        individual[3].fillcolor('blue')  # 将病人的颜色设置为蓝色

def isolate_individual(individual):  # 隔离
    individual[2] = 3  # 将病人状态设置为已隔离
    if individual[1] > 0:  # 如果病人还活着
        individual[1] -= recovery_period  # 将病人的生存天数减少recovery_period
        individual[3].fillcolor('red')  # 将病人的颜色设置为红色
    else:  # 如果病人已经死亡
        population.remove(individual)  # 将病人从总人口列表中移除
        num[0]+=1
        individual[3].reset()  # 将病人的turtle对象清除

def treatment_selection(individual):
    if hospital_capacity[0] == bednumber:  # 如果医院已经没有床位了
        isolate_individual(individual)  # 将病人隔离
    else:  # 如果医院还有床位
        treat_individual(individual)  # 对病人进行治疗
        hospital_capacity[0] += 1  # 将医院剩余床位数减1

def death_operation(individual):
    if individual[1] > max_survival_days:  # 如果病人已经生存了超过max_survival_days天
        individual[1] -= recovery_period  # 将病人的生存天数减少recovery_period
    elif individual[1] > 0 and individual[1] <= max_survival_days:  # 如果病人还活着并且生存时间小于等于max_survival_days天
        treatment_selection(individual)  # 对病人进行治疗或隔离
    else:  # 如果病人已经死亡
        population.remove(individual)  # 将病人从总人口列表中移除
        num[0]+=1
        individual[3].reset()  # 将病人的turtle对象清除

def start_simulation(days):
    for day in range(days):
        for individual in population:
            if individual[2] == 0 or individual[2] == 1:  # 如果病人状态为未感染或者潜伏期
                move_individual(individual)  # 对病人进行移动操作
            elif individual[2] == 2:  # 如果病人状态为已治愈
                treat_individual(individual)  # 对病人进行治疗操作
            else:  # 如果病人状态为已隔离或者死亡
                death_operation(individual)  # 对病人进行死亡操作
        infected_list = [x for x in population if x[2] == 1]  # 找出所有处于潜伏期的病人
        for infected in infected_list:
            spread_infection(infected)  # 对潜伏期病人进行感染操作
            death_operation(infected)  # 对潜伏期病人进行死亡操作

def statistics():
    num_infected = 0
    num_uninfected = 0
    for individual in population:
        if individual[2] == 1:  # 统计当前感染人数
            num_infected += 1
        elif individual[2] == 0:  # 统计当前未感染人数
            num_uninfected += 1
        else:
            continue

    print('目前潜伏感染的人数有', num_infected, '个')
    print('目前未感染的人数有', num_uninfected, '个')
    print('目前死亡的人数有',num[0],'个')  # 统计当前死亡人数
    print('目前治愈的人数有', hospital_capacity[1]*cure, '个')  # 统计当前治愈人数
    print('目前隔离或者住院的人数有',(personnumber*2)**2-num_infected-num_uninfected-num[0]-hospital_capacity[1],'个')

population[personnumber][2]=1
population[0][3].pencolor('green')  # 将第5个人的颜色设置为绿色
start_simulation(cricul)  # 运行模拟程序，模拟20天的传染过程
statistics()  # 统计结果并输出
turtle.mainloop()