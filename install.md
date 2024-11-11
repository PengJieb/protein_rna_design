<!--
 * @Author: pengjie pengjieb@mail.ustc.edu.cn
 * @Date: 2024-07-09 15:57:16
 * @LastEditors: pengjie pengjieb@mail.ustc.edu.cn
 * @LastEditTime: 2024-07-09 16:03:00
 * @FilePath: /LinearDesign/install.md
 * @Description: 
 * 
 * Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
-->
# Conda

```bash
conda create -n linear_design python=2.7 -y
conda activate linear_design
conda install conda-forge::gcc -y
make
cat P0DTC2.fasta.txt | ./lineardesign --lambda 3
```