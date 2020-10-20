import React from 'react';
import './App.css';
import './components/SearchBar';
import SearchBar from './components/SearchBar';
import Results from './components/Results';
import Data from '../src/util/Data';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { businesses: [] };
    this.searchData = this.searchData.bind(this);
  }

  searchData(term, location, sortBy) {
    Data.Search(term, location, sortBy).then((businesses) => {
      this.setState({ businesses: businesses });
    });
  }

  render() {
    return (
      <div className='App'>
        <SearchBar searchData={this.searchData} />
        <Results businesses={this.state.businesses} />
      </div>
    );
  }
}
