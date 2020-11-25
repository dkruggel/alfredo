import React from 'react';
import './App.css';
import './components/SearchBar';
import SearchBar from './components/SearchBar';
import Results from './components/Results';
import Data from '../src/util/Data';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { businesses: [], visibility: 'hidden', display: 'none', marginTop: '0', loading: false };
    this.searchHandler = this.searchHandler.bind(this);
    this.searchData = this.searchData.bind(this);
    this.showLoading = this.showLoading.bind(this);
  }

  showLoading = function () {
    return new Promise(() => {
      this.setState({ visibility: 'visible', display: 'flex center', marginTop: '250', loading: true });
    });
  };

  searchData = function () {
    return new Promise(() => {
      Data.Search().then((businesses) => {
        this.setState({ businesses: businesses, visibility: 'hidden', display: 'none', marginTop: '0', loading: false });
      });
    });
  };

  searchHandler = function () {
    this.showLoading().then(this.searchData());
  };

  render() {
    return (
      <div className='App'>
        <SearchBar searchData={this.searchHandler} />
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
