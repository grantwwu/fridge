#!/usr/bin/python
import json, requests

#Class to do all recipe/item lookup functions
class Recipe(object):

    def __init__( self ):
        self.api_key = "****************************"
        self.recipe_base_url = "http://api.bigoven.com/recipe/"
        self.search_base_url = "http://api.bigoven.com/recipes?pg=1&rpp=25&"

    #Makes the ingredient list by the data that is returned from the recipe request
    def make_ing_list( self, jsondat ):
        inglist =[]

        for ingredients in jsondat['Ingredients']:
            inglist.append(ingredients['Name'])

        return inglist

    #Retrieves the top recipe id in the results of the recipe lookup
    def get_recipe_id( self, jsondat ):
        for recipes in jsondat['Results']:
            print recipes['Title']
            return recipes['RecipeID']

        return ""

    #Request a recipe by ID as found by gen_search_request below
    #Returns a list of ingredients so that it can be determined if they are in the fridge
    #or not.
    def gen_recipe_request ( self, id ):
        self.recipe_request = self.recipe_base_url + str(id) + "?api_key=" + self.api_key
        print self.recipe_request
        params = {'type':'GET','dataType':'json','cache':'false'}
        headers = {'Accept':'application/json','Content-Type':'application/json'}
        resp = requests.get(url=self.recipe_request, params=params, headers=headers)
        data = json.loads(resp.text)

        return self.make_ing_list(data)

    #For use when searching for a recipe with any keyword in the title
    #Example: Fried Pickles
    #Accuracy: Not too good.  Weird results are returned as this feature is much more expensive.
    #I am waiting on a response from the company that may give us this ability for no additional cost
    def gen_search_any_request ( self, akeyword ):
        self.search_any_request = self.search_base_url + "any_kw=" + akeyword + "&api_key=" + self.api_key + "&sort=quality"
        print self.search_any_request
        params = {'type':'GET','dataType':'json','cache':'false'}
        headers = {'Accept':'application/json','Content-Type':'application/json'}
        resp = requests.get(url=self.search_any_request, params=params, headers=headers)
        data = json.loads(resp.text)

        return self.get_recipe_id(data)

    #For use when searching for a recipe title
    #Example:Peach Cobbler...To satisfy a question to Alexa like "Alexa, Can Fridge make peach cobbler?"
    #Accuracy: Very good.  This can be used to return search for ingredients in a recipe
    def gen_search_title_request ( self, tkeyword ):
        self.search_title_request = self.search_base_url + "title_kw=" + tkeyword + "&api_key=" + self.api_key + "&sort=quality"
        print self.search_title_request
        params = {'type':'GET','dataType':'json','cache':'false'}
        headers = {'Accept':'application/json','Content-Type':'application/json'}
        resp = requests.get(url=self.search_title_request, params=params, headers=headers)
        data = json.loads(resp.text)

        return self.get_recipe_id(data)


