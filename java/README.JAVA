I. to build
   a. run make to make ./chipboard executable and chipboard.jar jarfile

II. things to try
   1. seed 528 has a very wide spread! spread = 41.8705 ave = 0.1295 max = 42 xseed = 528
                                       spread = 43.94855 ave = 0.05145 max = 44 xseed = 528


III. work in progress on a file format
  
File format:
<name>
7 7
...  7 lines of 7 space -separated +/-k, where
  -k means k chip pile with red on bottom,
  +k means k chip pile with black on bottom

