const Data = {
    async Search(term, location, sortBy) {
        return fetch(`http://localhost:8000/businesses?categories_like=Restaurant&stars_gte=4.5`)
                .then(response => {return response.json();})
                .then(jsonResponse => {
                    console.log(jsonResponse);
                    return jsonResponse.map(business => {
                        return {
                            'id': business.business_id,
                            'name': business.name,
                            'address': business.address,
                            'city': business.city,
                            'state': business.state,
                            'zipCode': business.zip_code,
                            'rating': business.stars,
                            'categories': business.categories,
                            'reviewCount': business.review_count
                        }
                    });
                });
    }
}

export default Data;