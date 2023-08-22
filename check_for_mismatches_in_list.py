
def check_mismatches_in_lists(list_1,list_2):
      mismatch=[]
      for i in list_1:
            if i not in list_2:
                  mismatch.append(i)
      return mismatch