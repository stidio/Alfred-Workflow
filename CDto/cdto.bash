#!/bin/bash

# Author:   Nicolas Chow
# Contact:  stidio@163.com
# Blog:     http://stidio.github.io
# Created:  2016-11-21 12:21:00

FILE={query}

if [ -d "${FILE}" ]; then     # 目录直接保存
  DIR=${FILE}
else
  if [ -f "${FILE}" ]; then   # 文件获取文件所在目录
    DIR=$(dirname "${FILE}")
  else                        # 其他情况直接退出
    exit 1
  fi
fi

# 通过osascript(JavaScript)打开Terminal，然后输入cd ...
osascript -l JavaScript << END
  term = Application("Terminal");
  term.doScript("cd \"${DIR}\"");
  term.activate();
END