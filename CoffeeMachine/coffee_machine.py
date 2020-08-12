class CoffeeMachine:

    def __init__(self):
        self.machine_cash = 550
        self.machine_water = 400
        self.machine_milk = 540
        self.machine_beans = 120
        self.machine_cups = 9

    def start(self):
        while True:
            choice = self.menu()
            if choice == 'exit':
                break
            elif choice == 'remaining':
                self.show_machine()
            elif choice == 'buy':
                choice_buy = self.menu_buy()
                if choice_buy == 'back':
                    continue
                elif choice_buy in ['1', '2', '3']:
                    self.make_drink(choice_buy)
            elif choice == 'fill':
                self.fill_machine()
            elif choice == 'take':
                print(f'I gave you {self.machine_cash}')
                self.machine_cash = 0;

    def menu(self):
        print('Write action (buy, fill ,take, remaining, exit):')
        action = input()
        return action


    def menu_buy(self):
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        action = input()
        return action


    def show_machine(self):
        print(f'''\nThe coffee machine has:
    {self.machine_water} of water
    {self.machine_milk} of milk
    {self.machine_beans} of coffee beans
    {self.machine_cups} of disposable cups
    ${self.machine_cash} of money
    ''')


    def check_resources(self, water, milk, beans):
        enough_water = self.machine_water - water
        enough_milk = self.machine_milk - milk
        enough_beans = self.machine_beans - beans
        enough_cups = self.machine_cups - 1
        return all(value > 0 for value in [enough_water, enough_milk, enough_beans, enough_cups])


    def buy_coffee(self, water, milk, beans, cash):
        if self.check_resources(water, milk, beans):
            self.machine_water -= water
            self.machine_milk -= milk
            self.machine_beans -= beans
            self.machine_cups -= 1
            self.machine_cash += cash
            print('I have enough resources, making you a coffee!')
        else:
            print('Sorry, not enough water!')


    def make_drink(self, drink_type):
        if drink_type == '1':
            self.buy_coffee(250, 0, 16, 4)
        elif drink_type == '2':
            self.buy_coffee(350, 75, 20, 7)
        elif drink_type == '3':
            self.buy_coffee(200, 100, 12, 6)


    def fill_machine(self):
        print('Write how many ml of water do you want to add:')
        self.machine_water += int(input())
        print('Write how many ml of milk do you want to add:')
        self.machine_milk += int(input())
        print('Write how many grams of coffee beans do you want to add:')
        self.machine_beans += int(input())
        print('Write how many disposable cups of coffee do you want to add:')
        self.machine_cups += int(input())


machine = CoffeeMachine()
machine.start()