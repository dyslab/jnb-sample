# Filename: vt100_test.sh
# Don't forget the command line when you met a permission issue: chmod 777 ./vt100_test.sh

# Switch cursor OFF
echo -e "\033[?25l"   # "\033" equals to "\e", "\e[?25l" works fine too
for i in $(seq 30 37)  
do
    # Change text/foreground color
    echo -ne "\e[s\e[${i}m hello World 文字颜色测试 [$i] \e[u"
    # Delay 1 second(s)
    sleep 1s
done

echo    # New blank line

echo -ne "\e[30m"
for i in $(seq 40 47)  
do
    # Change background color
    echo -ne "\e[s\e[${i}m hello World 背景颜色测试 [$i] \e[u"
    # Delay 1 second(s)
    sleep 1s
done

echo    # New blank line

# Change text/foreground color to green and set cursor position to col 40
echo -e "\e[32m\e[40C Demo finished."

# Switch cursor ON and clear all vt100 commands and settings
echo -e "\e[?25h\e[0m"
