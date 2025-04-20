from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from data import cocktails, ingredient_catalog

app = FastAPI(title="Cocktail API")


@app.get("/cocktail/{name}")
def get_cocktail_by_name(name: str):
    for cocktail in cocktails:
        if cocktail["name"].lower() == name.lower():
            return cocktail
    raise HTTPException(status_code=404, detail="Cocktail not found")


@app.get("/cocktails")
def get_all_cocktails():
    return [cocktail["name"] for cocktail in cocktails]


@app.get("/ingredients")
def get_all_ingredients():
    return ingredient_catalog


@app.get("/cocktails/search")
def search_cocktails_by_ingredients(ingredients: List[str] = Query(...)):
    input_ingredients = [ing.lower() for ing in ingredients]
    matches = []

    for cocktail in cocktails:
        cocktail_ingredients = [i["name"].lower() for i in cocktail["ingredients"]]
        match_count = sum(1 for ing in input_ingredients if ing in cocktail_ingredients)

        if match_count > 0:
            matches.append({
                "cocktail": cocktail,
                "match_count": match_count,
                "total_ingredients": len(cocktail_ingredients)
            })

    matches.sort(key=lambda x: (-x["match_count"], x["total_ingredients"]))
    return JSONResponse(content=[m["cocktail"] for m in matches])
