// global variables
let recipe_count = 0;
const recipes = [];

// on log-in, set:

// localStorage.setItem("recipe_count", 0);
// localStorage.setItem("recipes", JSON.stringify([]));

// write a function to add recipe id to local session? all info - id, image,title
// when the recipe is added to local session then it can be pulled in a multiple recipe grab...

$(".add-recipe").click(function () {
  const id = $(this).data("id");
  const title = $(this).data("title");
  const image = $(this).data("image");
  const recipe = { id, title, image };
  
  recipe_count++;
  recipes.push(recipe);
  
  // save recipe to db
  
  //save recipe to user
});

$(".log-out-btn").click(function () {
  localStorage.clear();
});

function updateRecipeBadge(num) {
  $("#recipe-count").text(num);
}

