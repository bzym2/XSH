import curses

def main(stdscr):
    # 初始化curses环境
    curses.curs_set(1)  # 显示光标
    stdscr.nodelay(1)  # 设置为非阻塞输入模式
    stdscr.timeout(100)  # 设置屏幕刷新间隔，100毫秒

    # 初始化颜色
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # 处理输入和输出
    word = ''
    while True:
        stdscr.clear()  # 清屏
        stdscr.addstr(0, 0, 'Enter a word: ')

        # 根据输入的单词改变颜色
        if len(word) > 0 and word[0].lower() in 'aeiou':  # 如果第一个字母是元音
            stdscr.addstr(1, 0, word, curses.color_pair(1))  # 红色
        else:
            stdscr.addstr(1, 0, word, curses.color_pair(2))  # 绿色

        stdscr.refresh()

        # 获取用户输入
        key = stdscr.getch()

        # 按 'q' 退出
        if key == ord('q'):
            break
        # 按退格删除字符
        elif key == 263:
            word = word[:-1]
        # 获取其他按键字符并添加到word
        elif key != -1:
            word += chr(key)

# 运行curses应用
curses.wrapper(main)
