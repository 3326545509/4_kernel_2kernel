spetral_file=$1
kernel_out=$spetral_file"_kernel"
dist=$2

exefile="temp"$spetral_file
ifort -132 -save -o $exefile sensitivity.f

$exefile<<EOF
3
$spetral_file
unsmooth
$kernel_out
1
$dist
EOF

#生成结果图
python3 draw.py $kernel_out
