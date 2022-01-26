from DataFunc.accountmanagement import UserData
userinfo = UserData()
userid = '0001'
userpassword = 'password'
userinfo.delete_account(employeeID='0001')
userinfo.createUser(userID= userid, password= userpassword, acccompl=False, username= 'Shashank Shukla',
                    accountType='admin')