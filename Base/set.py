 交集（&）（intersection）：两者都存在的      

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>rint(a_set.intersection(b_set))
6 >>>print(a_set.intersection(b_set),type(a_set.intersection(b_set)))
7 >>>{4, 5} <class 'set'>#可以看出字典和集合都是{}，先将a和b都转成集合，然后求出交集（它们两都有的）
 

并集（|）（union）：去重后所有元素放一起

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>print(a_set.union(b_set))
 

差集（-）（difference）：语法使用规则是你有我没有

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>print(a_set.difference(b_set))#(前后存在顺序问题，a里面有的b里面没有的（有---没有）)
6 >>>print(b_set.difference(a_set))#b里面有的a里面没有

 

子集（issubset）：a是不是b的子集和b是不是a的子集

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>print(a_set.issubset(b_set))
6 >>>print(b_set.issubset(a_set))
7 >>>False
8 >>>False

     

父集（issuperset）：a是不是b的父集和b是不是a的子集

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>print(a_set.issuperset(b_set))
6 >>>print(b_set.issuperset(a_set))
7 >>>False
8 >>>False

        

对称差集（^）（symmetric_difference）:a和b都互相都没有（去重后放到一起）

1 >>>a = [1,2,3,4,5]
2 >>>b = [4,5,6,7,8]
3 >>>a_set = set(a)
4 >>>b_set = set(b)
5 >>>print(a_set.symmetric_difference(b_set))
6 >>>{1, 2, 3, 6, 7, 8}

a = [1,2,3,4,5]
b = [4,5,6,7,8]
a_set = set(a)
b_set = set(b)
print(a_set.isdisjoint(b_set))#前后两者存在交集就返回False，没有交集就打印True
解释：
    isdisjoint是判断a和b是否存在交集，如果存在返回False，不存在交集返回Trun

 

 

 4、基本操作

 .add(增加)添加一项

1 >>>a = [1,2,3,4,5]
2 >>>a_set = set(a)
3 >>>print(a_set)
4 >>>a_set.add(55)#一次只能添加一个元素，否则会报错
5 >>>print(a_set)
     

.update（[增加多项]）

1 >>>a = [1,2,3,4,5]
2 >>>a_set = set(a)
3 >>>print(a_set)
4 >>>a_set.update('88','lei','lei')
5 >>>print(a_set,type(a_set))
6 >>>{1, 2, 3, 4, 5}
7 >>>{1, 2, 3, 4, 5, '8', 'e', 'l', 'i'} <class 'set'>#通过结果不难看出集合天然去重

 

.remove('删除')（没有的话报错）

1 >>>a = [1,2,3,4,5]
2 >>>a_set = set(a)
3 >>>print(a_set)
4 >>>a_set.remove(1)#一次只能删除一个，否则会报错
5 >>>print(a_set,type(a_set))
 

.copy(复制)

>>>a = [1,2,3,4,5]
>>>a_set = set(a)
>>>b_set = a_set.copy()
>>>print(a_set,type(a_set))
>>>print(b_set,type(b_set))
>>>{1, 2, 3, 4, 5} <class 'set'>
>>>{1, 2, 3, 4, 5} <class 'set'>


.pop(删除任意一个并返回这个元素)

1 >>>a = [1,2,3,4,5]
2 >>>a_set = set(a)
3 >>>b_set = a_set.pop()#随机删除，并返回删除的元素
4 >>>print(a_set,type(a_set))
5 >>>print(b_set)
6 >>>{2, 3, 4, 5} <class 'set'>
7 >>>1


.discard(删除)（没有不会报错）

1 >>>a = [1,2,3,4,5]
2 >>>a_set = set(a)
3 >>>b_set = a_set.discard(5)
4 >>>print(a_set)
5 >>>print(b_set)
6 >>>{1, 2, 3, 4}
7 >>>None#有的话删除后并返回一个None
8 >>>就算没有，不报错，也只会返回一个None
