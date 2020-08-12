// write a function to add recipe id to local session? all info - id, image,title
// when the recipe is added to local session then it can be pulled in a multiple recipe grab...

// on log-in, set:
// let recipe_count=0;
// let recipes =[];

$(".add-meal-plan").click(function () {
  const id = $(this).data("id");
  const title = $(this).data("title");
  const image = $(this).data("image");
  const recipe = { title, image };
  console.log(recipe);
  console.log(JSON.stringify(recipe));
  localStorage.setItem(id, JSON.stringify(recipe));
  
  
});

$(".log-out-btn").click(function () {
  localStorage.clear();
});
