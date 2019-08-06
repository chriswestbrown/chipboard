from subprocess import Popen, PIPE
p = Popen(['./mybc'],stdout=PIPE,stdin=PIPE)
text = p.communicate("3+4\n")[0]
p.stdin.close()
print text
