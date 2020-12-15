const Accuracy = {
  async Accuracy(user) {
    return fetch(`http://localhost:8000/accuracy/`)
      .then((response) => {
        return response.json();
      })
      .then((jsonResponse) => {
        return jsonResponse;
      });
  },
};

export default Accuracy;
