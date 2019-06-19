/*================================================================
*   Copyright (C) 2019 * Ltd. All rights reserved.
*
*   Editor      : VIM
*   File name   : complex.h
*   Author      : YunYang1994
*   Created date: 2019-05-25 14:40:18
*   Description :
*
*===============================================================*/

#pragma once
#ifndef __MYCOMPLEX__
#define __MYCOMPLEX__
#define pi 3.1415926

class complex;
complex conj(const complex& x);

double imag(const complex& x);
double real(const complex& x);
double modul(const complex& x);
double getAngle(const complex& r);

class complex
{
public:
  complex (double r = 0, double i = 0): re (r), im (i) { }
  complex& operator += (const complex&);
  double real () const { return re; }
  double imag () const { return im; }
private:
  double re, im;

  friend double getAngle(const complex&);
};

#include <cmath>
#include <iostream>

inline double getAngle(const complex& r)
{
    return 180. * (atan(r.im / r.re) / pi);
};

#endif   //__MYCOMPLEX__




