def modify_list(lst):
	for i in lst:
		lst.remove(i)

lst = [1, 2, 3, 4]
modify_list(lst)
print(lst)