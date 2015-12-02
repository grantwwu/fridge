#!/usr/bin/python
import json, requests
import sys
import Recipe

def main():

    #request = Recipe.Recipe()
    #RecipeData = request.gen_recipe_request(530115)
    #print request.gen_recipe_request(RecipeData)

    #request2 = Recipe.Recipe()
    #AnyKeyword = "milk peaches sugar"
    #RecipeData2 = request2.gen_search_any_request(AnyKeyword.replace(" ", "%20"))
    #print request2.gen_recipe_request(RecipeData2)

    request3 = Recipe.Recipe()
    TitleKeyword = "Mac And Cheese"
    RecipeData3 = request3.gen_search_title_request(TitleKeyword.replace(" ", "%20"))
    print request3.gen_recipe_request(RecipeData3)



#    for ingredients in RecipeData['Ingredients']:
#        print ingredients['Name']


#    print data

if __name__ == "__main__":
    sys.exit(main())
