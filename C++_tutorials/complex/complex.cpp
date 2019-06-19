/*================================================================
*   Copyright (C) 2019 * Ltd. All rights reserved.
*
*   Editor      : VIM
*   File name   : complex.cpp
*   Author      : YunYang1994
*   Created date: 2019-05-25 16:36:49
*   Description :
*
*===============================================================*/

#include "complex.h"
#include <cmath>

complex& complex::operator += (const complex& r)
{
  this->re += r.re;
  this->im += r.im;
  return *this;
};

double imag(const complex& x)
{
  return x.imag ();
};

double real(const complex& x)
{
  return x.real ();
};

complex conj(const complex& x)
{
  return complex (real (x), -imag (x));
};

double modul(const complex& x)
{
  return real (x) * real (x) + imag (x) * imag (x);
};



