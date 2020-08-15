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

$(".recipe-cards").on("click", ".remove-recipe", () => {
  //delay added so action can complete
  setTimeout(() => {
    $(this).parentsUntil(".saved-card").remove();
  }, 3000);
});

//this is for items on the search page that have previously been saved
$(".recipe-cards").on("click", ".unsave-recipe", function () {
  const id = $(this).data("id");
  $(this).text("Save recipe");
  $(this).removeClass("remove-recipe");
  $(this).addClass("add-recipe");
});

$(".log-out-btn").click(function () {
  localStorage.clear();
});

function updateRecipeBadge(num) {
  $("#recipe-count").text(num);
}
