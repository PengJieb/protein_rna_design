###
 # @Author: pengjie pengjieb@mail.ustc.edu.cn
 # @Date: 2024-07-09 16:44:13
 # @LastEditors: pengjie pengjieb@mail.ustc.edu.cn
 # @LastEditTime: 2024-07-09 19:55:35
 # @FilePath: /LinearDesign/running_scripts/covid_19_mrna.sh
 # @Description: 
 # 
 # Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
### 
lambda_values="0 1 4 10"

for lv in $lambda_values
do
    cat Q9J3M8.fasta.txt | ./lineardesign --lambda $lv --verbose
done