def array_generator(lst):
    for item in lst:
        if item.all()==0: #funktiniert jetzt nur bei arrays!
            yield item
        else: 
            array_generator(item)
             #kommen wir aus dem loop raus?? oder gehen wir nur den ersten runter?


def iterate_list(lst):
    new_lst=[]
    gen=array_generator(lst)
    for value in gen:
        new_lst.append(value)
    return new_lst