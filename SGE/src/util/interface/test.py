import numpy as np
import interface
# from fitness.interface import interface

y=np.array([0,0,0,0,0],dtype=np.double)
yhat=np.array([1,3,2,4,5],dtype=np.double)

print(y,yhat)
print('f1 score='+str(interface.eval_f1_score(y,yhat)))

# result1=interface.testf(1,3)
# result2=interface.fitness_rmse(y,yhat)
# result3=interface.edit_dis("chris","christia")
#
# print("final1 =",result1)
# print("fitness_rmse =",result2)
# print("final3 =",result3)
#
#
#
# # # test case for  multiplexer problem
# multiplexer_sample = "( i0 and ( not i11 ) and ( not i10 ) and ( not i9 ) ) or ( i1 and ( not i11 ) and ( not i10 ) and ( i9 ) ) or ( i2 and ( not i11 ) and ( i10 ) and ( not i9 ) ) or ( i3 and ( not i11 ) and ( i10 ) and ( i9 ) ) or ( i4 and i11 and not ( i10 ) and not ( i9 ) ) or ( i5 and i11 and ( not i10 ) and i9 ) or ( i6 and i11 and i10 and ( not i9 ) ) or ( i7 and i11 and i10 and i9 )";
# multiplexer_sample_size=3
# res_mul=interface.eval_multiplexer(multiplexer_sample,multiplexer_sample_size)
# print("res_mul=",res_mul)
#
#
#
# # test casse for artificial ant problem
# ant_sample="mv tl mv mv mv mv tr mv mv mv"

# ant_sample="begin  ifa begin  tl   tl   mv   mv   mv   mv   mv   tr   tr   mv   tl   tl   mv   tr   mv   tr   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   mv   tl   mv   mv   mv   mv   tr   tl   mv   mv   mv   tr   tl   mv   tl   mv   tr   mv   tr   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   tr   tl   tl   tr   tl   mv   mv   mv   tr   tl   mv   mv   tr   tl   mv   mv   mv   mv   tl   mv   tl   mv   tl   tl   mv   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   tr   tl   mv   mv   mv   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   mv   tr   mv   mv   mv   mv   mv   tl   mv   mv   mv   mv   tr   tl   mv   mv   mv   tr   tl   mv   tl   mv   tr   tr   tr   mv   tl   mv   tr   tr   tl   mv   tr   tl   mv   tl   tl   mv   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   mv   tl   mv   mv   mv   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   mv   tl   mv   mv   mv   mv   tr   tl   mv   mv   tl   mv   tr   mv   tr   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   tr   tl   tl   tr   tl   mv   mv   mv   tr   tl   mv   mv   tr   tl   mv   mv   mv   mv   tl   mv   tl   mv   tl   tl   mv   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   mv   tl   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   mv   tr   tl   mv   mv   mv   mv   tl   mv   mv   mv   mv   tr   tl   mv   mv   mv   tr   tl   mv   tl   mv   tr   mv   tr   mv   mv   mv   mv   mv   tr   tr   mv   tl   tr   mv   tl   tl   mv   mv   mv   tr   tr   tl   tl   tr   tl   mv   mv   mv   tr   tl   mv   mv   tr   tl   mv   mv   mv   mv   tl  end begin  tl  end   mv   ifa begin  tl  end begin  mv   tr  end   ifa begin  mv  end begin  mv  end   ifa begin  mv  end begin  tr   tr   mv   tl   tr   mv  end   tl   ifa begin  tr  end begin  tr  end  end"
# res_ant=interface.eval_ant(ant_sample)
# print("res_ant=",res_ant)