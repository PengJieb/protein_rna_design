###
 # @Author: pengjie pengjieb@mail.ustc.edu.cn
 # @Date: 2024-07-09 16:52:07
 # @LastEditors: pengjie pengjieb@mail.ustc.edu.cn
 # @LastEditTime: 2024-07-09 16:53:26
 # @FilePath: /LinearDesign/running_scripts/debug.sh
 # @Description: 
 # 
 # Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
### 
make
cat testseq | python lineardesign_debug.py --lambda 1 --verbose