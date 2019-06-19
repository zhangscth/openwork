/*================================================================
*   Copyright (C) 2019 * Ltd. All rights reserved.
*
*   Editor      : VIM
*   File name   : test.cpp
*   Author      : YunYang1994
*   Created date: 2019-05-25 14:40:55
*   Description :
*
*===============================================================*/

#include <iostream>
#include "complex.h"

// using namespace std;

std::ostream&
operator << (std::ostream& os, const complex& x)
{
  return os << '(' << real (x) << ',' << imag (x) << ')';
}

int main()
{
  complex c1(2, 1);
  complex c2(4, 0);

  std::cout << "c1=" << c1 << " c2=" << c2 << std::endl;
  std::cout << "the angle of c1 is " << getAngle(c1) << std::endl;
  std::cout << "the conjugate of c1 is " << conj(c1) << std::endl;
  std::cout << "the modulus of complex is " << modul(c1) << std::endl;
  std::cout << "c1 += c2, so c1=" << (c1 += c2) << std::endl;

  return 0;
}







