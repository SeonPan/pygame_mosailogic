import pygame
import sys
from random import random


class Item:  # 自定义方块类
    def __init__(self, pos_x, pos_y, leng):
        self.rect = pygame.draw.rect(screen, white, [pos_x, pos_y, leng, leng], 0)
        self.state = False


def create_chessboard():  # 创建棋盘
    item_lst = []
    for v in range(size):
        for h in range(size):
            rect = Item(start_x + h*length, start_y + v*length, length)
            item_lst.append(rect)
    return item_lst


def draw_line():  # 绘制网格线
    for n in range(size+1):
        start = (start_x, start_y + n * length)
        end = (start_x + square, start_y + n * length)
        pygame.draw.line(screen, gray, start, end, 2)
    for n in range(size+1):
        start = (start_x + n * length, start_y)
        end = (start_x + n * length, start_y + square)
        pygame.draw.line(screen, gray, start, end, 2)


def check_click(item_lst, pos_x, pos_y):  # 更新每个方块的点击状态
    global count
    for i in item_lst:
        if i.rect.collidepoint(pos_x, pos_y):
            count += 1
            i.state = bool(1 - i.state)
            if i.state:
                click_on_sound.play()
            else:
                click_off_sound.play()


def change_color(item_lst):  # 根据状态改变方块颜色
    for i in item_lst:
        if i.state:
            pygame.draw.rect(screen, blue, i.rect, 0)
        else:
            pygame.draw.rect(screen, white, i.rect, 0)


def get_player_array(item_lst):  # 获取玩家操作矩阵
    return [1 if i.state else 0 for i in item_lst]


def create_answer_array():  # 创建答案矩阵
    lst = [1 if random() > 0.5 else 0 for _ in range(size*size)]
    if list(set(lst))[0] == 0:
        lst[0] = 1
    return lst


def get_line_remind(_line):  # 输出一行或一列的提示
    remind = []  # 一行或一列的提示记录
    num = 0  # 提示值

    def fun(line):
        nonlocal remind, num
        flag = 0  # 位移
        if len(line) > 1:
            if line[0] == 0 and line[1] == 1:
                flag += 1
            elif line[0] == line[1] == 0:
                flag += 2
            elif line[0] == 1 and line[1] == 0:
                num += 1
                remind.append(num)
                num = 0
                flag += 2
            elif line[0] == line[1] == 1:
                num += 1
                flag += 1
            fun(line[flag:])
        elif len(line) and line[0]:
            if num:
                remind.append(num + 1)
            else:
                remind.append(1)
    fun(_line)
    return remind


def get_w_remind(answer_lst):  # 根据答案矩阵输出提示列表
    h_remind = []
    v_remind = []
    h_array = [answer_lst[i: i+size] for i in range(0, len(answer_lst), size)]  # 横向矩阵
    for h in h_array:
        h_remind.append(get_line_remind(h))
    v_array = list(map(list, zip(*h_array)))  # 纵向矩阵
    for v in v_array:
        v_remind.append(get_line_remind(v))
    return h_remind, v_remind


def show_remind(answer_lst):  # 在棋盘两侧对应位置显示每行/列的提示
    h_remind, v_remind = get_w_remind(answer_lst)
    for i, h in enumerate(h_remind):
        for j, num in enumerate(h[::-1]):
            text = font.render(f"{num}", True, black)
            screen.blit(text, (start_x - 20 * (j + 1), start_y + i * length + length / 2 - 10))
    for i, v in enumerate(v_remind):
        for j, num in enumerate(v[::-1]):
            text = font.render(f"{num}", True, black)
            screen.blit(text, (start_x + i * length + length / 2 - 5, start_y - 30 * (j + 1)))


def change_difficulty(delta):  # 修改难度
    global size, length, items, answer
    if size > 7 and delta < 0:
        size += delta
    elif size < 3 and delta > 0:
        size += delta
    elif 3 <= size <= 7:
        size += delta
    length = int(square / size)
    re_start()
    answer = create_answer_array()  # 创建答案矩阵
    items = create_chessboard()  # 创建棋盘


def re_start():  # 重新游戏
    global items, win_flag, win_y, count
    for i in items:
        i.state = False
    win_flag = False
    win_y = count = 0


def fixed_icon():  # 固定图标显示
    click_icon = pygame.image.load(r'./images/click_icon.png')  # 操作次数图标
    click_icon = pygame.transform.scale(click_icon, icon_size)
    screen.blit(click_icon, (10, 8))
    fresh_icon = pygame.image.load(r'./images/fresh.png')  # 换题图标
    fresh_icon = pygame.transform.scale(fresh_icon, icon_size)
    fresh = screen.blit(fresh_icon, (330, 10))
    up_icon = pygame.image.load(r'./images/up.png')  # 提高难度图标
    up_icon = pygame.transform.scale(up_icon, (15, 15))
    up = screen.blit(up_icon, (370, 6))
    down_icon = pygame.image.load(r'./images/down.png')  # 降低难度图标
    down_icon = pygame.transform.scale(down_icon, (15, 15))
    down = screen.blit(down_icon, (370, 23))
    result_icon = pygame.image.load(r'./images/result.png')  # 作弊图标
    result_icon = pygame.transform.scale(result_icon, icon_size)
    res = screen.blit(result_icon, (5, 480))
    return fresh, up, down, res


def win_anime():  # 通关提示动画
    global win_y
    if win_y < 220:
        win_y += 20
    win_text = win_font.render("YOU WIN!", True, black)
    screen.blit(win_text, (255, win_y))
    if win_y > 200 and count > answer.count(1):  # 操作次数大于目标个数
        text = mes_font.render("need to improve =v=", True, black)
        screen.blit(text, (250, 280))
    elif win_y > 200:
        text = mes_font.render("wow~ perfect 0.0", True, black)
        screen.blit(text, (275, 280))


def show_click_count():  # 显示点击方格的次数
    count_text = mes_font.render(f"{count}", True, gold)
    screen.blit(count_text, (42, 3))


def show_aim_count():  # 显示目标方格的个数
    pygame.draw.rect(screen, blue, [80, 8, *icon_size], 0)
    count_text = mes_font.render(f"{answer.count(1)}", True, gold)
    screen.blit(count_text, (115, 3))


def show_result():  # 作弊
    count_text = font.render(f"{answer}", True, black)
    screen.blit(count_text, (40, 480))


if __name__ == '__main__':
    # 参数设置 ----------------------------------
    blue = (159, 197, 232)  # 被选中方格的颜色
    gray = (217, 217, 217)  # 棋盘网格线颜色
    gold = (255, 215, 0)  # 游戏记录文字颜色
    black = (0, 0, 0)
    white = (255, 255, 255)
    start_x = 240  # 棋盘左上角位置
    start_y = 150
    size = 2  # 一行/列的方块个数
    square = 320  # 棋盘边长
    length = int(square / size)  # 每个方块的边长
    count = 0  # 操作次数
    win_flag = False  # 是否通关
    win_y = 0  # 通关信息起始点
    icon_size = (28, 28)
    size_map = {2: "TEST", 3: "C", 4: "B", 5: "A", 6: "S", 7: "SS", 8: "SSS"}  # 难度级别
    # 游戏初始化 ----------------------------------
    pygame.init()
    screen = pygame.display.set_mode((780, 520))  # 创建窗口
    pygame.display.set_icon(pygame.image.load(r'./images/logo.ico'))  # 窗口图标
    pygame.display.set_caption("Mosailogic_1.0 by @Seon")  # 窗口标题
    tick = pygame.time.Clock()  # 帧数控制
    font = pygame.font.Font(r'./data/msyh.ttf', 20)  # 提示字体
    mes_font = pygame.font.Font(r'./data/msyh.ttf', 30)  # 游戏记录字体
    win_font = pygame.font.Font(r'./data/msyh.ttf', 60)  # 通关信息字体
    return_icon = pygame.image.load(r'./images/return.png')  # 重新游戏图标（初始隐藏）
    return_icon = pygame.transform.scale(return_icon, icon_size)
    return_rect = return_icon.get_rect(topleft=(650, 7))  # 碰撞检测区
    items = create_chessboard()  # 创建棋盘
    answer = create_answer_array()  # 创建答案矩阵
    pygame.mixer.music.load(r'./data/bgm.wav')
    pygame.mixer.music.play(-1)  # 循环背景音乐
    click_on_sound = pygame.mixer.Sound(r'./data/click_on.wav')  # 选中点击音效
    click_off_sound = pygame.mixer.Sound(r'./data/click_off.wav')  # 取消点击音效
    change_sound = pygame.mixer.Sound(r'./data/change.wav')  # 换题、修改难度、重开音效
    win_sound = pygame.mixer.Sound(r'./data/win.wav')  # 通关音效
    wait_sound = True
    # 主循环 ----------------------------------
    while True:
        screen.fill(white)  # 背景填充
        fresh_rect, up_rect, down_rect, res_rect = fixed_icon()  # 显示固定的图标，返回碰撞检测区
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 退出pygame
                sys.exit()  # 安全退出系统
            if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标点击事件
                x, y = event.pos
                if not win_flag:
                    check_click(items, x, y)  # 检查选中的方格，修改状态
                    result = get_player_array(items)  # 获取方格操作矩阵
                    if result == answer:
                        win_flag = True
                        win_sound.play()
                elif return_rect.collidepoint(x, y):
                    change_sound.play()
                    re_start()  # 重开
                if fresh_rect.collidepoint(x, y):
                    change_sound.play()
                    re_start()
                    answer = create_answer_array()  # 换题
                if up_rect.collidepoint(x, y):
                    change_sound.play()
                    change_difficulty(1)  # 提高难度
                if down_rect.collidepoint(x, y):
                    change_sound.play()
                    change_difficulty(-1)  # 降低难度
            if res_rect.collidepoint(pygame.mouse.get_pos()):
                show_result()  # 作弊码

        change_color(items)  # 根据方格状态修改颜色
        draw_line()  # 绘制棋盘网格线
        show_remind(answer)  # 显示数值提示
        show_click_count()  # 显示点击方格的次数
        diff_text = mes_font.render(f"{size_map[size]}", True, gold)  # 显示难度等级
        screen.blit(diff_text, (390, 3))
        if win_flag:
            win_anime()  # 通关提示动画
            show_aim_count()  # 显示目标方格的个数
            screen.blit(return_icon, (650, 7))  # 显示重新游戏图标
            again_text = mes_font.render("again", True, gold)
            screen.blit(again_text, (685, 0))
        pygame.display.flip()  # 更新全部显示
        tick.tick(30)
