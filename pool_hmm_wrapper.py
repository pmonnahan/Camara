
import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='This program takes a merged vcf with highest-coverage individuals from specific pops as input, and outputs a lookup key from the merged vcf')
parser.add_argument('-p', type=str, metavar='pileup_directory', required=True, help='full path to directory containing pileup files')
parser.add_argument('-c', type=str, metavar='min_cov', default='1', required=False, help='-c (or --min-coverage) value, where value is the minimum coverage required for a site to be used in the analyzes ; default is 1.')
parser.add_argument('-C', type=str, metavar='max_cov', default='10000', required=False, help='-C (or --max-coverage) value, where value is the maximum coverage required for a site to be used in the analyzes ; default is 10000.')
parser.add_argument('-q', type=str, metavar='min_qual', default='0', required=False, help='-C (or --max-coverage) value, where value is the maximum coverage required for a site to be used in the analyzes ; default is 10000.')
parser.add_argument('-o', type=str, metavar='Output_Prefix', required=True, help='should be absolute path to output directory plus population name.')
parser.add_argument('-nc', type=str, metavar='numberOfCores', required=True, help=' ')
parser.add_argument('-mem', type=str, metavar='memoryRequested', required=True, help=' ')
parser.add_argument('-P', type=str, metavar='Print?', default='false', required=False, help=' ')

args = parser.parse_args()

n = {"CEZ": '108', "LUZ": '50', "PIC": '104', "VKR": '52'}
file_list = []
for file in os.listdir(args.p):
    if file.endswith(".pileup"):
        file_list.append(file)

if args.p.endswith("/") is False:
    args.p += "/"

for i, file in enumerate(file_list):
    pop = file.split(".")[0][:3]

    prefix = file.split('.pileup')[0]

    shfile3 = open(file + '.sh', 'w')

    shfile3.write('#!/bin/bash\n' +
                  '#SBATCH -J ' + file + '.poolhmm.sh' + '\n' +
                  '#SBATCH -e /nbi/Research-Groups/JIC/Levi-Yant/Patrick/OandE/' + file + '.poolhmm.err' + '\n' +
                  '#SBATCH -o /nbi/Research-Groups/JIC/Levi-Yant/Patrick/OandE/' + file + '.poolhmm.out' + '\n' +
                  '#SBATCH -p nbi-medium\n' +
                  '#SBATCH -n ' + str(args.nc) + '\n' +
                  '#SBATCH -t 2-00:00\n' +
                  '#SBATCH --mem=' + str(args.mem) + '\n' +
                  'source python-2.7.5\n' +
                  'source env/bin/activate\n' +
                  'python /nbi/Research-Groups/JIC/Levi-Yant/Patrick/code/pool-hmm/1.4.3/pool-hmm.py -f ' + args.p + prefix + ' -e illumina -S -n ' + n[pop] + ' -c ' + args.c + ' -C ' + args.C + ' -q ' + args.q + '\n')
    shfile3.close()

    if args.P == 'false':
        cmd = ('sbatch ' + file + '.sh')
        p = subprocess.Popen(cmd, shell=True)
        sts = os.waitpid(p.pid, 0)[1]
    elif args.P == 'true':
        file1 = open(file + '.sh', 'r')
        data = file1.read()
        print(data)
    os.remove(file + '.sh')
