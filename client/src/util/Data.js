const Data = {
  async Search() {
    return fetch(`http://localhost:8000/api/david`)
      .then((response) => {
        return response.json();
      })
      .then((jsonResponse) => {
        // console.log(jsonResponse);
        return jsonResponse.map((business) => {
          return {
            id: business[0],
            name: business[1],
            rating: business[2],
            categories: business[3],
            hours: business[4],
          };
        });
      });
  },
};

export default Data;
