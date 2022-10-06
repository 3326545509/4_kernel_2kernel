sh fft.sh
sh dataCollect.sh
i=1
imax=`cat data.txt|wc -l`
while(($i<=$imax))
do
id=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$1}'`
slo=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$2}'`
sla=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$3}'`
rlo=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$4}'`
rla=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$5}'`
dist=`cat data.txt |awk -F ' ' '{if(NR=="'$i'")print$6}'`
spetral_file=$id".txt"
kernel_file=$spetral_file"_kernel"
echo "sh sensitivity.sh $spetral_file $dist">$i"temp.sh"
echo "python3 plus.py $kernel_file $slo $sla $rlo $rla $dist>>dlhA.txt">>$i"temp.sh"
let i++
done

for f in ./*temp.sh
do
sh $f &
done

wait
rm *temp.sh
