# Top-k preference judgments

Code to manage top-k preference judgments following the process defined in Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. *Assessing top-k preferences*. ACM Transactions on Information Systems. 2021. See: https://arxiv.org/abs/2007.11682

Plus, code to to simulation preference judging from a set of existing judgments as used in Chengxi Luo, Charles L. A. Clarke and Mark D. Smucker. *Evaluation measures based on preference graphs*. ACM SIGIR 2021.

Here's an example of how to use the prefj.py program to manage crowdsourcing of preference judgments:

1) We start with a set of graded judgments. In this example, we'll use the qrels from TREC CAsT 2019.
```
    $ head -5 CAST2019.qrels.txt 
    31_1 Q0 CAR_116d829c4c800c2fc70f11692fec5e8c7e975250 0
    31_1 Q0 CAR_1463f964653c5c9f614a0a88d26b175e4a8120f1 1
    31_1 Q0 CAR_172e16e89ea3d5546e53384a27c3be299bcfe968 2
    31_1 Q0 CAR_1c93ef499a0c2856c4a857b0cb4720c380dda476 0
    31_1 Q0 CAR_2174ad0aa50712ff24035c23f59a3c2b43267650 3
```

2) Initialize the judgment process. After initialization, the file "state" contains the state of the judging process.
```
    $ ./prefj.py state initialize CAST2019.qrels.txt
```

3) Generate requests for preference judging. Each request is a (topic, document, document) triple.
```
    $ ./prefj.py state requests > requests.00
    $ head -5 requests.00
    31_1 MARCO_3990603 MARCO_291004
    31_1 MARCO_8046971 MARCO_191056
    31_1 MARCO_1462317 MARCO_3878347
    31_1 MARCO_2954451 MARCO_3878347
    31_1 MARCO_3090847 MARCO_7972824
    $ wc requests.00 
    9145   27435  517332 requests.00
```
4) Have these preference judged by people. For this example, we'll just sort them reverse alpabetically. Each result is a (topic, document, document, preference) tuple.
```
    $ cat alpha.py
    #!/usr/bin/env python3
    import sys
    if __name__ == "__main__":
        for line in sys.stdin:
            (topic, a, b) = line.rstrip().split()
            if a < b:
                print(topic, a, b, b)
            else:
                print(topic, a, b, a)
    $ ./alpha.py < requests.00 > judgments.00
    $ head -5 judgments.00
    31_1 MARCO_3990603 MARCO_291004 MARCO_3990603
    31_1 MARCO_8046971 MARCO_191056 MARCO_8046971
    31_1 MARCO_1462317 MARCO_3878347 MARCO_3878347
    31_1 MARCO_2954451 MARCO_3878347 MARCO_3878347
    31_1 MARCO_3090847 MARCO_7972824 MARCO_7972824
    
```
5) Update the state by adding the judgments, and then generate more requests.
```
    $ ./prefj.py state add judgments.00
    $ ./prefj.py state requests > requests.01
    $ head -5 requests.01
    31_1 MARCO_6430441 MARCO_5990560
    31_1 MARCO_8610842 MARCO_3990603
    31_1 MARCO_8610842 MARCO_8046971
    31_1 MARCO_2954451 MARCO_5990560
    31_1 MARCO_3878347 MARCO_3990603
```
6) Repeat until there are no more requests. It's fine to update with a subset of the requested judgments or with extra judgments.
```
    $ ./alpha.py < requests.01 > judgments.01
    $ ./prefj.py state add judgments.01
    $ ./prefj.py state requests > requests.02
    $ ./alpha.py < requests.02 > judgments.02
    $ ./prefj.py state add judgments.02
    $ ./prefj.py state requests > requests.03
    $ ./alpha.py < requests.03 > judgments.03
    $ ./prefj.py state add judgments.03
    $ ./prefj.py state requests > requests.04
    $ ./alpha.py < requests.04 > judgments.04
    $ ./prefj.py state add judgments.04
    $ ./prefj.py state requests > requests.05
    $ wc requests.*
        9145   27435  517332 requests.00
        3554   10662  144281 requests.01
        1144    3432   39820 requests.02
         219     657    7147 requests.03
          25      75     811 requests.04
           0       0       0 requests.05
       14087   42261  709391 total
```
7) You can now the judgments directly with the code from the SIGIR 2021 paper
```
$ cat judgments.* > judgments.all
```
8) Or you can extract modified qrels to use with the code from the TOIS 2021 paper.
```
$ ./prefj.py state prefs > preference.qrels
```

