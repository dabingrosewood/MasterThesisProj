import numpy as np
import interface
# from fitness.cython import interface

y=np.array([0,0,0,0,0],dtype=np.long)
yhat=np.array([1,3,2,4,5],dtype=np.long)

print(y,yhat)

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
# ant_sample="mv mv mv tr mv "
#
# ant_ebst="ifa begin  mv  end begin  tl ifa begin  mv end begin  tr  end  tr ifa begin mv end begin  tl  end mv   end"
# res_ant=interface.eval_ant(ant_sample)
# print("res_ant=",res_ant)


y=np.array([1.,-1.,1.,-1.,1.],dtype=np.double)
yhat=np.array([0.1,1.,1.,-1.,-1.],dtype=np.double)
f1_score=interface.fit_f1_score(y,yhat)
print(f1_score)