from subprocess import Popen, PIPE
p = Popen(['bc'],stdout=PIPE,stdin=PIPE)
text = p.communicate("3+4\n".encode())[0]
p.stdin.close()
print(text.decode())
