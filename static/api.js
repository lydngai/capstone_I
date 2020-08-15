const BASE_URL = "http://localhost:5000/";

// save recipe to user's recipebox, add recipe to db if missing
async function saveRecipe(rec_id) {
  //saves recipe for user
  const response = await axios.get(`${BASE_URL}save_to_recipebox/${rec_id}`, {
    withCredentials: true,
  });
  return response;
  //response will be the Recipe name
}

// remove recipe from user's recipebox
async function unsaveRecipe(rec_id) {
  //saves recipe for user
  const response = await axios.delete(`${BASE_URL}unsave_recipe/${rec_id}`);
  return response;
  //response will be the Recipe name
}
