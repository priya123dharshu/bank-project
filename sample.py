# binary search

# a=[1,3,5,67,3]
# target = 7

# for i in range(0,len(a)):
#     if a[i] == target:
#         print(i)
#         break
# else:
#     print(-1)


# anagram

# def myfunc(s,t):
#     if len(s) != len(t):
#         return False
#     for i in s:
#         if s.count(i) != t.count(i):
#             return(False) 
#         # s.replace(i,"")
#     return True


# print(myfunc("anagram","negaram"))


# best time to buy and sell stock

# prices = [7,1,5,3,6,4]

# min_value = 100
# max_value = 0

# for price in prices:
#     # print(price)
#     if price < min_value:
#         # print(price)
#         min_value = price
#         print(min_value)
#     else:
#         max_value = max(max_value,price-min_value)
#         print(max_value)

# majority of element


nums = [4,4,4,4,2,34,3]
n = len(nums)//2
count = 1
i = 0
j=len(nums)-1

while i < len(nums):
    if nums[i] == nums[j]:
        count +=1
        if n < count:
            result = nums[i]
            # print(count,n)
    if j == i:
        count = 1
        j=len(nums)-1
        i+=1
    else:
        j-=1

print( result)

# def summa(nums):
#     nums.sort()
#     return nums[len(nums)//2]

# print(summa([4,4,4,4,2,34,3]))
    



