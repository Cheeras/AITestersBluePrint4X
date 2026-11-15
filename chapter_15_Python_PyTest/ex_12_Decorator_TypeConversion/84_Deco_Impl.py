def add_sercurity(fun):
    def wrapper():
        print("1.Before the function is called")
        print("2.Add Helment, Dashcash, gloves, knee guards, License")
        fun()
        print("3.After the function is called" )
        print("4.Remove Helment, Dashcash, gloves, knee guards, License")
    return wrapper

@add_sercurity
def drive_ola_scooter():
    print("I am driving the ola scooter")

#function calling
drive_ola_scooter()