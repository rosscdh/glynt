Transact
--------

App to allow for the creation of sets of checklists based on a transaction object i.e. Incorporation, Seed Funding

Each of which has a set of todo checklist items that msut be customised and assocaited with the inputs from the user.


Usage
-----

1. create a transaction yaml file in **templates/transactions/<transaction_type_name>.yml** (base it on the format in the other yml files in the same dir)
2. create a new bunch class in bunches.py -> <transaction_type_name>Bunch
3. the bunch will take the form of

''''
class IncorporationBunch(BaseToDoBunch):
    """ class defined the names of fields to extract from a transaction data field """
'''

1. a class defined as above will try to load the file from template/transactions/incorporation.yml
2. the resulting object can be accessed by

'''
>>> i = IncorporationBunch()
>>> i.name
>>> i.description
>>> for c in i.todos:
>>>   print c
>>>   print i.todos.get(c).checklist
>>>   print i.todos.get(c).attachements
'''

1. Attachments in the yml file need to be defined as a "slug"
2. this slug will refer to teh slug associated with the attachment uploaded to the system