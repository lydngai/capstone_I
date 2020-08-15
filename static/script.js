// global variables
let recipe_count = 0;
const recipes = [];

// on log-in, set:

// localStorage.setItem("recipe_count", 0);
// localStorage.setItem("recipes", JSON.stringify([]));

// write a function to add recipe id to local session? all info - id, image,title
// when the recipe is added to local session then it can be pulled in a multiple recipe grab...

$(".recipe-cards").on("click", ".add-recipe", async function () {
  const rec_id = $(this).data("id");
  // save recipe to db
  // ADD ASYNC
  console.log(rec_id);
  // let res = await saveRecipe(rec_id);
  // console.log(res);
  $(this).text("Unsave recipe");
  $(this).removeClass("add-recipe");
  $(this).addClass("remove-recipe");
  //save recipe to global user object
});

$(".recipe-cards").on("click", ".remove-recipe", function (e) {
  const id = $(this).data("id");
  // save recipe to db
  // let res = await saveRecipe(rec_id)
  //change button to 'remove recipe' from 'add recipe' class and text.
  $(this).text("Save recipe");
  $(this).removeClass("remove-recipe");
  $(this).addClass("add-recipe");
  console.log(id);
  //save recipe to user
});

$(".log-out-btn").click(function () {
  localStorage.clear();
});

function updateRecipeBadge(num) {
  $("#recipe-count").text(num);
}
