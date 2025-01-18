#!/bin/bash
# ディレクトリ内の大量ファイルを2**n分割してディレクトリに分ける

if [ $# -ne 1 ]; then
    echo "引数の数が違う"
    exit 1
fi

# 対象のディレクトリとそこのパスを切り分ける
splite_directory=$(basename $1)
readonly splite_directory
base_directory=$(dirname $1)
readonly base_directory

echo $splite_directory
echo $base_directory

target_dir_list=($splite_directory)
count=1
while [ $count -lt 32 ]
do
    new_target_dir_list=()
    for t_dir in ${target_dir_list[@]};
    do
        echo $t_dir
        # ディレクトリ内のファイル数を数えて、その半分値を算出する
        num_file=$(find ${base_directory}/${t_dir}/. -type f|wc -l)
        half_num=$(($num_file>>1))
        echo $num_file
        echo $half_num

        # 対象のディレクトリ内のファイル一覧を出力し、その後半部分を作成する
        ls -1 ${base_directory}/${t_dir}/. > file_list.txt
        tail -q -n $half_num file_list.txt > half_list.txt
        half_files=(`cat half_list.txt|xargs`)
        rm file_list.txt
        rm half_list.txt

        # ディレクトリを2つに分割し、収納ファイル数を半分に分ける
        rename_dir=${t_dir}0
        new_dir=${t_dir}1
        new_target_dir_list+=(${rename_dir} ${new_dir})

        # 収納ファイルの後ろ半分を新しいディレクトリに移す
        mkdir ${base_directory}/${new_dir}
        for hf in ${half_files[@]};
        do
            mv ${base_directory}/${t_dir}/${hf} ${base_directory}/${new_dir}/${hf}
        done

        # 移し元のディレクトリを改名する
        mv ${base_directory}/${t_dir} ${base_directory}/${rename_dir}
    done

    target_dir_list=${new_target_dir_list[@]}
    count=$(($count<<1))
done