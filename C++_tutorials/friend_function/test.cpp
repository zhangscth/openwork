/*================================================================
*   Copyright (C) 2019 * Ltd. All rights reserved.
*
*   Editor      : VIM
*   File name   : test.cpp
*   Author      : YunYang1994
*   Created date: 2019-05-31 14:50:14
*   Description :
*
*===============================================================*/

// 类的友元函数是定义在类外部，但有权访问类的所有私有（private）成员和保护（protected）成员。
// 尽管友元函数的原型有在类的定义中出现过，但是友元函数并不是成员函数。

#include <iostream>

class Box{
    double width;
public:
    friend void printWidth(Box box);
    void setWidth(double wid);
};

// 成员函数的定义
void Box::setWidth(double wid){
    width = wid;
}

// 请注意：printWidth() 不是任何类的成员函数
void printWidth(Box box){
    /* 因为 printWidth() 是 Box 的友元，它可以直接访问该类的任何成员 */
    std::cout << "Width of box : " << box.width << std::endl;
}

// 程序的主函数
int main(){
    Box box;

    // 使用成员函数设置宽度
    box.setWidth(10.0);

    // 使用友元函数输出宽度
    printWidth(box);

    return 0;
}
