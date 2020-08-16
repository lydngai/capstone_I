$(".recipe-cards").on("click", ".add-recipe", async function () {
  const rec_id = $(this).data("id");
  // save recipe to db
  // ADD ASYNC

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

$(".recipe-cards").on("click", ".unsave-recipe", function () {
  $(this).text("Save recipe");
  $(this).removeClass("remove-recipe");
  $(this).addClass("add-recipe");
});
