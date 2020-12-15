import csv


def GetRestaurants():
    with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_business.json') as businessFile:
        lines = businessFile.readlines()
        businesses = []
        restaurants = []
        for line in lines:
            businessID = line[16:line.find('name') - 3]
            name = line[line.find('name') + 7:line.find('address') - 3]
            state = line[line.find('state') + 8:line.find('postal_code') - 3]
            categories = line[line.find(
                'categories') + 13:line.find('hours') - 3].split(', ')
            hours = line[line.find('hours') + 8:line.find('}}') - 1]
            isRest = 'Restaurants' in categories and 'Shopping' not in categories and 'Grocery' not in categories and 'Coffee & Tea' not in categories and 'Tea Rooms' not in categories and 'Convenience Stores' not in categories and 'Hotels & Travel' not in categories and 'Internet Cafes' not in categories
            if isRest:
                businesses.append(businessID)
                restaurants.append(
                    [businessID, name, categories, state, hours])

        return businesses, restaurants


def GetReviews(businesses):
    with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_review.json') as reviewFile:
        lines = reviewFile.readlines(20000000)
        reviews = []
        for line in lines:
            userID = line[line.find('user_id') +
                          10:line.find('business_id') - 3]
            businessID = line[line.find(
                'business_id') + 14:line.find('stars') - 3]
            stars = line[line.find('stars') + 7:line.find('useful') - 2]
            date = line[line.find('date') + 7:line.find('}') - 1]
            isRest = businessID in businesses
            if isRest and date.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and len(date) < 20:
                reviews.append([userID, businessID, stars, date])

        return reviews


def GetUsers():
    reviewUsers = []
    with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/reviews.csv') as reviewsFile:
        reviewReader = csv.reader(reviewsFile)
        next(reviewReader)
        for row in reviewReader:
            reviewUsers.append(row[0])
    with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_user.json') as userFile:
        line = userFile.readline()
        users = []
        while line != '':
            userID = line[line.find('user_id') + 10:line.find('name') - 3]
            if userID in reviewUsers:
                name = line[line.find('name') +
                            7:line.find('review_count') - 3]
                users.append((userID, name))
            line = userFile.readline()

        with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/users.csv', mode='w') as outbound:
            writer = csv.writer(outbound)

            writer.writerow(['UserID', 'Name'])
            writer.writerows(users)

GetReviews(GetRestaurants())
GetUsers()
print('Finished')
