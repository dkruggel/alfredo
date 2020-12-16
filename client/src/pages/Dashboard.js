import React from 'react';
import SearchBar from '../components/SearchBar';
import Results from '../components/Results';
import DataSection from '../components/DataSection';
import Data from '../util/Data';
import Accuracy from '../util/Accuracy';
import moment from 'moment';

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      businesses: [],
      visibility: 'hidden',
      display: 'none',
      marginTop: '0',
      loading: false,
      queryTime: '',
      user: '',
    };
    this.searchHandler = this.searchHandler.bind(this);
    this.searchData = this.searchData.bind(this);
    this.measureAccuracy = this.measureAccuracy.bind(this);
    this.showLoading = this.showLoading.bind(this);
  }

  componentDidMount() {
    // this.searchHandler();
  }

  showLoading = function () {
    return new Promise(() => {
      this.setState({
        visibility: 'visible',
        display: 'flex center',
        marginTop: '250',
        loading: true,
      });
    });
  };

  searchData = function () {
    const user =
      this.props.user === 'david' ? 'ofKDkJKXSKZXu5xJNGiiBQ' : 'david';
    return new Promise(() => {
      const start = moment.now();
      Data.Search(user).then((businesses) => {
        this.setState({
          businesses: businesses,
          visibility: 'hidden',
          display: 'none',
          marginTop: '0',
          loading: false,
          queryTime: moment().diff(start, 'seconds', true),
          user: user,
        });
      });
    });
  };

  measureAccuracy = function () {
    const user =
      this.props.user === 'david' ? 'ofKDkJKXSKZXu5xJNGiiBQ' : 'david';
    return new Promise(() => {
      Accuracy.Accuracy(user).then((accuracy) => {
        this.setState({
          mae: accuracy.mae,
          rmse: accuracy.rmse,
        });
      });
    });
  };

  searchHandler = function () {
    this.showLoading().then(this.measureAccuracy()).then(this.searchData());
  };

  render() {
    // change
    return (
      <div className='App'>
        <SearchBar searchData={this.searchHandler} />
        <div className='data-sections'>
          <DataSection
            title='Algorithm Data'
            data={this.state.queryTime}
            user={this.state.user}
            mae={this.state.mae}
            rmse={this.state.rmse}
          />
        </div>
        <Results
          businesses={this.state.businesses}
          visibility={this.state.loading}
          marginTop={this.state.marginTop}
          display={this.state.display}
          loading={this.state.loading}
        />
      </div>
    );
  }
}
