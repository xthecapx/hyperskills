class CoffeMachine:
    ACTION = 'ACTION'
    TYPE = 'TYPE OF COFFEE'
    # INGREDIENTS
    WATER = 'water'
    MILK = 'milk'
    BEANS = 'coffee beans'
    CUPS = 'disposable cups'
    MONEY = 'money'
    MESSAGES = {
        'main': 'Write action (buy, fill, take, remaining, exit):',
        'buy': 'What do you want to buy? 1) espresso 2) latte 3) cappuccino 4) back: ',
        'fill_water': 'Write how many ml of water do you want to add: ',
        'fill_milk': 'Write how many ml of milk do you want to add: ',
        'fill_beans': 'Write how many grams of coffee beans do you want to add: ',
        'fill_cups': 'Write how many disposable cups of coffee do you want to add: '
    }

    def __init__(self, inital_ingredients):
        self.ingredients = dict([
            (self.WATER, inital_ingredients[self.WATER]),
            (self.MILK, inital_ingredients[self.MILK]),
            (self.BEANS, inital_ingredients[self.BEANS]),
            (self.CUPS, inital_ingredients[self.CUPS]),
            (self.MONEY, inital_ingredients[self.MONEY])
        ])
        self.state = 'main'

    def currentStatus(self):
        print(f"""The coffee machine has:
{self.ingredients[self.WATER]} of water
{self.ingredients[self.MILK]} of milk
{self.ingredients[self.BEANS]} of coffee beans
{self.ingredients[self.CUPS]} of disposable cups
{self.ingredients[self.MONEY]} of money\n""")

    def not_enough(self, resource):
        print(f'Sorry, not enough {resource}!\n')

    def enough_resources(self):
        print('I have enough resources, making you a coffee!\n')

    def take(self):
        print('I gave you $' + str(self.ingredients[self.MONEY]) + '\n')
        self.ingredients[self.MONEY] = 0

    def resource_validator(self, resources):
        for _index, (resource, required_value) in enumerate(resources.items()):
            if self.ingredients[resource] < required_value:
                self.not_enough(resource)

                return False

        for resource in resources:
            self.ingredients[resource] -= resources[resource]

        self.enough_resources()

        return True

    def buy(self, type):
        if type == '4':
            self.state = 'main'
        elif type == '1':
            espresso = dict([
                (self.WATER, 250),
                (self.BEANS, 16),
                (self.CUPS, 1)
            ])

            if self.resource_validator(espresso):
                self.ingredients[self.MONEY] += 4

        elif type == '2':
            latte = dict([
                (self.WATER, 350),
                (self.MILK, 75),
                (self.BEANS, 20),
                (self.CUPS, 1)
            ])

            if self.resource_validator(latte):
                self.ingredients[self.MONEY] += 7

        elif type == '3':
            cappuccino = dict([
                (self.WATER, 200),
                (self.MILK, 100),
                (self.BEANS, 12),
                (self.CUPS, 1)
            ])

            if self.resource_validator(cappuccino):
                self.ingredients[self.MONEY] += 6
        
        self.state = 'main'
    
    def start(self):
        while True:
            action = input(self.MESSAGES[self.state])

            if self.state == 'main':
                if action == "take":
                    self.take()

                if action == "buy":
                    self.state = 'buy'

                if action == "fill":
                    self.state = 'fill_water'

                if action == "remaining":
                    self.currentStatus()

                if action == "exit":
                    break
            elif self.state == 'buy':
                self.buy(action)
            elif self.state == 'fill_water':
                 self.ingredients[self.WATER] += int(action)
                 self.state = 'fill_milk'
            elif self.state == 'fill_milk':
                self.ingredients[self.MILK] += int(action)
                self.state = 'fill_beans'
            elif self.state == 'fill_beans':
                self.ingredients[self.BEANS] += int(action)
                self.state = 'fill_cups'
            elif self.state == 'fill_cups':
                self.ingredients[self.CUPS] += int(action)
                self.state = 'main'


ingredients = dict([
    (CoffeMachine.WATER, 400),
    (CoffeMachine.MILK, 540),
    (CoffeMachine.BEANS, 120),
    (CoffeMachine.CUPS, 9),
    (CoffeMachine.MONEY, 550)
])

machine = CoffeMachine(ingredients)
machine.start()
